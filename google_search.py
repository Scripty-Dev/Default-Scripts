import json

public_description = "Search Google for information"

async def function(args):
    query = args.get("query")
    response = call_serper(query)
    return json.dumps({
        "success": True,
        "message": response
    })

object = {
    "name": "google_search",
    "description": "Search Google for information",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search for"
            }
        },
        "required": ["query"]
    }
}   
