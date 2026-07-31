import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a specified file relative to the working directory, returning the content as a string. If the file exceeds MAX_CHARS, it will be truncated.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_full = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_full, file_path))
        valid_target_file = os.path.commonpath([working_directory_full, target_file]) == working_directory_full

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'