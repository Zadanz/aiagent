import os, subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_file_path = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

        if not valid_file_path:
            raise Exception(f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory")

        if not os.path.isfile(target_file):
            raise Exception(f"Error: \"{file_path}\" does not exist or is not a regular file")

        if not target_file.endswith('.py'):
            raise Exception(f"Error: \"{file_path}\" is not a Python file")

        command = ["python", target_file]

        if args != None:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, cwd=work_dir_abs, timeout=30, check=True, text=True)

        process_out = process.stdout
        process_err = process.stderr
        process_retcode = process.returncode

        output_string = ""

        if process_retcode != 0:
            output_string += f"Process exited with code {process_retcode}\n"

        if process_out == None and process_err == None:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {process_out}\n"
            output_string += f"STDERR: {process_err}\n"

        return output_string

    except Exception as e:
        return(f"Error: executing Python file: {e}")

# Schema for LLM to understand how this function works
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file at the given file path with arguments that can also be passed in.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to python file to run, relative to working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments that will be passed into the python file being run, optional as not all functions need arguments (default is no arguments)",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument being passed into the called python file"
                ),
            ),
        },
    ),
)
