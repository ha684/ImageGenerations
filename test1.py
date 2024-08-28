# Define the input and output file paths
input_file_path = r'D:\Workspace\python_code\ImageGeneration\images_out\labels.txt'
output_file_path = r'D:\Workspace\python_code\ImageGeneration\images_out\labels1.txt'

# Open the input file for reading and output file for writing
with open(input_file_path, 'r', encoding='utf-8', errors='replace') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        line = line.strip()
        parts = line.split('\t')

        if len(parts) > 2:
            corrected_line = parts[0] + '\t' + ' '.join(parts[1:])
        elif len(parts) == 2:
            corrected_line = line
        else:
            continue
        
        outfile.write(corrected_line + '\n')

import random
print("Processing complete. Check the output file for the corrected data.")

# Shuffle and split the lines
with open(output_file_path, 'r', encoding='utf-8', errors='replace') as infile:
    lines = infile.readlines()
    random.shuffle(lines)

split_index = int(0.9 * len(lines))
train_lines = lines[:split_index]
test_lines = lines[split_index:]

# Write the train set to label_train.txt
with open(r'D:\Workspace\python_code\ImageGeneration\images_out\label_train.txt', 'w', encoding='utf-8') as train_outfile:
    train_outfile.writelines(train_lines)

# Write the test set to label_test.txt
with open(r'D:\Workspace\python_code\ImageGeneration\images_out\label_test.txt', 'w', encoding='utf-8') as test_outfile:
    test_outfile.writelines(test_lines)

print("Tab characters added successfully.")
