import requests
import json
import sys
import asyncio

public_description = "Execute Google searches with structured results including knowledge graphs, answer boxes, and organic listings."

async def search_with_serper(query):
    """
    Uses the Serper API through a server route to get Google search results in a clean JSON format.
    """

    try:
        # Define the endpoint where the server is exposing the Serper search API
        url = "https://scripty.me/api/assistant/serper"

        # Prepare the payload with the query
        payload = {
            "query": query
        }

        # Make the request to your server API (without needing API keys here)
        response = requests.post(url, json=payload)

        # Ensure the request was successful
        if response.status_code != 200:
            return f"Error: Received a {response.status_code} from the server."

        # Parse the JSON response
        result = response.json()

        search_results = []

        # Extract knowledge graph information if available
        if "knowledgeGraph" in result:
            kg = result["knowledgeGraph"]
            search_results.append({
                'type': 'knowledge_graph',
                'title': kg.get('title', ''),
                'description': kg.get('description', ''),
                'source': 'Google Knowledge Graph',
                'url': kg.get('url', '')
            })

        # Extract answer box information if available
        if "answerBox" in result:
            answer_box = result["answerBox"]
            search_results.append({
                'type': 'answer_box',
                'title': answer_box.get('title', ''),
                'answer': answer_box.get('answer', ''),
                'snippet': answer_box.get('snippet', ''),
                'source': answer_box.get('source', 'Google'),
                'url': answer_box.get('link', '')
            })

        # Extract top organic results
        if "organic" in result:
            for index, item in enumerate(result["organic"][:3]):  # Get top 3 organic results
                search_results.append({
                    'type': 'organic',
                    'position': index + 1,
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'source': item.get('source', ''),
                    'url': item.get('link', '')
                })

        return search_results

    except Exception as e:
        return f"Error: {str(e)}"


async def function(args):
    try:
        search_query = args.get('query')
        if not search_query:
            return json.dumps({"error": "No search query provided"})

        results = {
            "message": f"Search results for: {search_query}",
            "results": []
        }

        search_results = await search_with_serper(search_query)
        if isinstance(search_results, list):
            results["results"] = search_results
        else:
            results["error"] = search_results

        return json.dumps(results)

    except Exception as e:
        return json.dumps({"error": str(e)})

# Object for performing a search operation
object = {
    "name": "searcher",
    "description": "Performs a search query using the Serper API to get Google search results",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query to execute"
            }
        },
        "required": ["query"]
    }
}
