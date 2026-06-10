import os

schema_write_file = {
    "name": "write_file",
    "description": "Write into any file present under the working directory",
    "input_schema": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path of the file which the content will be written into, relative to the working directory"
            },
            "content": {
                "type": "string",
                "description": "Content to write into the file specified in file_path argument"
            }
        }
    }
}


def write_file(work_dir: str, file_path: str, content: str):
  try:
    if not work_dir:
      raise ValueError('You need to provide a working directory')

    work_dir_abs = os.path.abspath(work_dir)
    full_path = os.path.normpath(os.path.join(work_dir_abs, file_path))
    valid_path = os.path.commonpath([work_dir_abs, full_path]) == work_dir_abs

    if not valid_path:
      raise ValueError(
          f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    if os.path.isdir(full_path):
      raise ValueError(
          f'Error: Cannot write to "{file_path}" as it is a directory')

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
      char_count = f.write(content)
      return (f'Successfully wrote to "{file_path}" ({char_count} characters written)')
  except Exception as e:
    if isinstance(e, (ValueError, OSError)):
      return f"Error: {str(e)}"
    else:
      return f"Error: An unexpected error occurred: {str(e)}"
