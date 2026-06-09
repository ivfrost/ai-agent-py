import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        }
    )
)


def get_files_info(work_dir: str, directory: str = ".") -> str:
    try:
        if not work_dir:
            raise ValueError("You need to provide a working directory")

        work_dir_abs = os.path.abspath(work_dir)
        full_path = os.path.normpath(os.path.join(work_dir_abs, directory))
        if not os.path.isdir(full_path):
            raise ValueError(f'Cannot list "{directory}" as it is not a valid directory')
        valid_path = os.path.commonpath([work_dir_abs, full_path]) == work_dir_abs

        if not valid_path:
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')

        response = ''

        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            item_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            response += (f'  - {item}: file_size={item_size} bytes, is_dir={is_directory}\n')
        
        
        return response
    except Exception as e:
        if isinstance(e, (ValueError, FileNotFoundError)):
            return (f"    Error: {str(e)}")
        else:            
            return (f"    Error: Unexpected error ocurred")
