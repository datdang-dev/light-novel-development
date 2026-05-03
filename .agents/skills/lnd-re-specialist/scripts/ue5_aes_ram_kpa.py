import sys
import os
import struct
import ctypes
from ctypes import wintypes
from Crypto.Cipher import AES

# ---- Windows API Definitions ----
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

class MEMORY_BASIC_INFORMATION64(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_ulonglong),
        ("AllocationBase", ctypes.c_ulonglong),
        ("AllocationProtect", wintypes.DWORD),
        ("__alignment1", wintypes.DWORD),
        ("RegionSize", ctypes.c_ulonglong),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("__alignment2", wintypes.DWORD),
    ]

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

ReadProcessMemory = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_size_t)
]
ReadProcessMemory.restype = wintypes.BOOL

VirtualQueryEx = kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.POINTER(MEMORY_BASIC_INFORMATION64),
    ctypes.c_size_t
]
VirtualQueryEx.restype = ctypes.c_size_t

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

# ---- Helper Functions ----

def is_valid_string(decrypted_bytes):
    """
    Checks if the first 4 bytes of decrypted_bytes form a valid length prefix,
    followed by readable characters starting with '../../../' or similar paths.
    """
    if len(decrypted_bytes) < 32:
        return False
    
    length = struct.unpack('<i', decrypted_bytes[:4])[0]
    if length <= 0 or length > 512:
        return False
    
    string_data = decrypted_bytes[4:]
    actual_len = min(length, len(string_data))
    
    # Try to decode as ascii/utf8
    try:
        decoded = string_data[:actual_len].decode('utf-8').rstrip('\x00')
        if decoded.startswith('../../') or decoded.startswith('/'):
            return True
        if all(32 <= c < 127 for c in string_data[:min(10, actual_len)]): 
            # Plausible text
            return True
    except UnicodeDecodeError:
        pass
    
    return False

def get_encrypted_pak_header(pak_path):
    """
    Read the first 32 bytes from the pak file (if encrypted, this is the start of the index block)
    Note: Ideally we seek to the start of the index block based on the footer offset, 
    but for many games, hitting early index headers or even the global AES testing blocks is sufficient.
    """
    # Simply reading the first encrypted block of the index is best.
    # This requires footer parsing in a real scenario.
    print(f"[*] Extracting footer logic from {pak_path}")
    
    with open(pak_path, 'rb') as f:
        f.seek(-221, os.SEEK_END)
        footer_data = f.read(221)
        
        # Look for magic
        magic_pos = footer_data.find(b'\xE1\x12\x6F\x5A')
        if magic_pos == -1:
            # Try earlier position
            f.seek(-204, os.SEEK_END)
            footer_data = f.read(204)
            magic_pos = footer_data.find(b'\xE1\x12\x6F\x5A')
            if magic_pos == -1:
                print("[-] Could not find UE Pak magic in footer.")
                sys.exit(1)
                
        # Parse IndexOffset (Assuming v11 IoStore or v9/v11 pak)
        f.seek(-len(footer_data) + magic_pos, os.SEEK_END)
        f.read(4) # Magic
        f.read(4) # Version
        index_offset = struct.unpack('<Q', f.read(8))[0]
        index_size = struct.unpack('<Q', f.read(8))[0]
        
        # Read the first 32 bytes of the encrypted index
        f.seek(index_offset)
        encrypted_index_head = f.read(32)
        
        if len(encrypted_index_head) < 32:
            print("[-] Not enough data at index offset.")
            sys.exit(1)
            
        print(f"[+] Found Index Offset: {index_offset}")
        return encrypted_index_head

def scan_process_for_key(pid, target_cipher_bytes):
    print(f"[*] Opening process {pid}")
    process_handle = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    
    if not process_handle:
        print(f"[-] Failed to open process. Error code: {ctypes.get_last_error()}")
        sys.exit(1)

    MEM_COMMIT = 0x1000
    PAGE_READWRITE = 0x04
    PAGE_EXECUTE_READWRITE = 0x40
    
    system_info = wintypes.SYSTEM_INFO()
    kernel32.GetSystemInfo(ctypes.byref(system_info))
    
    address = ctypes.c_ulonglong(0)
    mbi = MEMORY_BASIC_INFORMATION64()
    
    bytes_read = ctypes.c_size_t(0)
    print("[*] Scanning memory for valid AES keys...")
    
    found_keys = []
    
    while VirtualQueryEx(process_handle, address, ctypes.byref(mbi), ctypes.sizeof(mbi)):
        if mbi.State == MEM_COMMIT and mbi.Protect in (PAGE_READWRITE, PAGE_EXECUTE_READWRITE):
            buffer = ctypes.create_string_buffer(mbi.RegionSize)
            if ReadProcessMemory(process_handle, ctypes.c_void_p(mbi.BaseAddress), buffer, mbi.RegionSize, ctypes.byref(bytes_read)):
                
                data = buffer.raw[:bytes_read.value]
                
                # Scan through memory chunk in 16-byte aligned pieces
                for i in range(0, len(data) - 32, 16):
                    candidate_key = data[i:i+32]
                    
                    try:
                        cipher = AES.new(candidate_key, AES.MODE_ECB)
                        decrypted = cipher.decrypt(target_cipher_bytes)
                        if is_valid_string(decrypted):
                            key_hex = "0x" + candidate_key.hex().upper()
                            address_hex = "0x{:016X}".format(mbi.BaseAddress + i)
                            
                            print(f"\n[!!!] KEY FOUND at {address_hex}")
                            print(f"[+] Key: {key_hex}")
                            
                            try:
                                print(f"[+] Decrypted sample: {decrypted.decode('utf-8', errors='ignore').rstrip(chr(0))}")
                            except Exception:
                                pass
                            
                            found_keys.append(key_hex)
                            # Could continue or break, stopping on first match for speed.
                            return found_keys
                    except Exception as e:
                        pass
        address.value = mbi.BaseAddress + mbi.RegionSize

    CloseHandle(process_handle)
    return found_keys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ue5_aes_ram_kpa.py <pid> <path_to_pak_file>")
        sys.exit(1)
        
    pid = int(sys.argv[1])
    pak_path = sys.argv[2]
    
    encrypted_block = get_encrypted_pak_header(pak_path)
    print(f"[*] Targeting encrypted block: {encrypted_block.hex()}")
    
    scan_process_for_key(pid, encrypted_block)
    print("[*] Scan complete.")
