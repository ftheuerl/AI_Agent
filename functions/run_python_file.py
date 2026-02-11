import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
#command to run subprocess
        command = ["python", abs_file_path]
        if args != None:
            command.extend(args)
        variable = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=abs_working_dir)
        output = []
        if variable.returncode != 0:
            output.append(f"Process exited with code {variable.returncode}")
        if not variable.stdout and not variable.stderr:
            output.append("No output produced")
        if variable.stdout:
            output.append(f"STDOUT: {variable.stdout}")
        if variable.stderr:
            output.append(f"STDERR: {variable.stderr}")
        result = "\n".join(output)
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of command-line arguments to pass the Python script when running it",
            ),

        },
        required=["file_path"],
    ),
)
