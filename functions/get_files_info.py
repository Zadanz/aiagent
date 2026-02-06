import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        work_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
        valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs

        if not os.path.isdir(target_dir):
            raise Exception(f"Error: {directory} is not a directory")
        if not valid_target_dir:
            raise Exception(f"Error: Cannot list {directory} as it is outside the permitted working directory")

        return_string = ""

        for entry in os.listdir(target_dir):
            return_string += (f"    - {entry}: file_size={os.path.getsize(f"{target_dir}/{entry}")} bytes, is_dir={os.path.isdir(f"{target_dir}/{entry}")} \n")
    
        return return_string
    
    except Exception as e:
        print(f"Error getting info of files: {e}")


if __name__ == "__main__":
    get_files_info("calculator")


# Schema for LLM to understand how this function works
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

