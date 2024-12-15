"""
Author: Ahmed Saad - (lxth0rz)
Description: Script to read and combine multiple .env files, removing duplicates.
Creation Date: 2024-05-29
"""

import os
import argparse
from io import StringIO
from typing import Dict, List


def read_env_file(file_path: str) -> Dict[str, str]:
    """
    Read a .env file and return its contents as a dictionary.

    Args:
        file_path (str): Path to the .env file.

    Returns:
        Dict[str, str]: Dictionary with key-value pairs from the .env file.
    """
    env_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                env_dict[key] = value
    return env_dict


def combine_env_files(**kwargs) -> StringIO:
    """
    Combine multiple .env files, removing duplicates, then return the result as StringIO.

    Args:
        kwargs: Arbitrary keyword arguments. Expects 'files' as a list of file paths.

    Returns:
        StringIO: StringIO object with combined .env content.
    """
    file_paths = kwargs.get('files', [])

    combined_env = {}

    for file_path in file_paths:
        env_dict = read_env_file(file_path)
        combined_env.update(env_dict)  # Later files will overwrite earlier ones

    return StringIO('\n'.join([f'{key}={value}' for key, value in combined_env.items()]))


def list_env_variables() -> List[str]:
    """
    List all environment variables after loading .env files.

    Returns:
        List[str]: List of environment variable names.
    """
    return list(os.environ.keys())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage and combine .env files.')
    parser.add_argument('--files', nargs='+', required=True, help='Paths to the .env files to be combined')
    parser.add_argument('--output', default='combined.env', help='Path to the output .env file')

    args = parser.parse_args()

    combined_env_content = combine_env_files(files=args.files)

    with open(args.output, 'w') as output_file:
        output_file.write(combined_env_content.getvalue())

    print(f'Combined .env file saved to {args.output}')