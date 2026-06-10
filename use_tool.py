from anthropic.types import ToolUseBlock
from functions import *
from collections.abc import Callable

available_tools = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
    schema_get_web_search,
    schema_get_web_answer,
    schema_get_web_content,
    schema_get_user_meta
]

tool_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_web_search": get_web_search,
    "get_web_answer": get_web_answer,
    "get_web_content": get_web_content,
    "get_user_meta": get_user_meta
}

def use_tool(work_dir: str, tool_use: ToolUseBlock, verbose: bool = False) -> str:
    if verbose:
        print(f"Calling function: {tool_use.name}({tool_use.input})")
    else:
        print(f"Calling function: {tool_use.name}")
    
    tool_name = tool_use.name or ""
    
    if tool_name not in tool_map:
        return f"Unknown tool: {tool_name}"
    
    FILE_TOOLS = {"get_file_content", "get_files_info", "write_file", "run_python_file"}

    args = dict(tool_use.input) if tool_use.input else {}
    if tool_name not in FILE_TOOLS:
        args.pop("work_dir", None)
    return tool_map[tool_name](**args)
