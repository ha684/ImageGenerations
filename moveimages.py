def combine_image_folders(source_folders, destination_folder, move_files=False):
    """
    Combine images from multiple source folders into a single destination folder.

    Parameters:
    - source_folders (list of str): List of paths to source folders.
    - destination_folder (str): Path to the destination folder.
    - move_files (bool): If True, move files instead of copying. Default is False.
    """
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    for folder in source_folders:
        # List all files in the source folder
        for file_name in tqdm(os.listdir(folder), desc=f"Processing {folder}"):
            source_file = os.path.join(folder, file_name)
            destination_file = os.path.join(destination_folder, file_name)
            
            if os.path.isfile(source_file):  # Only handle files
                # If move_files is True, move the file; otherwise, copy it
                if move_files:
                    shutil.move(source_file, destination_file)
                else:
                    shutil.copy2(source_file, destination_file)

    print(f"Images have been {'moved' if move_files else 'copied'} to {destination_folder}")

# Example usage
source_folders = [
    "/path/to/source/folder1",
    "/path/to/source/folder2",
    "/path/to/source/folder3"
]

destination_folder = "/path/to/destination/folder"

combine_image_folders(source_folders, destination_folder, move_files=False)
