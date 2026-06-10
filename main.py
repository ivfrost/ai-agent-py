import os, argparse, time
from dotenv import load_dotenv
from anthropic import Anthropic
from prompts import system_prompt
from config import MAX_ITERATIONS, MAX_TOKENS, TEMPERATURE
from use_tool import available_tools, use_tool
load_dotenv()

def generate_content(client, messages):
    config = {
        "model": "claude-haiku-4-5",
        "max_tokens": MAX_TOKENS or 1024,
        "system": system_prompt,
        "temperature": TEMPERATURE or 0,
        "tools": available_tools,
    }
    return client.messages.create(**config, messages=messages)
def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--work-dir", type=str, default=os.getcwd(), help="Define the working directory where the agent can read/write files. Default is the current directory.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    api_key = os.environ.get("CLAUDE_API_KEY")
    messages: list[dict] = [{"role": "user", "content": args.user_prompt}]

    if not api_key:
        raise RuntimeError("CLAUDE_API_KEY is not set")
    
    client = Anthropic(api_key=api_key)

    for _ in range(MAX_ITERATIONS or 20):
        response = generate_content(client, messages)
        if response.content:
            messages.append({"role": "assistant", "content": response.content})
        usage = response.usage
        if not usage:
            raise RuntimeError("API request failed. Try again later")
        
        promptTokens = usage.input_tokens
        responseTokens = usage.output_tokens
        if args.verbose:
            print("Prompt tokens: " + str(promptTokens)) 
            print("Response tokens: " + str(responseTokens)) 
            print()
            print("User prompt: " + str(args.user_prompt))
            print()
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if tool_uses:
            tool_results = []
            for tool in tool_uses:
                result = use_tool(args.work_dir, tool, args.verbose)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool.id,
                    "content": result
                })
                if args.verbose:
                    print(f"-> {result}")
            messages.append({"role": "user", "content": tool_results})
        else:
            print(next(b.text for b in response.content if b.type == "text"))
            break
    else:
        print(f"The agent reached the limit of iterations without producing a final response")
        exit(1)


if __name__ == "__main__":
    main()
