from anthropic.types import ToolUseBlock
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions import get_file_content, get_files_info, write_file, run_python_file
from collections.abc import Callable

available_tools = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]

tool_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def use_tool(tool_use: ToolUseBlock, verbose: bool = False) -> str:
    if verbose:
        print(f"Calling function: {tool_use.name}({tool_use.input})")
    else:
        print(f" - Calling function: {tool_use.name}")
    
    tool_name = tool_use.name or ""
    
    if tool_name not in tool_map:
        return f"Unknown tool: {tool_name}"
    
    args = dict(tool_use.input) if tool_use.input else {}
    args["work_dir"] = "./calculator"
    
    return tool_map[tool_name](**args)
