from config import MAX_CHARS
from functions.get_file_content import get_file_content

work_dir = 'calculator'
files = ['lorem.txt', 'main.py', 'pkg/does_not_exist.py', 'pkg/calculator.py', '/bin/cat']

for file in files:
  response = get_file_content(work_dir, file)
  if response.startswith("Error: "):
    print(response)
    continue
  if len(response) > MAX_CHARS:
    print(f"{file} length: {len(response)}")
    print(f"{file} truncated: {'truncated' in response}")
  else:
    print(response)