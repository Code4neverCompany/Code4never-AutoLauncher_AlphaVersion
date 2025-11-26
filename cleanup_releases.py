"""
Post-Release Cleanup Script
Cleans up build artifacts and old release files.
- Keeps only the last 3 versions in the release/ folder.
- Keeps only the latest BUILD_SUMMARY and GITHUB_RELEASE files in the root directory.

© 2025 4never Company. All rights reserved.
"""

import os
import glob
import json
import re
import shutil
from pathlib import Path

def clean_root_artifacts(pattern):
    """Keep only the latest file matching the pattern."""
    files = glob.glob(pattern)
    if not files:
        return

    # Sort by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)

    # Keep the first one
    latest = files[0]
    print(f"\nCleaning {pattern}...")
    print(f"  Keeping latest: {latest}")

    # Remove the rest
    removed_count = 0
    for f in files[1:]:
        try:
            os.remove(f)
            print(f"  ✓ Removed old: {f}")
            removed_count += 1
        except Exception as e:
            print(f"  ✗ Failed to remove {f}: {e}")
            
    if removed_count == 0 and len(files) > 1:
        print("  No files removed (unexpected).")
    elif removed_count > 0:
        print(f"  Removed {removed_count} old files.")

def clean_release_folder():
    """Keep artifacts for the last 3 versions."""
    release_dir = Path("release")
    if not release_dir.exists():
        return

    print("\nCleaning release folder...")

    # Get all files
    files = [f for f in release_dir.glob("*") if f.is_file()]
    
    if not files:
        print("  Release folder is empty.")
        return

    # Group files by version
    # Regex to capture version: v(1.0.13a) or v(1.0.13)
    version_pattern = re.compile(r"v(\d+\.\d+\.\d+[a-z]*)")
    
    version_map = {} # version_str -> list of files
    
    for f in files:
        match = version_pattern.search(f.name)
        if match:
            version = match.group(1)
            if version not in version_map:
                version_map[version] = []
            version_map[version].append(f)
        else:
            # Treat non-matching files as separate "versions" or just ignore them?
            # Let's ignore them for deletion to be safe, or print a warning.
            # Actually, if we want to clean up, we should probably be careful.
            # But the user said "reduce the files... to only have the last 3 releases".
            # So we should probably only touch release artifacts.
            pass
            
    if not version_map:
        print("  No versioned files found.")
        return

    # Calculate age for each version (max mtime of its files)
    version_ages = []
    for version, v_files in version_map.items():
        max_mtime = max(f.stat().st_mtime for f in v_files)
        version_ages.append((version, max_mtime))
        
    # Sort by mtime descending (newest first)
    version_ages.sort(key=lambda x: x[1], reverse=True)
    
    # Keep top 3
    keep_versions = [v[0] for v in version_ages[:3]]
    
    print(f"  Keeping versions: {', '.join(keep_versions)}")
    
    # Remove others
    removed_count = 0
    for version, v_files in version_map.items():
        if version not in keep_versions:
            for f in v_files:
                try:
                    f.unlink()
                    print(f"  ✓ Removed: {f.name}")
                    removed_count += 1
                except Exception as e:
                    print(f"  ✗ Failed to remove {f.name}: {e}")
                    
    print(f"  Removed {removed_count} files from release folder.")

def clean_build_artifacts():
    """Clean up temporary build artifacts."""
    print("\nCleaning build artifacts...")
    
    # Clean __pycache__ recursively
    for pycache_dir in glob.glob('**/__pycache__', recursive=True):
        try:
            shutil.rmtree(pycache_dir)
            print(f"  ✓ Removed: {pycache_dir}")
        except Exception as e:
            print(f"  ✗ Failed to remove {pycache_dir}: {e}")
    
    # Clean other temp files
    temp_files = ['etag_cache.json', 'last_update_check.json']
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"  ✓ Removed: {temp_file}")
            except Exception as e:
                print(f"  ✗ Failed to remove {temp_file}: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Project Cleanup Script")
    print("=" * 60)
    
    # 1. Clean Root Artifacts
    clean_root_artifacts("BUILD_SUMMARY_v*.md")
    clean_root_artifacts("GITHUB_RELEASE_v*.md")
    
    # 2. Clean Release Folder
    clean_release_folder()
    
    # 3. Clean Build Artifacts
    clean_build_artifacts()
    
    print("\n" + "=" * 60)
    print("Cleanup Complete!")
    print("=" * 60)
