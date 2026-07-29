import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_full = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_full, file_path))
        valid_target_file = os.path.commonpath([working_directory_full, target_file]) == working_directory_full

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_directory_full, capture_output=True, text=True, timeout=30)

        result = ""
        if completed_process.returncode != 0:
            result += "Process exited with code {completed_process.returncode}\n"
        if not completed_process.stdout and not completed_process.stderr:
            result += "No output produced.\n"
        if completed_process.stdout:
            result += f"STDOUT:\n{completed_process.stdout}\n"
        if completed_process.stderr:
            result += f"STDERR:\n{completed_process.stderr}\n"
        return result

    except Exception as e:
        return f'Error: executing Python file: {str(e)}'