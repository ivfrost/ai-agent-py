from functions.run_python_file import run_python_file


work_dir = "calculator"
commands = [['main.py'], ['main.py', '3 + 5'], ['tests.py'], ['../main.py'], ['nonexistent.py'], ['lorem.txt']]

for cmd in commands:
  result = run_python_file(work_dir, cmd[0], cmd[1:] if len(cmd) > 1 else None)
  print(f"{result}")