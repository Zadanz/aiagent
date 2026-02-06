import os
from config import MAX_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    try:        
        work_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_abs, file_path))
        valid_file_path = os.path.commonpath([work_dir_abs, target_file]) == work_dir_abs

        if not valid_file_path:
            raise Exception(f"Error: Cannot read {file_path} as it is outside the permitted working directory")

        if not os.path.isfile(target_file):
            raise Exception(f"Error: {file_path} is not a file")

        working_file = open(target_file)
        content = working_file.read(MAX_CHARS)
        if working_file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        print(e)


# Schema for LLM to understand how this function works
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns the content of a file, as a string. Content is truncated at {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to read content from, relative to the working directory",
            ),
        },
    ),
)