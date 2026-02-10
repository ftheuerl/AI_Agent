import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

#import os


#def get_files_info(working_directory, directory="."):
#    try:
#        abs_working_dir = os.path.abspath(working_directory)
#        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
#        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
#            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
#        if not os.path.isdir(target_dir):
#            return f'Error: "{directory}" is not a directory'
#        files_info = []
#        for filename in os.listdir(target_dir):
#            filepath = os.path.join(target_dir, filename)
#            is_dir = os.path.isdir(filepath)
#            file_size = os.path.getsize(filepath)
#            files_info.append(
#                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
#            )
#        return "\n".join(files_info)
#    except Exception as e:
#        return f"Error listing files: {e}"

