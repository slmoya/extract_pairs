import os
import re
import argparse
import logging
from tqdm import tqdm
import psutil
import threading
import time
import fileinput

# Compiling the regex patterns outside the function
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
password_regex = re.compile(r'[:,\s](\S+)')

def extract_email_password_pairs(file_paths, output_file_path):
    try:
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            previous_line = ""
            for line in fileinput.input(files=file_paths, openhook=fileinput.hook_encoded("utf-8", "ignore")):
                email_match = email_regex.search(line)
                if email_match:
                    email = email_match.group()
                    password_match = password_regex.search(line[email_match.end():])
                    if password_match:
                        password = password_match.group(1)
                        output_file.write(f"{email}:{password}\n")
                    else:
                        password_match = re.search(r'\S+', previous_line)
                        if password_match:
                            password = password_match.group()
                            output_file.write(f"{email}:{password}\n")
                previous_line = line
    except Exception as e:
        logging.error(f"Error processing files: {e}")

def process_directory(input_dir, output_file_path):
    file_paths = []
    for root, _, filenames in os.walk(input_dir):
        for filename in filenames:
            file_paths.append(os.path.join(root, filename))
    
    with tqdm(total=len(file_paths), desc="Processing files", unit="file") as pbar:
        for file_path in file_paths:
            extract_email_password_pairs([file_path], output_file_path)
            pbar.update(1)

def monitor_memory(interval=5):
    while True:
        mem = psutil.virtual_memory()
        logging.info(f"Memory Usage: {mem.percent}%")
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description='Extract email:password pairs from files in a directory and write to one file.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing files to process.')
    parser.add_argument('output_file', type=str, help='Path to the output file where results will be saved.')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting processing with direct write to {args.output_file}")
    
    memory_thread = threading.Thread(target=monitor_memory, daemon=True)
    memory_thread.start()
    
    try:
        if os.path.exists(args.output_file):
            os.remove(args.output_file)
        
        process_directory(args.input_directory, args.output_file)
        logging.info(f"Consolidated email:password pairs saved to {args.output_file}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info("Processing complete")

if __name__ == '__main__':
    main()
