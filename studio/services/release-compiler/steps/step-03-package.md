# Step 03: Final Package

**Goal:** Provide the final zipped asset containing everything the user needs for distribution or direct ingestion.

## Instructions

1. **Verify Integrity**: Perform a quick read of the `release_manifest.json` ensuring all paths in the asset index actually point to valid files within `novel/base`, `novel/modded`, and `roleplay/`.
2. **Zip the Release**: Using a shell command (`run_command`), compress the `_release/[project_name]` folder into a `[project_name]-[version].zip` archive. Place the archive in the root `_release/` directory alongside the unzipped version.
3. **Notify User**: Conclude the workflow by using the `notify_user` command to present the user with the final absolute path of the zipped release, alongside a short summary of the content warnings and version included.

## Completion

Once the user is notified, the release compiler workflow is successfully concluded. Wait for the user's response.
