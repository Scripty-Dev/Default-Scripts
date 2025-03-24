import json
import os
from datetime import datetime
import platform
import subprocess

if platform.system() == "Windows":
    import win32clipboard as clipboard
    import win32con

documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
HISTORY_FILE = os.path.join(documents_dir, "clipboard_history.json")
MAX_HISTORY_ITEMS = 100  

if not os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    except Exception:
        pass

public_description = "Manage clipboard history and retrieve previously copied items."

def get_clipboard_text():
    if platform.system() == "Windows":
        clipboard.OpenClipboard()
        try:
            if clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
                data = clipboard.GetClipboardData(win32con.CF_TEXT)
                return data.decode('utf-8')
            return ""
        finally:
            clipboard.CloseClipboard()
    
    elif platform.system() == "Darwin": 
        try:
            return subprocess.check_output(
                ['pbpaste'], universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
        except subprocess.CalledProcessError:
            return ""
    
    elif platform.system() == "Linux":
        try:
            return subprocess.check_output(
                ['xclip', '-selection', 'clipboard', '-o'], 
                universal_newlines=True, stderr=subprocess.DEVNULL
            ).strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            try:
                return subprocess.check_output(
                    ['xsel', '-b'], 
                    universal_newlines=True, stderr=subprocess.DEVNULL
                ).strip()
            except (subprocess.SubprocessError, FileNotFoundError):
                return ""
    
    return ""

def set_clipboard_text(text):
    if platform.system() == "Windows":
        clipboard.OpenClipboard()
        try:
            clipboard.EmptyClipboard()
            clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
        finally:
            clipboard.CloseClipboard()
    
    elif platform.system() == "Darwin": 
        try:
            subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
        except subprocess.SubprocessError:
            pass
    
    elif platform.system() == "Linux":
        try:
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'), check=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            try:
                subprocess.run(['xsel', '-ib'], input=text.encode('utf-8'), check=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                pass

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return []
    return []

def save_history(history):
    if not os.path.exists(documents_dir):
        try:
            os.makedirs(documents_dir)
        except Exception:
            pass
    
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def add_to_history(text):
    if not text or text.isspace():
        return
        
    history = load_history()
    
    history = [item for item in history if item["text"] != text]
    
    history.insert(0, {
        "text": text,
        "timestamp": datetime.now().isoformat(),
    })
    
    if len(history) > MAX_HISTORY_ITEMS:
        history = history[:MAX_HISTORY_ITEMS]
        
    save_history(history)

def search_history(query):
    history = load_history()
    if not query:
        return history[:10]  
    
    matches = []
    for item in history:
        if query.lower() in item["text"].lower():
            matches.append(item)
    
    return matches

async def function(args):
    try:
        current_clipboard = get_clipboard_text()
        if current_clipboard:
            add_to_history(current_clipboard)
        
        operation = args.get("operation", "show")
        
        if not args:
            args = {}
            
        elif operation == "show":
            limit = int(args.get("limit", 10))
            history = load_history()
            
            if not history:
                return json.dumps({
                    "message": "No clipboard history found."
                })
                
            recent_items = history[:limit]
            formatted_items = []
            
            for i, item in enumerate(recent_items):
                try:
                    timestamp = datetime.fromisoformat(item["timestamp"])
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, KeyError):
                    time_str = "Unknown time"
                
                text = item["text"]
                if len(text) > 100:
                    text = text[:97] + "..."
                
                formatted_items.append({
                    "index": i, 
                    "text": text,
                    "time": time_str
                })
            
            return json.dumps({
                "message": {
                    "text": f"Showing {len(formatted_items)} clipboard history items",
                    "items": formatted_items
                }
            })
            
        elif operation == "search":
            query = args.get("query", "")
            if not query:
                return json.dumps({
                    "message": "Please provide a search query"
                })
                
            matches = search_history(query)
            
            if not matches:
                return json.dumps({
                    "message": f"No matches found for '{query}'"
                })
                
            formatted_matches = []
            for i, item in enumerate(matches):
                try:
                    timestamp = datetime.fromisoformat(item["timestamp"])
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, KeyError):
                    time_str = "Unknown time"
                
                text = item["text"]
                if len(text) > 100:
                    text = text[:97] + "..."
                
                formatted_matches.append({
                    "index": i,
                    "text": text,
                    "time": time_str
                })
            
            return json.dumps({
                "message": {
                    "text": f"Found {len(formatted_matches)} matches for '{query}'",
                    "items": formatted_matches
                }
            })
            
        elif operation == "restore":
            index = int(args.get("index", 0))
            history = load_history()
            
            if not history:
                return json.dumps({
                    "message": "No clipboard history available"
                })
                
            if index < 0 or index >= len(history):
                return json.dumps({
                    "message": f"Invalid index: {index}. Valid range is 0 to {len(history)-1}"
                })
                
            item = history[index]
            set_clipboard_text(item["text"])
            
            return json.dumps({
                "message": {
                    "text": "Restored clipboard item",
                    "content": item["text"][:100] + ("..." if len(item["text"]) > 100 else "")
                }
            })
            
        elif operation == "clear":
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            return json.dumps({
                "message": "Clipboard history cleared"
            })
            
        else:
            return json.dumps({
                "message": f"Unknown operation: {operation}"
            })
            
    except Exception as e:
        return json.dumps({
            "message": str(e)
        })

object = {
    "name": "clipboard_manager",
    "description": "Manage clipboard history and retrieve previously copied items.",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["show", "search", "restore", "clear"],
                "description": "Operation to perform with clipboard history"
            },
            "query": {
                "type": "string",
                "description": "Search query when using search operation"
            },
            "index": {
                "type": "integer",
                "description": "Index of clipboard item to restore"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of items to show (default: 10)"
            }
        },
        "required": ["operation"]
    }
} 