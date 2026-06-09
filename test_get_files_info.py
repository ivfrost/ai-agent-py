from functions.get_files_info import get_files_info
working_dir = "calculator"
dirs = [".", "pkg", "/bin", "../"]
for dir in dirs:
  header_name = "current directory" if dir == "." else f"'{dir}' directory"
  print(f"Result for {header_name}:")
  print(get_files_info(working_dir, dir))