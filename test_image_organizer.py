import os
from datetime import datetime

import pytest

from image_organizer import image_organizer


@pytest.fixture
def test_env(tmp_path):
    """
    Creates a temporary clean folder for every test run.
    This ensures we don't move or delete your actual files.
    """
    # Create dummy files for testing
    (tmp_path / "vacation.jpg").write_text("fake image data")
    (tmp_path / "portrait.png").write_text("fake image data")
    (tmp_path / "notes.txt").write_text("this should be ignored")

    # Switch to the temp directory
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path

    # Switch back to original directory after test
    os.chdir(old_cwd)


def test_organization_logic(test_env):
    """Checks if images are copied and renamed, and txt files are ignored."""
    # Run the script
    image_organizer()

    archive = test_env / "images_archive"
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Check 1: Did the folder get created?
    assert archive.exists()

    # Check 2: Were only the 2 images copied?
    copied_files = list(archive.glob("*"))
    msg = f"Expected 2 files in archive, but found {len(copied_files)}"
    assert len(copied_files) == 2, msg

    # Check 3: Did the filenames include today's date?
    for file in copied_files:
        msg = f"Filename {file.name} is missing the date suffix."
        assert today_str in file.name, msg


def test_no_images_scenario(tmp_path):
    """Checks if the script handles a folder with zero images gracefully."""
    os.chdir(tmp_path)
    image_organizer()

    archive = tmp_path / "images_archive"
    assert archive.exists()
    assert len(list(archive.glob("*"))) == 0
