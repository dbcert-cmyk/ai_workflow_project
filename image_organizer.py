import os
from pathlib import Path
from datetime import datetime

def image_organizer():
    current_dir = Path('.')
    images_archive = current_dir / 'images_archive'
    
    if not images_archive.exists():
        images_archive.mkdir()
    
    total_files_moved = 0
    total_size_mb = 0
    
    for file in current_dir.glob('*.jpg') | current_dir.glob('*.jpeg') | current_dir.glob('*.png'):
        try:
            new_filename = f"{file.stem}_{datetime.now().strftime('%Y-%m-%d')}{file.suffix}"
            new_file_path = images_archive / new_filename
            file.rename(new_file_path)
            
            total_files_moved += 1
            total_size_mb += file.stat().st_size / (1024 * 1024)
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    print(f"Total number of files moved: {total_files_moved}")
    print(f"Total size of the archive in MB: {total_size_mb:.2f}")

if __name__ == '__main__':
    image_organizer()
