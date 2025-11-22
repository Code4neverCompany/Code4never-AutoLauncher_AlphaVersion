import os
import glob
import subprocess
import json
import sys

VERSION_FILE = "version_info.json"

def load_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get("version", "0.0.0")
    return "0.0.0"

def get_release_notes(version):
    """Extract changelog entries for the given version from version_info.json."""
    if not os.path.exists(VERSION_FILE):
        return ""
    with open(VERSION_FILE, 'r') as f:
        data = json.load(f)
    for entry in data.get("changelog", []):
        if entry.get("version") == version:
            changes = entry.get("changes", [])
            notes = f"## Changes for version {version}\n"
            for change in changes:
                notes += f"- {change}\n"
            return notes
    return ""

def prepend_update_system(notes):
    """Prepend the release notes to UPDATE_SYSTEM.md so the program can display them."""
    update_path = "UPDATE_SYSTEM.md"
    if not os.path.exists(update_path):
        return
    with open(update_path, 'r', encoding='utf-8') as f:
        existing = f.read()
    with open(update_path, 'w', encoding='utf-8') as f:
        f.write(notes + "\n" + existing)

def publish_release():
    version = load_version()
    print(f"Publishing Release v{version}...")

    # Generate release notes
    release_notes = get_release_notes(version)
    if release_notes:
        prepend_update_system(release_notes)
        print("Release notes added to UPDATE_SYSTEM.md")
    else:
        print("No release notes found for this version.")

    # Find artifacts
    release_dir = "release"
    files = glob.glob(f"{release_dir}/*v{version}*")

    if not files:
        print(f"No artifacts found for version {version} in {release_dir}/")
        return

    print(f"Found artifacts: {files}")

    tag = f"v{version}"
    title = f"v{version} Release"

    # Build gh command
    cmd = [
        "gh", "release", "create", tag,
    ] + files + [
        "--title", title,
        "--notes", release_notes,
        "--generate-notes"
    ]

    print("Running gh release create...")
    try:
        subprocess.run(cmd, check=True)
        print("✅ Release published successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to publish release: {e}")

if __name__ == "__main__":
    publish_release()
