"""
Verification Script for Update Manager
Tests version comparison, update checking (mocked), and installer generation.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import json
import tempfile
import shutil

# Add current directory to path
sys.path.append(os.getcwd())

from update_manager import UpdateManager

class TestUpdateManager(unittest.TestCase):
    def setUp(self):
        self.manager = UpdateManager()
        # Mock version info
        self.manager.version_info = {"version": "1.0.0"}

    def test_version_comparison(self):
        print("\n--- Testing Version Comparison ---")
        # Test cases: (v1, v2, expected_result)
        # result: 1 if v1 > v2, -1 if v1 < v2, 0 if equal
        test_cases = [
            ("1.0.0", "1.0.0", 0),
            ("1.0.1", "1.0.0", 1),
            ("1.0.0", "1.0.1", -1),
            ("1.1.0", "1.0.9", 1),
            ("2.0.0", "1.9.9", 1),
            ("1.0.0a", "1.0.0", 1), # Suffix 'a' > no suffix? Wait, usually 1.0.0a is a hotfix for 1.0.0, so it should be > 1.0.0.
            # Let's check the implementation logic in update_manager.py:
            # suffix_val = ord(suffix) - 96 if suffix else 0.
            # 'a' -> 1. '' -> 0. So 1.0.0a > 1.0.0. Correct.
            ("1.0.0b", "1.0.0a", 1),
            ("1.0.1", "1.0.0a", 1), # Patch bump > hotfix? 
            # 1.0.1 -> (1, 0, 1, 0)
            # 1.0.0a -> (1, 0, 0, 1)
            # (1,0,1,0) > (1,0,0,1) -> True. Correct.
        ]

        for v1, v2, expected in test_cases:
            result = self.manager._compare_versions(v1, v2)
            print(f"Comparing {v1} vs {v2}: Expected {expected}, Got {result}")
            self.assertEqual(result, expected, f"Failed comparison: {v1} vs {v2}")

    @patch('requests.get')
    def test_check_for_updates(self, mock_get):
        print("\n--- Testing Update Check (Mocked) ---")
        
        # Mock response for a new version
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "tag_name": "v1.0.1",
            "html_url": "http://example.com/release",
            "body": "Release notes",
            "assets": [
                {"name": "Autolauncher.zip", "browser_download_url": "http://example.com/download"}
            ]
        }]
        mock_get.return_value = mock_response

        # Force current version to be older
        self.manager.version_info = {"version": "1.0.0"}
        
        # We need to mock is_executable to True to test "can_auto_update"
        self.manager.is_executable = True
        
        update_info, error = self.manager.check_for_updates()
        
        self.assertIsNotNone(update_info)
        self.assertIsNone(error)
        self.assertEqual(update_info['version'], "1.0.1")
        self.assertTrue(update_info['can_auto_update'])
        print("Update check successful: Found 1.0.1 > 1.0.0")

    def test_installer_generation(self):
        print("\n--- Testing Installer Generation ---")
        
        # Create a dummy zip file
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "update.zip")
        
        import zipfile
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Add a dummy file to simulate content
            zf.writestr("Autolauncher/Autolauncher.exe", "dummy content")
            
        # Mock is_executable and sys.executable
        self.manager.is_executable = True
        
        # We need to mock sys.executable to be in a writable temp dir
        fake_install_dir = os.path.join(temp_dir, "install")
        os.makedirs(fake_install_dir)
        fake_exe = os.path.join(fake_install_dir, "Autolauncher.exe")
        with open(fake_exe, 'w') as f:
            f.write("old content")
            
        with patch('sys.executable', fake_exe):
            # Also need to mock subprocess.Popen so we don't actually run the batch
            with patch('subprocess.Popen') as mock_popen:
                result = self.manager.install_update_and_restart(zip_path)
                
                self.assertTrue(result)
                
                # Check if batch file was created
                batch_path = os.path.join(fake_install_dir, "_update_installer.bat")
                self.assertTrue(os.path.exists(batch_path))
                
                with open(batch_path, 'r') as f:
                    content = f.read()
                    print("Batch file content preview:")
                    print(content[:200] + "...")
                    
                    self.assertIn(f"taskkill /F /IM {os.path.basename(fake_exe)}", content)
                    self.assertIn("xcopy", content)
                    self.assertIn("start \"\" \"", content)

        # Cleanup
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()
