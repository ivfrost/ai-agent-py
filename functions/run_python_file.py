import os
import subprocess
from sys import stderr, stdout

schema_run_python_file = {
    "name": "run_python_file",
    "description": "Execute the code of a valid Python file in the Python interpreter",
    "input_schema": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path of the Python file which contents are to be executed, relative to the working directory"
            },
            "args": {
                "type": "array",
                "description": "Optional list of arguments to pass to the Python file when executing it",
                "items": {
                    "type": "string"
                }
            }
        }
    }
}


def run_python_file(work_dir: str, file_path: str, args: list[str] | None = None) -> str:
  try:
    if not work_dir:
      raise ValueError('You need to provide a working directory')

    work_dir_abs = os.path.abspath(work_dir)
    full_path = os.path.normpath(os.path.join(work_dir_abs, file_path))
    valid_path = os.path.commonpath([work_dir_abs, full_path]) == work_dir_abs

    if not valid_path:
      raise ValueError(
          f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(full_path):
      raise ValueError(
          f'Error: "{file_path}" does not exist or is not a regular file')
    if not file_path.endswith('.py'):
      raise ValueError(f'Error: "{file_path}" is not a Python file')

    command = ["python", full_path]
    if args is not None:
      command.extend(args)

    sp_result = subprocess.run(
        command, cwd=work_dir_abs, capture_output=True, text=True, timeout=30)
    result = ''
    if sp_result.returncode != 0:
      result += (f"Process exited with code {sp_result.returncode}")
    if not sp_result.stdout and not sp_result.stderr:
      result += (f"\nNo output produced")
    else:
      result += (f"\nSTDOUT: {sp_result.stdout}")
      result += (f"\nSTDERR: {sp_result.stderr}")
    return result
  except Exception as e:
    if isinstance(e, (ValueError, OSError)):
      return f"Error: executing Python file: {str(e)}"
    else:
      return f"Error: An unexpected error occurred: {str(e)}"
