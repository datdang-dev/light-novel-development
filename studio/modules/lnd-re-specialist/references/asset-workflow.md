# Asset Workflow

This capability guides the user from key extraction to using the 3D assets in Blender.

## Prerequisites
1. AES Key (Extracted via `Encryption Analysis` -> `AES RAM KPA`).
2. FModel (Configured correctly for the UE5 Engine version and Directory).

## FModel Setup

1. **Directories:** Select the game root folder containing the `WindowsNoEditor` or similar packaged client.
2. **Local Settings:** Ensure `UE5.x` version matches the game (Check executables headers if unknown, e.g. `UE5.4`).
3. **AES Key:** Add the extracted hex string to the FModel AES Key Manager.
4. **Load Mode:** Ensure "Load all Paks" is used.

## Finding Assets

Instruct the user to navigate the FModel virtual repository `Game/Content/`:
- **Meshes:** Usually in `/Characters/` or `/Models/`. Suffixes: `_Mesh`, `_Skin`.
- **Textures:** Usually in `/Textures/` or `/Materials/`. Suffixes:
  - `_D` / `_BC` / `_BaseColor` -> Diffuse/Base Color.
  - `_N` / `_Normal` -> Normal Map.
  - `_R` / `_RHA` / `_ORM` -> Roughness/Metallic/Ambient Occlusion maps (often packed into RGB channels).

## Exporting

1. Select desired `SkeletalMesh` (.uasset) or `StaticMesh` (.uasset).
2. Right-click and **Save Packages** or export via the 3D viewer.
3. Export format should ideally be `.psk` (for psk import plugins in Blender) or `.gltf` / `.fbx` if FModel supports it cleanly.

## Hand-off

Cipher's job ends at unlocking and extracting the models. For Blender material assignments or rigging, the user might transition to another agent if needed.
