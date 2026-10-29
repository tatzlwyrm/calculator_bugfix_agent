import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    # First, validate directory permission.
    try:
        abs_work_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_work_path, file_path))
    except Exception as e:
        return f"Error: Error at os.path call. {e}"
    #print(target_path)
    valid_target_path = os.path.commonpath([abs_work_path, target_path]) == abs_work_path
    if not valid_target_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if target_path.split(".")[-1] != "py":
        return f'Error: "{file_path}" is not a Python file'
    # Perform purpose of function.
    try:
        command = ["python", target_path]
        if args != None:
            command.extend(args)
        process_result = subprocess.run(command, cwd=os.path.dirname(target_path), text=True, capture_output=True, timeout=30) # CompletedProcess object.
        process_report = ""
        if process_result.returncode != 0:
            process_report += f"Process exited with code {process_result.returncode}. "
        if process_result.stdout == None and process_result.stderr == None:
            process_report += "No output produced. "
        else:
            process_report += f"STDOUT: {process_result.stdout} "
            process_report += f"STDERR: {process_result.stderr} "
        return process_report
    except Exception as e:
        return f"Error: executing Python file {e}"
