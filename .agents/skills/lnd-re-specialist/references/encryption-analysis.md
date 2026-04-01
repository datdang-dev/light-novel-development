# Encryption Analysis

This capability helps users analyze Unreal Engine game files to determine the engine version, container format, and encryption state.

## Approach

1. **Identify Engine Version:** Have the user upload or inspect the main executable. Determine if it's UE4 or UE5.
2. **Container Format:** Check the `/Content/Paks/` folder.
   - `.pak` only = Legacy format.
   - `.utoc` / `.ucas` = UE5 IoStore format.
3. **Encryption Verification:**
   - Ask the user to run `fmodel` or use a hex editor on the pak/utoc footer.
   - For UE5 v11 (IoStore), the `FPakInfo` structure is 204 or 221 bytes from the EOF.
   - Magic byte `E1 12 6F 5A` confirms a pak footer.
   - If `bEncryptedIndex` is 1, the pak is encrypted.
   - If `EncryptionKeyGuid` is `{00000000-00000000-00000000-00000000}` (Null GUID), the game dynamically generates or uses a default encryption key at runtime.

## Outcome
Determine whether we need to perform an AES Known-Plaintext Attack to extract the key from memory. If the pak is encrypted and the key is not public, guide the user to the AES RAM KPA capability.
