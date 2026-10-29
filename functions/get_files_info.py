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
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    #else:
    #    return f'Success: "{directory}" is within the working directory'
    #print(target_dir)
    #print(os.listdir(target_dir))
    result = "Result for current directory:\n"
    for item in os.listdir(target_dir):
        item_path = os.path.normpath(os.path.join(target_dir, item))
        #print(item_path)
        result += f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n"
    return result


#print(get_files_info("..", "calculator"))
