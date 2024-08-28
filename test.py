import random
input_file = './images_out/labels.txt'
output_file ='./images_out/label_out.txt'
train_file = './images_out/label_train.txt'
test_file = './images_out/label_test.txt'
def check_format(line):
    """Check if a line has the correct format: {image_name}\t{label}\n"""
    parts = line.strip().split('\t')
    if len(parts) != 2 or not parts[0].endswith('.png'):
        return False
    return True

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile.readlines():
        image_name = line.split(" ", 1)[0]
        text = line.split(" ", 1)[1]
        outfile.write(f"{image_name}\t{text}")

print("Tab characters added successfully.")

with open(output_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()
    
valid_lines = []
for line in lines:
    if check_format(line):
        valid_lines.append(line)
    else:
        print(f'Invalid line: {line.strip()}')
        
with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.writelines(valid_lines)
    
with open(output_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()
    random.shuffle(lines)

split_index = int(0.9 * len(lines))
train_lines = lines[:split_index]
test_lines = lines[split_index:]

with open(train_file, 'w', encoding='utf-8') as train_outfile:
    train_outfile.writelines(train_lines)

# Write the test set to label_test.txt
with open(test_file, 'w', encoding='utf-8') as test_outfile:
    test_outfile.writelines(test_lines)
    
print("Tab characters added successfully.")
