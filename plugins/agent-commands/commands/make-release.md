---
description: Make a versioned release of the repository
argument-hint: [version] | patch | minor | major
allowed-tools: Read, Bash, Edit, Write, Glob
---

Make a release of this repository.

Version or release type: "$ARGUMENTS"

## Step-by-Step Process:

### 1. Detect the project type and current version

Scan the repository to determine the project type and find the current version. Check these sources in order, using the first one found:

- `package.json` (Node.js/TypeScript) -- read the `"version"` field
- `Cargo.toml` (Rust) -- read the `version` field under `[package]`
- `pyproject.toml` (Python) -- read `version` under `[project]` or `[tool.poetry]`
- `setup.cfg` (Python legacy) -- read `version` under `[metadata]`
- `VERSION` or `version.txt` file -- read the contents directly
- Git tags -- use `git describe --tags --abbrev=0` and strip any leading `v`

If no version source is found, ask the user where the version is defined.

Store the detected source file and current version for later use.

### 2. Determine the target version

The `$ARGUMENTS` can be either:
- An explicit version number (e.g., `1.2.3`) -- use that directly as `$NEW_VERSION`
- A release type: `patch`, `minor`, or `major` -- bump from the current version accordingly:
  - `patch`: `1.2.3` -> `1.2.4`
  - `minor`: `1.2.3` -> `1.3.0`
  - `major`: `1.2.3` -> `2.0.0`

If no argument is provided, ask the user which version or type to use.

### 3. Update the changelog

Run the `/update-changelog` command to ensure the changelog is up to date with recent changes.

### 4. Verify with the user

Before making changes, confirm with the user:
> Releasing version **$NEW_VERSION** (currently $CURRENT_VERSION).
> Version source: `$VERSION_FILE`
> Proceed?

### 5. Update the version file

Update the version in the detected source file:

- **package.json**: Update the `"version"` field. Then run `npm install --package-lock-only` if a `package-lock.json` exists to keep it in sync.
- **Cargo.toml**: Update the `version` field under `[package]`. Then run `cargo check` if available to update `Cargo.lock`.
- **pyproject.toml**: Update the `version` field in the appropriate section.
- **setup.cfg**: Update the `version` field under `[metadata]`.
- **VERSION/version.txt**: Write the new version to the file.

### 6. Update CHANGELOG.md

Edit the `CHANGELOG.md` file:
- Change the `# Unreleased` heading to `# $NEW_VERSION`
- Add a new `# Unreleased` section at the top (empty for now)

### 7. Create the release commit and tag

Stage only the files that were modified (version file, lockfile, CHANGELOG.md):

```bash
git add $VERSION_FILE CHANGELOG.md   # and lockfile if updated
git commit -m "Release $NEW_VERSION"
git tag "$NEW_VERSION"
```

### 8. Show push instructions

After the release commit and tag are created, show the user the commands to push:

```bash
git push origin $(git branch --show-current) && git push origin $NEW_VERSION
```

**Important:** Do NOT automatically push. Let the user review the commit and tag first, then they can manually run the push commands.

## Notes

- If a `scripts/release.sh` or similar release script exists in the repo, mention it to the user and ask if they want to use it instead of the generic steps above
- The user should review the commit and tag before pushing
- Using an explicit version number is recommended so that aborted releases can be retried without accidentally double-bumping
