import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_full = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_full, directory))
        valid_target_dir = os.path.commonpath([working_directory_full, target_dir]) == working_directory_full

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files = os.listdir(target_dir)
        result = []
        for file in files:
            file_path = os.path.join(target_dir, file)
            result.append(f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
        return "\n".join(result)
    except Exception as e:
        return f'Error: {str(e)}'
