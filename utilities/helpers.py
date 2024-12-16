import re
import os
import logging
from dotenv import load_dotenv
from utilities.env_manager import combine_env_files, list_env_variables

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_env_files_path():
    project_root = os.getcwd()
    return project_root


def get_base_config_file_path() -> str:
    return os.path.join(get_env_files_path(), '.env')


def to_pascal_case(text):
    # Split the text by any non-alphanumeric character
    words = re.split(r'\W+|_', text)
    # Capitalize the first letter of each word and join them together
    return ''.join(word.capitalize() for word in words if word)


def load_combined_env_files(dotenv_file):
    dotenv_file_full_path = os.path.join(get_env_files_path(), dotenv_file)
    logger.info(f"Loading .env file from: {dotenv_file}")
    combined_env_stream = combine_env_files(files=[get_base_config_file_path(), dotenv_file_full_path])
    load_dotenv(dotenv_file_full_path, encoding='utf-8')

def get_image_folder_path():
    return os.getcwd()

def list_files_in_directory(directory_path):
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return files


class LoggingMeta(type):
    def __new__(cls, name, bases, class_dict):
        def log_function_call(func):
            def wrapper(*args, **kwargs):
                logger.info(f"Calling function {func.__name__} with args: {args} and kwargs: {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"Function {func.__name__} returned: {result}")
                return result

            return wrapper

        for attr_name, attr_value in class_dict.items():
            if callable(attr_value):
                class_dict[attr_name] = log_function_call(attr_value)
        return super().__new__(cls, name, bases, class_dict)

