import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # First, validate directory permission.
    #print(working_directory)
    #print(file_path)
    #print(content[0:10])
    try:
        abs_work_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_work_path, file_path))
    except Exception as e:
        return f"Error: Error at os.path call. {e}"
    #print(target_path)
    valid_target_path = os.path.commonpath([abs_work_path, target_path]) == abs_work_path
    if not valid_target_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    # Perform purpose of function.
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to file.",
        "parameters": {
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to file. ",
                },
            },
        },
    },
}
