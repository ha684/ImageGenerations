import os

def remove_last_n_lines_large_file(file_path, n):
    """Removes the last n lines from a large file without loading the entire file into memory."""
    try:
        temp_file_path = file_path + ".tmp"
        line_count = 0

        # First, count the total number of lines
        with open(file_path, 'r', encoding='utf-8') as file:
            for _ in file:
                line_count += 1

        # Calculate the number of lines to keep
        lines_to_keep = line_count - n
        if lines_to_keep <= 0:
            raise ValueError("The file has fewer lines than the number to be removed.")

        # Now, write the lines to keep into a temporary file
        with open(file_path, 'r', encoding='utf-8') as file, open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            for idx, line in enumerate(file):
                if idx < lines_to_keep:
                    temp_file.write(line)

        # Replace the original file with the temp file
        os.replace(temp_file_path, file_path)
        print(f"Successfully removed the last {n} lines from {file_path}.")
    except Exception as e:
        print(f"An error occurred while removing lines: {e}")
remove_last_n_lines_large_file(r'D:\Workspace\python_code\ImageGeneration\images_out\labels.txt',2900)