import os
import re
import sys
import logging
import json
from collections import namedtuple

# Define a named tuple to hold regex match and replacement patterns
RegexPattern = namedtuple('RegexPattern', ['search', 'replace'])

def generate_file_paths(directory, file_extension=None):
    """
    Generate file paths recursively within a directory.

    Args:
        directory (str): The directory to search for files.
        file_extension (str): Optional file extension to filter files.

    Yields:
        str: A file path found within the directory and its subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file_extension is None or file.endswith(file_extension):
                file_path = os.path.join(root, file)
                yield file_path

def perform_regex_replacement(file_path, regex_patterns):
    """
    Perform regex replacement on the content of a file using provided regex patterns.

    Args:
        file_path (str): The path to the file to perform replacement on.
        regex_patterns (list of RegexPattern): A list of RegexPattern objects containing
            search and replace regex patterns.

    Returns:
        str: The content of the file after replacement.
    """
    with open(file_path, 'r') as file:
        content = file.read()
        for pattern in regex_patterns:
            content = re.sub(pattern.search, pattern.replace, content)
    return content

def process_file(file_path, regex_patterns):
    """
    Process a single file by performing regex replacement on its content.

    Args:
        file_path (str): The path to the file to be processed.
        regex_patterns (list of RegexPattern): A list of RegexPattern objects containing
            search and replace regex patterns.
    """
    try:
        logger.info(f"Processing file: {file_path} (File type: {os.path.splitext(file_path)[1]})")
        new_content = perform_regex_replacement(file_path, regex_patterns)
        with open(file_path, 'w') as file:
            file.write(new_content)
    except Exception as e:
        logger.error(f"Error processing file '{file_path}': {e}")


def create_boilerplate_config(config_file_path):
    """
    Create a boilerplate config file.

    Args:
        config_file_path (str): The path to the config file.
    """
    default_config = {
        "directory_path": "/path/to/your/directory",
        "file_extension": ".txt",
        "regex_patterns": [
            {
                "search": "((.|[\\r\\n])+?)(---[\\r\\n]+tags:.*[\\r\\n]+---)",
                "replace": "\\3\\r\\n\\1"
            }
        ]
    }
    with open(config_file_path, 'w') as f:
        json.dump(default_config, f, indent=4)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Check if config file path is provided via command-line argument
    if len(sys.argv) > 1:
        config_file_path = sys.argv[1]
        # Convert to absolute path if it's a relative path
        if not os.path.isabs(config_file_path):
            config_file_path = os.path.abspath(config_file_path)
    else:
        config_file_path = 'config.json'  # Default config file path

    # Check if config file exists
    if not os.path.exists(config_file_path):
        create_boilerplate = input(f"Config file '{config_file_path}' not found. Would you like to create a boilerplate config file? (yes/no): ")
        if create_boilerplate.lower() == 'yes':
            custom_config_path = input("Enter the path where you would like to save the config file (press Enter to save in the current directory): ")
            if custom_config_path:
                config_file_path = os.path.abspath(custom_config_path)
            create_boilerplate_config(config_file_path)
            logger.info(f"Boilerplate config file created at '{config_file_path}'")
        else:
            logger.error("Config file not found. Please provide a valid config file or create a boilerplate config file.")
            sys.exit(1)

    logger.info(f"Using config file: {config_file_path}")

    # Load configuration from JSON file
    try:
        with open(config_file_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file '{config_file_path}' not found.")
        sys.exit(1)

    logger.info(f"Performing replacement in directory: {config.get('directory_path')}")
    logger.info(f"Performing replacement for all '{config.get('file_extension')}' files")
    
    # Extract configuration values
    directory_path = config.get('directory_path')
    file_extension = config.get('file_extension')
    regex_patterns = [RegexPattern(**pattern) for pattern in config.get('regex_patterns', [])]

    # Generator for all files contained in the given directory
    file_paths_generator = generate_file_paths(directory_path, file_extension)

    if file_paths_generator:
        for file_path in file_paths_generator:
            process_file(file_path, regex_patterns)

        logger.info("Regex replacement completed.")
    else:
        logger.info("No files found to process.")  # No files to process
