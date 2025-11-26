"""
Release Simulation Script
Runs a local HTTP server to act as a fake GitHub release source and tests the full update flow.
"""

import os
import sys
import json
import time
import shutil
import threading
import tempfile
import zipfile
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path

# Add current directory to path
sys.path.append(os.getcwd())

from update_manager import UpdateManager

# Configuration
PORT = 8000
HOST = "localhost"
BASE_URL = f"http://{HOST}:{PORT}"
TEST_VERSION = "9.9.9" # A version guaranteed to be newer
TEST_DIR = "test_release_server"

def setup_test_server_files():
    """Create the necessary files for the test server."""
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    # 1. Create a dummy update zip
    zip_name = "Autolauncher_v9.9.9.zip"
    zip_path = os.path.join(TEST_DIR, zip_name)
    
    # Create content to zip
    content_dir = os.path.join(TEST_DIR, "content")
    os.makedirs(content_dir)
    
    # Structure: c4n-AutoLauncher/Autolauncher.exe
    app_dir = os.path.join(content_dir, "c4n-AutoLauncher")
    os.makedirs(app_dir)
    
    with open(os.path.join(app_dir, "Autolauncher.exe"), "w") as f:
        f.write("This is the new version executable")
        
    with open(os.path.join(app_dir, "README.txt"), "w") as f:
        f.write("New version installed successfully!")
        
    # Zip it
    shutil.make_archive(os.path.join(TEST_DIR, "Autolauncher_v9.9.9"), 'zip', content_dir)
    
    # 2. Create releases.json response
    releases_data = [
        {
            "tag_name": f"v{TEST_VERSION}",
            "html_url": f"{BASE_URL}/release_page",
            "body": "## Test Release\nThis is a simulated release for testing.",
            "assets": [
                {
                    "name": zip_name,
                    "browser_download_url": f"{BASE_URL}/{zip_name}",
                    "size": os.path.getsize(zip_path),
                    "content_type": "application/zip"
                }
            ]
        }
    ]
    
    with open(os.path.join(TEST_DIR, "releases.json"), "w") as f:
        json.dump(releases_data, f)
        
    print(f"Test server files created in {TEST_DIR}")

from functools import partial

def start_server():
    """Start the HTTP server in a background thread."""
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Silence logs
            
    # Bind the directory to the handler
    # Note: 'directory' argument is available in Python 3.7+
    handler_class = partial(Handler, directory=TEST_DIR)
            
    server = HTTPServer((HOST, PORT), handler_class)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    print(f"Server started at {BASE_URL}")
    return server

def run_simulation():
    setup_test_server_files()
    server = start_server()
    
    print("\n--- Starting Update Simulation ---")
    
    # Set environment variables for test mode
    # Point to releases.json
    os.environ["AUTOLAUNCHER_UPDATE_URL"] = f"{BASE_URL}/releases.json"
    os.environ["AUTOLAUNCHER_TEST_MODE"] = "1"
    
    # FIX: Update the global variable in the module because it was already imported
    import update_manager as um_module
    um_module.GITHUB_API_URL = f"{BASE_URL}/releases.json"
    
    # Clear ETag cache to ensure fresh check
    if os.path.exists("etag_cache.json"):
        os.remove("etag_cache.json")
        
    # Configure logging
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    
    # Verify server is reachable
    try:
        print(f"Verifying server at {BASE_URL}/releases.json...")
        resp = requests.get(f"{BASE_URL}/releases.json")
        print(f"Server response: {resp.status_code}")
        print(f"Server content: {resp.text[:100]}...")
    except Exception as e:
        print(f"Server verification failed: {e}")

    try:
        manager = UpdateManager()
        print(f"Current version: {manager.get_current_version()}")
        
        # 1. Check for updates
        print("\nChecking for updates...")
        update_info, error = manager.check_for_updates()
        
        if error:
            print(f"ERROR: {error}")
            return
            
        if not update_info:
            print("No updates found! (Something is wrong, we expect v9.9.9)")
            return
            
        print(f"Update found: {update_info['version']}")
        print(f"Update info keys: {update_info.keys()}")
        
        # 2. Download update
        print("\nDownloading update...")
        # Updated to use zip_asset (our fix changed exe_asset to zip_asset)
        zip_asset = update_info.get('zip_asset') or update_info.get('exe_asset')
        
        if not zip_asset:
            print("ERROR: No update package asset found in update info")
            print(f"Available keys: {update_info.keys()}")
            return
            
        def progress(dl, total):
            sys.stdout.write(f"\rProgress: {dl}/{total} bytes")
            sys.stdout.flush()
            
        zip_path = manager.download_update(zip_asset, progress)

        print("\nDownload complete!")
        
        # 3. Install update
        print("\nInstalling update...")
        success = manager.install_update_and_restart(zip_path)
        
        if success:
            print("Installation started successfully!")
            
            # Verify the batch file exists in the temp install dir
            temp_install_dir = os.path.join(tempfile.gettempdir(), "autolauncher_test_install")
            batch_path = os.path.join(temp_install_dir, "_update_installer.bat")
            
            if os.path.exists(batch_path):
                print(f"SUCCESS: Batch file created at {batch_path}")
                print("Simulation PASSED.")
            else:
                print(f"FAILURE: Batch file NOT found at {batch_path}")
        else:
            print("Installation FAILED.")
            
    finally:
        # Cleanup
        if os.path.exists(TEST_DIR):
            try:
                shutil.rmtree(TEST_DIR)
            except:
                pass
        
        # Clean temp install dir
        temp_install_dir = os.path.join(tempfile.gettempdir(), "autolauncher_test_install")
        if os.path.exists(temp_install_dir):
            try:
                shutil.rmtree(temp_install_dir)
            except:
                pass

if __name__ == "__main__":
    run_simulation()
