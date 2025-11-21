import shutil
import os
import zipfile

def zip_project():
    output_filename = "Autolauncher_v0.1.1_Source.zip"
    
    # Files/Dirs to exclude
    excludes = {
        'venv', '.git', '.vscode', '__pycache__', 
        'logs', 'dist', 'build', '.idea',
        output_filename # Don't include the zip itself
    }
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in excludes]
            
            for file in files:
                if file in excludes or file.endswith('.pyc'):
                    continue
                    
                file_path = os.path.join(root, file)
                # Archive name should not have leading ./
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                
    print(f"Created {output_filename}")

if __name__ == "__main__":
    zip_project()
