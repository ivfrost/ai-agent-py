import urllib.request
import json

schema_get_user_meta = {
    "name": "get_user_meta",
    "description": "Fetch metadata about the user, such as IP address, location, timezone and ISP. Use this information to provide more personalized and context-aware responses, or to infer location-based information when relevant.",
    "input_schema": {
        "type": "object",
        "properties": {}
    }
}

def get_user_meta() -> str:
    try:
        with urllib.request.urlopen("https://ipinfo.io/json") as url:
            data = json.loads(url.read().decode())
            return (
                f"IP: {data.get('ip')}\n"
                f"Location: {data.get('city')}, {data.get('region')}, {data.get('country')}\n"
                f"Timezone: {data.get('timezone')}\n"
                f"Org: {data.get('org')}"
            )
    except Exception as e:
        return "Error: Unable to fetch user metadata"