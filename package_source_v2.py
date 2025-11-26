import shutil
import os
import zipfile
from pathlib import Path

def zip_project():
    # Read version from config
    import config
    version = config.APP_VERSION
    
    # Output to release directory
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    output_filename = release_dir / f"c4n-AutoLauncher_v{version}_Source.zip"
    
    # Files/Dirs to exclude
    excludes = {
        'venv', '.git', '.vscode', '__pycache__', 
        'logs', 'dist', 'build', '.idea', 'release',
        '.gitignore', '.env'
    }
    
    print(f"Creating source package: {output_filename}")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in excludes]
            
            for file in files:
                if file in excludes or file.endswith('.pyc') or file.endswith('.zip'):
                    continue
                    
                file_path = os.path.join(root, file)
                # Archive name should not have leading ./
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                print(f"  Adding: {arcname}")
                
    print(f"Created {output_filename}")
    
    # Get size
    size_mb = output_filename.stat().st_size / (1024 * 1024)
    print(f"Package size: {size_mb:.2f} MB")
    
    return output_filename

if __name__ == "__main__":
    zip_project()
