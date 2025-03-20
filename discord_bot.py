import json
import os
import aiohttp
import asyncio
from pathlib import Path

public_description = "Manage Discord token and handle message operations (fetch and send)"

# Constants
TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".discord_token.json")
API_BASE = "https://discord.com/api/v10"

async def save_token(token):
    """Save Discord token to file"""
    try:
        data = {"token": token}
        with open(TOKEN_FILE, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        return False

async def get_token():
    """Retrieve token from file"""
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                return data.get("token")
        return None
    except Exception:
        return None

async def validate_token(token):
    """Validate Discord token by making a test API call"""
    headers = {"Authorization": f"Bot {token}" if token.startswith("Bot ") else token}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE}/users/@me", headers=headers) as resp:
                if resp.status == 200:
                    return True
                return False
    except Exception:
        return False

async def fetch_messages(token, channel_id, limit=50):
    """Fetch messages from a channel"""
    headers = {"Authorization": f"Bot {token}" if token.startswith("Bot ") else token}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_BASE}/channels/{channel_id}/messages?limit={limit}", headers=headers) as resp:
                if resp.status == 200:
                    messages = await resp.json()
                    # Format messages to simpler format with just name and content
                    simplified_messages = [
                        {
                            "name": msg["author"].get("global_name", msg["author"]["username"]),
                            "content": msg["content"],
                            "timestamp": msg["timestamp"],
                            "has_attachments": len(msg.get("attachments", [])) > 0
                        }
                        for msg in messages
                    ]
                    return simplified_messages
                return None
    except Exception as e:
        return None

async def send_message(token, channel_id, content):
    """Send a message to a channel"""
    headers = {
        "Authorization": f"Bot {token}" if token.startswith("Bot ") else token,
        "Content-Type": "application/json"
    }
    payload = {"content": content}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_BASE}/channels/{channel_id}/messages", 
                                   headers=headers, 
                                   json=payload) as resp:
                if resp.status in (200, 201):
                    return await resp.json()
                return None
    except Exception as e:
        return None

async def function(args):
    try:
        action = args.get("action")
        token = args.get("token")
        channel_id = args.get("channel_id")
        content = args.get("content")
        message_limit = int(args.get("limit", 50))
        
        # Automatically save token if provided
        if token:
            await save_token(token)
        else:
            # Try to load from file
            token = await get_token()
            if not token:
                return json.dumps({
                    "success": False,
                    "error": "No token provided or saved"
                })
        
        # Validate token
        if action == "validate":
            is_valid = await validate_token(token)
            return json.dumps({
                "success": True,
                "valid": is_valid
            })
        
        # Fetch messages
        if action == "fetch":
            if not channel_id:
                return json.dumps({
                    "success": False,
                    "error": "Channel ID is required"
                })
                
            messages = await fetch_messages(token, channel_id, message_limit)
            if messages is None:
                return json.dumps({
                    "success": False,
                    "error": "Failed to fetch messages"
                })
                
            return json.dumps({
                "success": True,
                "message": messages
            })
        
        # Send message
        if action == "send":
            if not channel_id:
                return json.dumps({
                    "success": False,
                    "error": "Channel ID is required"
                })
                
            if not content:
                return json.dumps({
                    "success": False,
                    "error": "Message content is required"
                })
                
            result = await send_message(token, channel_id, content)
            if result is None:
                return json.dumps({
                    "success": False,
                    "error": "Failed to send message"
                })
                
            return json.dumps({
                "success": True,
                "message": "Message sent successfully",
                "data": result
            })
            
        return json.dumps({
            "success": False,
            "error": "Invalid action"
        })
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

object = {
    "name": "discord_bot",
    "description": "Manage Discord token and handle message operations (fetch and send)",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["validate", "fetch", "send"],
                "description": "Action to perform with Discord"
            },
            "token": {
                "type": "string",
                "description": "Discord token (optional if previously saved)"
            },
            "channel_id": {
                "type": "string",
                "description": "Discord channel ID for message operations"
            },
            "content": {
                "type": "string",
                "description": "Content for sending messages"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of messages to fetch (default: 50)"
            }
        },
        "required": ["action"]
    }
} 