import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_work_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_work_path, directory))
    except:
        return "Error: os.path call returned error."
    # Will be True or False
    valid_target_dir = os.path.commonpath([abs_work_path, target_dir]) == abs_work_path
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    else:
        return f'Success: "{directory}" is within the working directory'
