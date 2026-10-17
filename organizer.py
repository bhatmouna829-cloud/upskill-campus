import os
import shutil


# File categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css"]
}


# Store the last organization
last_organization = []


# Find the category of a file
def get_category(filename):

    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


# Organize files
def organize_files(folder_path, progress_callback=None):

    global last_organization

    # Clear previous history
    last_organization = []

    category_counts = {
        "Images": 0,
        "Documents": 0,
        "Videos": 0,
        "Audio": 0,
        "Archives": 0,
        "Code": 0,
        "Others": 0
    }

    # Find files
    files = []

    for filename in os.listdir(folder_path):

        source_path = os.path.join(
            folder_path,
            filename
        )

        if os.path.isfile(source_path):
            files.append(filename)

    total_files = len(files)
    moved_files = 0

    # Organize each file
    for filename in files:

        source_path = os.path.join(
            folder_path,
            filename
        )

        category = get_category(filename)

        category_folder = os.path.join(
            folder_path,
            category
        )

        os.makedirs(
            category_folder,
            exist_ok=True
        )

        destination_path = os.path.join(
            category_folder,
            filename
        )

        # Avoid duplicate names
        if os.path.exists(destination_path):

            name, extension = os.path.splitext(filename)

            count = 1

            while os.path.exists(destination_path):

                new_filename = f"{name}_{count}{extension}"

                destination_path = os.path.join(
                    category_folder,
                    new_filename
                )

                count += 1

        # Move file
        shutil.move(
            source_path,
            destination_path
        )

        # Save information for Undo
        last_organization.append(
            (
                source_path,
                destination_path
            )
        )

        moved_files += 1
        category_counts[category] += 1

        # Update progress
        if progress_callback:

            progress_callback(
                moved_files,
                total_files
            )

    return moved_files, category_counts


# Undo the last organization
def undo_last_organization():

    global last_organization

    restored_files = 0

    # Reverse the moves
    for original_path, current_path in reversed(last_organization):

        if os.path.exists(current_path):

            # Make sure the original folder exists
            original_folder = os.path.dirname(
                original_path
            )

            os.makedirs(
                original_folder,
                exist_ok=True
            )

            # Avoid overwriting
            destination = original_path

            if os.path.exists(destination):

                name, extension = os.path.splitext(
                    destination
                )

                count = 1

                while os.path.exists(destination):

                    new_filename = f"{name}_{count}{extension}"

                    destination = os.path.join(
                        original_folder,
                        new_filename
                    )

                    count += 1

            shutil.move(
                current_path,
                destination
            )

            restored_files += 1

    last_organization = []

    return restored_files