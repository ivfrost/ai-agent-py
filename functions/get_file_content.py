import os
from config import MAX_CHARS

schema_get_file_content = {
    "name": "get_file_content",
    "description": "Display the contents of the specified file. If the output character's length limit of MAX_CHARS is surpassed, the content is truncated and the user is informed about it",
    "input_schema": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path of the file which contents are to be displayed, relative to the working directory"
            }
        }
    }
}


def get_file_content(work_dir: str, file_path: str) -> str:
  try:
    if not work_dir:
      raise ValueError("You need to provide a working directory")
    work_dir_abs = os.path.abspath(work_dir)
    full_path = os.path.normpath(os.path.join(work_dir_abs, file_path))
    valid_path = os.path.commonpath([work_dir_abs, full_path]) == work_dir_abs

    if not valid_path:
      raise ValueError(
          f'Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(full_path):
      raise ValueError(
          f'File not found or is not a regular file: "{file_path}"')

    with open(full_path, "r") as f:
      response = f.read(MAX_CHARS)
      if f.read(1):
        response += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
      return response

  except Exception as e:
    if isinstance(e, (ValueError, FileNotFoundError)):
      return (f"Error: {str(e)}")
    else:
      return (f"Error: Unexpected error ocurred")
