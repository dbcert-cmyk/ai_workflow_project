import shutil
from datetime import datetime
from pathlib import Path


def image_organizer():
    """
    Scans the current directory for images, copies them to an archive folder,
    and renames them with today's date while preventing name conflicts.
    """
    # 1. Setup paths using pathlib
    current_dir = Path(".")
    archive_dir = current_dir / "images_archive"

    # 2. Create the archive folder if it doesn't exist
    if not archive_dir.exists():
        archive_dir.mkdir()

    # 3. Define target image types
    extensions = {".jpg", ".jpeg", ".png"}

    total_files_copied = 0
    total_size_bytes = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 4. Loop through files in the current directory
    for file in current_dir.iterdir():
        # Check if it's a file and has the right extension
        if file.is_file() and file.suffix.lower() in extensions:
            try:
                # Prepare the base new filename
                base_name = f"{file.stem}_{today_str}"
                extension = file.suffix.lower()
                target_path = archive_dir / f"{base_name}{extension}"

                # 5. Prevent overwriting (Conflict Resolution)
                counter = 1
                while target_path.exists():
                    target_path = archive_dir / f"{base_name}_{counter}{extension}"
                    counter += 1

                # 6. Perform the copy
                shutil.copy2(file, target_path)

                # 7. Update summary data
                total_files_copied += 1
                total_size_bytes += target_path.stat().st_size

            except Exception as e:
                print(f"Error processing {file.name}: {e}")

    # 8. Print Final Summary
    total_size_mb = total_size_bytes / (1024 * 1024)
    print("-" * 30)
    print("ORGANIZATION COMPLETE")
    print(f"Total files copied: {total_files_copied}")
    print(f"Archive total size: {total_size_mb:.2f} MB")
    print("-" * 30)


if __name__ == "__main__":
    image_organizer()
