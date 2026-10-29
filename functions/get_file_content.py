import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    # First, validate directory permission.
    try:
        abs_work_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_work_path, file_path))
    except:
        return "Error: os.path call returned error."
    #print(target_dir)
    valid_target_dir = os.path.commonpath([abs_work_path, target_dir]) == abs_work_path
    if not valid_target_dir:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" is not a file'
    # Perform purpose of function.
    with open(target_dir, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return file_content_string
