# email_password_extractor

This script extracts email:password pairs from text files in a directory and writes them to a specified output file. It is designed to handle large datasets efficiently by processing files line by line and leveraging multiprocessing for concurrent processing.

## Features

- Extracts email:password pairs from text files.
- Handles multiple files in nested directories.
- Uses multiprocessing to speed up the processing.
- Monitors memory usage.

## Requirements

- Python 3.6+
- `tqdm` for progress bar
- `psutil` for memory monitoring

## Installation

1. Clone the repository:
```
git clone https://https://github.com/slmoya/email_password_extractor.git
cd email-password-extractor
```

1. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Usage:
```
python3 email_password_extractor.py <input_directory> <output_file>
```

Arguments
- input_directory: Path to the directory containing text files to process.
- output_file: Path to the output file where the extracted email pairs will be saved.

## Example
```
python3 email_password_extractor.py /path/to/input_directory /path/to/output_file.txt

```

File Structure
The script processes files in the specified input directory, including files in nested directories, and extracts email
pairs. The results are written directly to the specified output file.

Logging
The script logs its progress and memory usage. The memory monitoring runs in a separate thread and logs the memory usage every 5 seconds.

Contributing
If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
