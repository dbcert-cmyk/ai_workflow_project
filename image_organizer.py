from datetime import datetime
from pathlib import Path


def image_organizer():
    current_dir = Path(".")
    images_archive = current_dir / "images_archive"

    if not images_archive.exists():
        images_archive.mkdir()

    total_files_moved = 0
    total_size_mb = 0

    # Correctly combine generators by iterating through extensions
    extensions = ("*.jpg", "*.jpeg", "*.png")
    files_to_move = []
    for ext in extensions:
        files_to_move.extend(current_dir.glob(ext))

    for file in files_to_move:
        try:
            # Generate new filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d")
            new_filename = f"{file.stem}_{timestamp}{file.suffix}"
            new_file_path = images_archive / new_filename

            # Calculate size before moving
            total_size_mb += file.stat().st_size / (1024 * 1024)

            file.rename(new_file_path)
            total_files_moved += 1
            print(f"Moved: {file.name} -> {new_filename}")
        except Exception as e:
            print(f"Error moving {file.name}: {e}")

    print("\n--- Summary ---")
    print(f"Total files moved: {total_files_moved}")
    print(f"Total size: {total_size_mb:.2f} MB")
    print(f"Archive location: {images_archive.absolute()}")


if __name__ == "__main__":
    image_organizer()
