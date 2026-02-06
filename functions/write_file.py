import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):

    try:
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_file_path = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

        if not valid_file_path:
            raise Exception(f"Error: Cannot write to {target_file} as it is outside the permitted working directory")

        if os.path.isdir(target_file):
            raise Exception(f"Error: Cannot write to {target_file} as it is a directory")

        print(f"Working directory: {working_directory}, File path: {file_path}")

        os.makedirs(os.path.dirname(target_file),exist_ok=True)

        with open(target_file, 'w') as f:
            f.write(content)
            return(f"Successfully wrote to \"{target_file}\" ({len(content)} characters written)")
    except Exception as e:
        return (f"Error: Error writing to file {target_file}: {e}")


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file. If that file doesn't exist, it is created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file, or directory an name of file that will be created, where the content will be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file.",
            ),
        },
    ),
)