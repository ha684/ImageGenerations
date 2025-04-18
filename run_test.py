import argparse
import errno
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import random as rnd
import sys
from multiprocessing import Pool, Manager
from trdg.data_generator import FakeTextDataGenerator
from tqdm import tqdm
import argparse
import os
from PIL import Image
from functools import partial
import errno

import psutil
import time
import multiprocessing
import signal
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate synthetic text data for text recognition.")
    
    # Output directory
    parser.add_argument("--output_dir", type=str, nargs="?", help="The output directory", default="./images_out/")
    
    # Input file
    parser.add_argument("-i", "--input_file", type=str, nargs="?", help="When set, this argument uses a specified text file as source for the text", default="./texts/data.txt")
    
    # Language
    parser.add_argument("-l", "--language", type=str, nargs="?", help="The language to use", default="en")
    
    # Number of images to be created
    parser.add_argument("-c", "--count", type=int, nargs="?", help="The number of images to be created.")
    
    # Random sequences options
    parser.add_argument("-rs", "--random_sequences", action="store_true", help="Use random sequences as the source text for the generation.", default=False)
    parser.add_argument("-let", "--include_letters", action="store_true", help="Define if random sequences should contain letters.", default=False)
    parser.add_argument("-num", "--include_numbers", action="store_true", help="Define if random sequences should contain numbers.", default=False)
    parser.add_argument("-sym", "--include_symbols", action="store_true", help="Define if random sequences should contain symbols.", default=False)
    
    # Text length and randomness
    parser.add_argument("-w", "--length", type=int, nargs="?", help="Define how many words should be included in each generated sample.", default=1)
    parser.add_argument("-r", "--random", action="store_true", help="Define if the produced string will have variable word count.", default=False)
    
    # Image format and size
    parser.add_argument("-f", "--format", type=int, nargs="?", help="Define the height of the produced images if horizontal, else the width", default=64)
    
    # Number of threads to use
    parser.add_argument("-t", "--thread_count", type=int, nargs="?", help="Define the number of threads to use for image generation", default=1)
    
    # File extension
    parser.add_argument("-e", "--extension", type=str, nargs="?", help="Define the extension to save the image with", default="png")
    
    # Skew options
    parser.add_argument("-k", "--skew_angle", type=int, nargs="?", help="Define skewing angle of the generated text.", default=10)
    parser.add_argument("-rk", "--random_skew", action="store_true", help="When set, the skew angle will be randomized.", default=True)
    
    # Blur options
    parser.add_argument("-bl", "--blur", type=int, nargs="?", help="Apply gaussian blur to the resulting sample.", default=3)
    parser.add_argument("-rbl", "--random_blur", action="store_true", help="When set, the blur radius will be randomized.", default=True)
    
    # Background type
    parser.add_argument("-b", "--background", type=int, nargs="?", help="Define what kind of background to use.", default=3)
    
    # Handwriting option
    parser.add_argument("-hw", "--handwritten", action="store_true", help='Define if the data will be "handwritten" by an RNN.', default=False)
    
    # File naming format
    parser.add_argument("-na", "--name_format", type=int, help="Define how the produced files will be named.", default=2)
    
    # Output options
    parser.add_argument("-om", "--output_mask", type=int, help="Define if the generator will return masks for the text", default=0)
    parser.add_argument("-obb", "--output_bboxes", type=int, help="Define if the generator will return bounding boxes for the text.", default=0)
    
    # Distortion options
    parser.add_argument("-d", "--distorsion", type=int, nargs="?", help="Define a distortion applied to the resulting image.", default=3)
    parser.add_argument("-do", "--distorsion_orientation", type=int, nargs="?", help="Define the distortion's orientation.", default=0)
    
    # Image dimensions and alignment
    parser.add_argument("-wd", "--width", type=int, nargs="?", help="Define the width of the resulting image.", default=-1)
    parser.add_argument("-al", "--alignment", type=int, nargs="?", help="Define the alignment of the text in the image.", default=1)
    
    # Orientation
    parser.add_argument("-or", "--orientation", type=int, nargs="?", help="Define the orientation of the text.", default=0)
    
    # Text color
    parser.add_argument("-tc", "--text_color", type=str, nargs="?", help="Define the text's color.", default="#282828")
    
    # Spacing options
    parser.add_argument("-sw", "--space_width", type=float, nargs="?", help="Define the width of the spaces between words.", default=1.0)
    parser.add_argument("-cs", "--character_spacing", type=int, nargs="?", help="Define the width of the spaces between characters.", default=1)
    
    # Margins
    parser.add_argument("-m", "--margins", type=str, nargs="?", help="Define the margins around the text when rendered.", default="5,5,5,5")
    
    # Fit text
    parser.add_argument("-fi", "--fit", action="store_true", help="Apply a tight crop around the rendered text", default=False)
    
    # Font options
    parser.add_argument("-ft", "--font", type=str, nargs="?", help="Define font to be used")
    parser.add_argument("-fd", "--font_dir", type=str, nargs="?", help="Define a font directory to be used", default="./fonts/vi/")
    
    # Image directory
    parser.add_argument("-id", "--image_dir", type=str, nargs="?", help="Define an image directory to use when background is set to image", default="./images/")
    
    # Case options
    parser.add_argument("-ca", "--case", type=str, nargs="?", help="Generate upper or lowercase only.")
    
    # Dictionary file
    parser.add_argument("-dt", "--dict", type=str, nargs="?", help="Define the dictionary to be used")
    
    # Word splitting
    parser.add_argument("-ws", "--word_split", action="store_true", help="Split on words instead of on characters.", default=True)
    
    # Stroke options
    parser.add_argument("-stw", "--stroke_width", type=int, nargs="?", help="Define the width of the strokes", default=0)
    parser.add_argument("-stf", "--stroke_fill", type=str, nargs="?", help="Define the color of the contour of the strokes.", default="#282828")
    
    # Image mode
    parser.add_argument("-im", "--image_mode", type=str, nargs="?", help="Define the image mode to be used.", default="RGB")
    
    return parser.parse_args()

logging.basicConfig(filename='process.log', level=logging.INFO)

terminate_flag = multiprocessing.Event()

def signal_handler(sig, frame):
    logging.info("Termination signal received, stopping processes...")
    terminate_flag.set()

def check_total_ram_usage(threshold):
    total_memory = psutil.virtual_memory().used / (1024 ** 2)
    return total_memory > threshold
import os
import logging
import multiprocessing
from multiprocessing import Event
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from tqdm import tqdm
from PIL import Image
import random as rnd


def stream_input_file(input_file, start_idx=0, batch_size=10000):
    """Generator to stream input file in batches."""
    with open(input_file, 'r', encoding='utf-8') as file:
        batch = []
        for idx, line in enumerate(file):
            if idx < start_idx:
                continue
            if terminate_flag.is_set():
                break
            batch.append(line.strip())
            if len(batch) == batch_size:
                yield idx, batch
                batch = []
        if batch:
            yield idx, batch

def remove_incorrect_srgb_profile(image_path):
    """Remove the incorrect sRGB profile from an image if present."""
    try:
        with Image.open(image_path) as img:
            if "icc_profile" in img.info:
                img.info["icc_profile"] = None
                img.save(image_path)
    except Exception as e:
        logging.error(f"Failed to process {image_path}: {e}")

def process_image(args, fonts, image_id, string):
    """Process a single image: generate, clean, and prepare label."""
    image_path = os.path.join(args.output_dir, f"{image_id}.{args.extension}")
    random_height = rnd.randint(11, 48)
    try:
        FakeTextDataGenerator.generate_from_tuple(
            (image_id, string, rnd.choice(fonts), args.output_dir, random_height,
             args.extension, args.skew_angle, args.random_skew, args.blur, args.random_blur,
             args.background, 0, 0, 0, args.name_format, -1, 1, args.text_color, 0, 1.0,
             args.character_spacing, (0, 0, 0, 0), False, 0, args.word_split, args.image_dir,
             0, args.text_color, args.image_mode, 0)
        )
        remove_incorrect_srgb_profile(image_path)
        return f"{image_id}.{args.extension}\t{string}\n"
    except Exception as e:
        logging.error(f"Error processing image {image_id}: {e}")
        return None

def get_last_image_id(output_dir, default_id=0):
    """Retrieve the last processed image ID."""
    id_file_path = os.path.join(output_dir, "last_image_id.txt")
    if os.path.exists(id_file_path):
        with open(id_file_path, "r", encoding='utf-8') as id_file:
            try:
                return int(id_file.read().strip())
            except ValueError:
                return default_id
    return default_id

def save_last_image_id(output_dir, last_image_id):
    """Save the last processed image ID."""
    id_file_path = os.path.join(output_dir, "last_image_id.txt")
    with open(id_file_path, "w", encoding='utf-8') as id_file:
        id_file.write(str(last_image_id))

def get_last_processed_line(output_dir):
    """Retrieve the last processed line index."""
    line_file_path = os.path.join(output_dir, "last_processed_line.txt")
    if os.path.exists(line_file_path):
        with open(line_file_path, "r", encoding='utf-8') as line_file:
            try:
                return int(line_file.read().strip())
            except ValueError:
                return 0
    return 0

def save_last_processed_line(output_dir, line_idx):
    """Save the last processed line index."""
    line_file_path = os.path.join(output_dir, "last_processed_line.txt")
    with open(line_file_path, "w", encoding='utf-8') as line_file:
        line_file.write(str(line_idx))

def setup_logging(output_dir):
    """Configure logging to capture errors."""
    logging.basicConfig(
        filename=os.path.join(output_dir, 'error.log'),
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def write_labels(output_dir, labels):
    """Write a batch of labels to the labels file."""
    labels_path = os.path.join(output_dir, "labels.txt")
    with open(labels_path, "a", encoding="utf-8") as labels_file:
        labels_file.writelines(labels)

def main():
    args = parse_arguments()
    setup_logging(args.output_dir)
    
    # Preload font paths
    fonts = [os.path.join(args.font_dir, p) for p in os.listdir(args.font_dir) if p.endswith(".ttf")]
    if not fonts:
        logging.error("No .ttf fonts found in the specified font directory.")
        return
    
    image_id = get_last_image_id(args.output_dir, default_id=1)
    start_line_idx = get_last_processed_line(args.output_dir)
    
    cpu_count = multiprocessing.cpu_count()
    
    # Prepare partial function for multiprocessing
    process_image_partial = partial(process_image, args, fonts)
    
    labels_buffer = []
    buffer_size = 1000  # Adjust based on memory and performance
    
    with ProcessPoolExecutor(max_workers=cpu_count) as executor:
        futures = []
        for batch_idx, batch in stream_input_file(args.input_file, start_idx=start_line_idx, batch_size=10000):
            if terminate_flag.is_set():
                break
            
            # Submit all tasks for the current batch
            for idx, string in enumerate(batch):
                current_image_id = image_id + idx
                futures.append(executor.submit(process_image_partial, current_image_id, string))
            
            # Use tqdm for progress visualization
            for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing Batch {batch_idx}"):
                result = future.result()
                if result:
                    labels_buffer.append(result)
                    image_id += 1  # Increment only if processing was successful
                
                # Save labels in buffer to reduce I/O operations
                if len(labels_buffer) >= buffer_size:
                    write_labels(args.output_dir, labels_buffer)
                    labels_buffer = []
            
            # Clear futures for the next batch
            futures = []
            
            # Save progress
            save_last_processed_line(args.output_dir, batch_idx * 10000 + len(batch))
            save_last_image_id(args.output_dir, image_id)
        
        # Write any remaining labels
        if labels_buffer:
            write_labels(args.output_dir, labels_buffer)

if __name__ == "__main__":
    terminate_flag = Event()
    try:
        main()
    except KeyboardInterrupt:
        terminate_flag.set()
