import os, shutil, json, zipfile

TEST_DIR = "test_release_server"
ZIP_NAME = "Autolauncher_v9.9.9.zip"
VERSION = "9.9.9"
BASE_URL = "http://localhost:8000"

def create_test_release():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    # Create dummy content
    content_dir = os.path.join(TEST_DIR, "content")
    os.makedirs(content_dir)
    app_dir = os.path.join(content_dir, "c4n-AutoLauncher")
    os.makedirs(app_dir)
    with open(os.path.join(app_dir, "Autolauncher.exe"), "w") as f:
        f.write("This is the new version executable")
    with open(os.path.join(app_dir, "README.txt"), "w") as f:
        f.write("New version installed successfully!")

    # Create zip archive
    zip_path = os.path.join(TEST_DIR, ZIP_NAME)
    shutil.make_archive(os.path.splitext(zip_path)[0], "zip", content_dir)

    # Create releases.json
    releases = [{
        "tag_name": f"v{VERSION}",
        "html_url": f"{BASE_URL}/release_page",
        "body": "## Test Release\nThis is a simulated release for testing.",
        "assets": [{
            "name": ZIP_NAME,
            "browser_download_url": f"{BASE_URL}/{ZIP_NAME}",
            "size": os.path.getsize(zip_path),
            "content_type": "application/zip"
        }]
    }]
    with open(os.path.join(TEST_DIR, "releases.json"), "w") as f:
        json.dump(releases, f)
    print(f"Test release files created in {TEST_DIR}")

if __name__ == "__main__":
    create_test_release()
