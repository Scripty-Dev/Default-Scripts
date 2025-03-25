from pathlib import Path
import platform
import json
import os
import glob
import shutil
import datetime

public_description = "Handle file operations with smart path resolution."
PLATFORM = platform.system().lower()

async def function(args):
    try:
        operation = args.get("operation")
        source = args.get("source", "")
        destination = args.get("destination", "")
        filename = args.get("filename", "")
        content = args.get("content", "")
        pattern = args.get("pattern", "*")

        if source:
            if source.startswith('~'):
                source = os.path.join(os.path.expanduser('~'), source[2:] if source.startswith('~/') or source.startswith('~\\') else source[1:])
            source = os.path.normpath(source)
            
        if destination:
            if destination.startswith('~'):
                destination = os.path.join(os.path.expanduser('~'), destination[2:] if destination.startswith('~/') or destination.startswith('~\\') else destination[1:])
            destination = os.path.normpath(destination)
        
        # Operation-specific validations
        if operation in ["move", "copy", "latest", "read", "file_info", "search"]:
            if not source or not os.path.exists(source):
                return json.dumps({"error": f"Source not found: {source}"})
                
        if operation in ["move", "copy", "write", "create_directory"]:
            if not destination:
                return json.dumps({"error": f"Destination required for {operation}"})
            
            # Create parent directories if they don't exist for certain operations
            if operation in ["write", "create_directory"]:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                
        # Handle different operations
        if operation == "move":
            if filename:
                matches = list(Path(source).glob(f"{filename}*"))
                if not matches:
                    return json.dumps({"error": f"No file matching '{filename}' found"})
                
                src_file = matches[0]
                dst_file = Path(destination) / src_file.name
                
                try:
                    if not src_file.is_file():
                        return json.dumps({"error": "Source is not a file"})
                    
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    os.replace(str(src_file), str(dst_file))
                    
                    if not dst_file.exists():
                        return json.dumps({"error": "Move operation failed"})
                        
                except PermissionError:
                    return json.dumps({"error": "Permission denied"})
                except Exception as e:
                    return json.dumps({"error": f"Move failed: {str(e)}"})
            else:
                return json.dumps({"error": "Filename required for move operation"})

        elif operation == "latest":
            try:
                files = [(f, os.path.getmtime(f)) for f in Path(source).iterdir() if f.is_file()]
                if not files:
                    return json.dumps({"error": f"No files found in {source}"})
                
                latest = max(files, key=lambda x: x[1])[0]
                dst_file = Path(destination) / latest.name
                
                os.replace(str(latest), str(dst_file))
                
                if not dst_file.exists():
                    return json.dumps({"error": "Move operation failed"})
                    
            except Exception as e:
                return json.dumps({"error": f"Latest operation failed: {str(e)}"})
                
        elif operation == "read":
            try:
                if os.path.isdir(source):
                    return json.dumps({"error": f"Cannot read a directory: {source}"})
                
                with open(source, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                return json.dumps({"content": content})
            except UnicodeDecodeError:
                return json.dumps({"error": "File appears to be binary and cannot be read as text"})
            except Exception as e:
                return json.dumps({"error": f"Read failed: {str(e)}"})
                
        elif operation == "write":
            try:
                with open(destination, 'w', encoding='utf-8') as f:
                    f.write(content)
                return json.dumps({"message": f"Successfully wrote to {destination}"})
            except Exception as e:
                return json.dumps({"error": f"Write failed: {str(e)}"})
                
        elif operation == "list_directory":
            try:
                if not os.path.isdir(source):
                    return json.dumps({"error": f"Not a directory: {source}"})
                
                items = []
                for item in os.listdir(source):
                    full_path = os.path.join(source, item)
                    is_dir = os.path.isdir(full_path)
                    items.append({
                        "name": item,
                        "type": "directory" if is_dir else "file",
                        "path": full_path
                    })
                
                return json.dumps({"items": items})
            except Exception as e:
                return json.dumps({"error": f"List directory failed: {str(e)}"})
                
        elif operation == "directory_tree":
            try:
                if not os.path.isdir(source):
                    return json.dumps({"error": f"Not a directory: {source}"})
                
                def build_tree(path, max_depth=3, current_depth=0):
                    if current_depth > max_depth:
                        return {"name": os.path.basename(path), "type": "directory", "children": [{"name": "...", "type": "more"}]}
                    
                    result = {"name": os.path.basename(path), "type": "directory", "children": []}
                    
                    try:
                        for item in os.listdir(path):
                            full_path = os.path.join(path, item)
                            if os.path.isdir(full_path):
                                result["children"].append(build_tree(full_path, max_depth, current_depth + 1))
                            else:
                                result["children"].append({"name": item, "type": "file"})
                    except PermissionError:
                        result["children"].append({"name": "Permission denied", "type": "error"})
                    
                    return result
                
                tree = build_tree(source)
                return json.dumps({"tree": tree})
            except Exception as e:
                return json.dumps({"error": f"Directory tree failed: {str(e)}"})
                
        elif operation == "file_info":
            try:
                if not os.path.exists(source):
                    return json.dumps({"error": f"File not found: {source}"})
                
                stat = os.stat(source)
                info = {
                    "name": os.path.basename(source),
                    "path": source,
                    "size": stat.st_size,
                    "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "accessed": datetime.datetime.fromtimestamp(stat.st_atime).isoformat(),
                    "is_directory": os.path.isdir(source),
                    "is_file": os.path.isfile(source),
                    "permissions": oct(stat.st_mode)[-3:]
                }
                
                return json.dumps({"info": info})
            except Exception as e:
                return json.dumps({"error": f"File info failed: {str(e)}"})
                
        elif operation == "search":
            try:
                if not os.path.isdir(source):
                    return json.dumps({"error": f"Not a directory: {source}"})
                
                matches = []
                for item in glob.glob(f"{source}/**/{pattern}", recursive=True):
                    if os.path.exists(item):  # Check in case it was deleted during search
                        matches.append({
                            "path": item,
                            "name": os.path.basename(item),
                            "is_directory": os.path.isdir(item)
                        })
                
                return json.dumps({"matches": matches})
            except Exception as e:
                return json.dumps({"error": f"Search failed: {str(e)}"})
                
        elif operation == "create_directory":
            try:
                os.makedirs(destination, exist_ok=True)
                return json.dumps({"message": f"Successfully created directory: {destination}"})
            except Exception as e:
                return json.dumps({"error": f"Create directory failed: {str(e)}"})
                
        elif operation == "copy":
            try:
                if filename:
                    matches = list(Path(source).glob(f"{filename}*"))
                    if not matches:
                        return json.dumps({"error": f"No file matching '{filename}' found"})
                    
                    src_file = matches[0]
                    dst_file = Path(destination) / src_file.name
                    
                    if os.path.isdir(src_file):
                        shutil.copytree(src_file, dst_file)
                    else:
                        shutil.copy2(src_file, dst_file)
                    
                    return json.dumps({"message": f"Successfully copied {src_file} to {dst_file}"})
                else:
                    return json.dumps({"error": "Filename required for copy operation"})
            except Exception as e:
                return json.dumps({"error": f"Copy failed: {str(e)}"})
        else:
            return json.dumps({"error": "Invalid operation"})

        return json.dumps({"message": "File operation completed successfully"})
        
    except Exception as e:
        return json.dumps({"error": str(e)})

object = {
    "name": "file_ops",
    "description": """Handle file operations with smart path resolution.

Examples:
"move report from downloads to documents"
→ {"operation": "move", "source": "~/Downloads", "destination": "~/Documents", "filename": "report"}

"move latest download to Documents"
→ {"operation": "latest", "source": "~/Downloads", "destination": "~/Documents"}

"read my notes.txt file"
→ {"operation": "read", "source": "~/notes.txt"}

"list files in Downloads folder"
→ {"operation": "list_directory", "source": "~/Downloads"}

"get info about my resume.pdf"
→ {"operation": "file_info", "source": "~/Documents/resume.pdf"}

"search for python files in my projects folder"
→ {"operation": "search", "source": "~/Projects", "pattern": "*.py"}""",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["move", "latest", "read", "write", "list_directory", "directory_tree", "file_info", "search", "create_directory", "copy"],
                "description": "Type of file operation"
            },
            "source": {
                "type": "string",
                "description": "Source path (use ~ for home directory)"
            },
            "destination": {
                "type": "string", 
                "description": "Destination path (use ~ for home directory)"
            },
            "filename": {
                "type": "string",
                "description": "Filename without extension (optional)"
            },
            "content": {
                "type": "string",
                "description": "Content to write to a file"
            },
            "pattern": {
                "type": "string",
                "description": "Search pattern (e.g., *.txt for text files)"
            }
        },
        "required": ["operation"]
    }
}