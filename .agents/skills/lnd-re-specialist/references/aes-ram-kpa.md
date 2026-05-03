# AES RAM Known-Plaintext Attack (KPA)

This capability guides the user through extracting a hidden AES-256 key from a running Unreal Engine 5 game process.

## The Principle

Instead of searching for hardcoded keys in the executable or matching GUID strings, we use a Known-Plaintext Attack:
1. UE5 encrypted pak indices always start with an `FString` mount point (e.g., `../../../`).
2. An `FString` is serialized as a 32-bit integer (length) followed by the UTF-8/UTF-16 string data.
3. The game must eventually hold the raw 32-byte AES key in process memory to decrypt assets.
4. We scan process memory (RAM) in 16-byte aligned chunks, trying each 32-byte sequence as an AES decryption key against the first 32 bytes of the encrypted pak index.
5. If the decrypted output starts with a plausible `FString` length (1 to 512) and contains printable ASCII text matching a mount point, we have found the key.

## Instructions

1. Ensure the user has the game running in Windows.
2. Use the deterministic script `./scripts/ue5_aes_ram_kpa.py`.
3. Provide the script to the user or run it through the appropriate terminal access if available.

### Script Execution

```bash
# Requires Python and pycryptodome (pip install pycryptodome)
python ./scripts/ue5_aes_ram_kpa.py <pid> <path_to_pak_file>
```

If the user does not know the PID or Pak path, instruct them to use Task Manager context and game directory paths.

## Outcome

The script will output the memory address, the 32-byte Hex AES key, and the decrypted mount point. Save this key output to a text file for the user.
