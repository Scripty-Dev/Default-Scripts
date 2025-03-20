import os
import subprocess
import json
import shutil
import platform
import tkinter as tk
from tkinter import filedialog

public_description = "Convert files between various formats (audio, video, images) using local tools."
PLATFORM = platform.system().lower()

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1][1:].lower()

def ensure_tools_installed():
    required_tools = {
        "ffmpeg": "FFmpeg for audio/video conversion",
        "convert": "ImageMagick for image conversion",
    }
    
    missing_tools = []
    
    for tool, description in required_tools.items():
        if shutil.which(tool) is None:
            missing_tools.append(f"{tool} ({description})")
    
    if missing_tools:
        return {
            "error": "Missing required tools",
            "missing": missing_tools,
            "instructions": {
                "windows": "Install tools using chocolatey or direct downloads",
                "darwin": "Install tools using brew: brew install ffmpeg imagemagick",
                "linux": "Install tools using your package manager, e.g., apt install ffmpeg imagemagick"
            }
        }
    
    return {"success": True}

def convert_media(input_file, output_file, format_params=None):
    try:
        cmd = ["ffmpeg", "-i", input_file]

        if format_params:
            cmd.extend(format_params)
            
        cmd.append(output_file)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"error": f"FFmpeg error: {result.stderr}"}
        
        return {"success": True, "output_file": output_file}
    except Exception as e:
        return {"error": f"Media conversion failed: {str(e)}"}

def convert_image(input_file, output_file, format_params=None):
    try:
        cmd = ["convert", input_file]
        
        if format_params:
            cmd.extend(format_params)
            
        cmd.append(output_file)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"error": f"ImageMagick error: {result.stderr}"}
        
        return {"success": True, "output_file": output_file}
    except Exception as e:
        return {"error": f"Image conversion failed: {str(e)}"}

def get_conversion_command(input_ext, output_ext):
    media_formats = ["mp3", "mp4", "wav", "flac", "ogg", "avi", "mkv", "webm", "m4a", "aac"]
    image_formats = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg"]
    
    if input_ext in media_formats and output_ext in media_formats:
        return "media", None
    elif input_ext in image_formats and output_ext in image_formats:
        return "image", None
    else:
        if input_ext in image_formats and output_ext == "pdf":
            return "image", None
        elif input_ext in media_formats and output_ext == "gif":
            return "media", ["-vf", "scale=320:-1"]
        
        return None, None

def process_file(input_file, output_format, output_file=None):
    input_ext = get_file_extension(input_file)
    
    if not output_file:
        output_dir = os.path.dirname(input_file)
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}.{output_format}")
    
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    
    converter_type, params = get_conversion_command(input_ext, output_format)
    
    if not converter_type:
        return {"error": f"Conversion from {input_ext} to {output_format} is not supported", "file": input_file}
    
    if converter_type == "media":
        result = convert_media(input_file, output_file, params)
    elif converter_type == "image":
        result = convert_image(input_file, output_file, params)
    else:
        return {"error": "Unknown converter type", "file": input_file}
    
    if "error" in result:
        result["file"] = input_file
        return result
    
    return {"success": True, "output_file": output_file, "input_file": input_file}

def open_file_explorer(folder=False):
    try:
        root = tk.Tk()
        root.withdraw()
        
        if folder:
            path = filedialog.askdirectory(title="Select Folder")
        else:
            path = filedialog.askopenfilename(title="Select File")
            
        root.destroy()
        
        if path:
            return path.replace('\\', '/')
        return None
    except Exception as e:
        print(f"Error opening file explorer: {str(e)}")
        return None

async def function(args):
    try:
        if isinstance(args, str):
            try:
                args = json.loads(args.replace('\\', '\\\\'))
            except json.JSONDecodeError:
                args = {"input_file": args}
        
        input_path = os.path.expanduser(args.get("input_file", ""))
        output_format = args.get("output_format", "").lower()
        output_file = args.get("output_file", "")
        
        input_path = input_path.replace('\\', '/')
        if output_file:
            output_file = output_file.replace('\\', '/')
        
        if not input_path or not os.path.exists(input_path):
            print(f"Path '{input_path}' not found. Opening file explorer...")
            selected_path = open_file_explorer(folder=args.get("folder_mode", False))
            
            if not selected_path:
                return json.dumps({"error": "No file or folder selected"})
            
            input_path = selected_path
            print(f"Selected path: {input_path}")
        
        if not output_format:
            return json.dumps({"error": "Output format not specified"})
        
        supported_formats = [
            "mp3", "wav", "flac", "ogg", "aac", "m4a",
            "mp4", "avi", "mkv", "webm", "mov", "gif",
            "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg", "pdf"
        ]
        
        if output_format not in supported_formats:
            return json.dumps({
                "error": f"Output format '{output_format}' not supported",
                "supported_formats": supported_formats
            })
        
        tools_check = ensure_tools_installed()
        if "error" in tools_check:
            return json.dumps(tools_check)
        
        results = []
        
        if os.path.isfile(input_path):
            result = process_file(input_path, output_format, output_file)
            results.append(result)
        elif os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = get_file_extension(file_path)
                    
                    converter_type, _ = get_conversion_command(file_ext, output_format)
                    if converter_type:
                        result = process_file(file_path, output_format)
                        results.append(result)
        
        success_count = sum(1 for r in results if r.get("success", False))
        
        if not results:
            return json.dumps({
                "success": False,
                "message": "No files were found to convert"
            })
        
        if len(results) == 1:
            return json.dumps(results[0])
        
        return json.dumps({
            "success": success_count > 0,
            "message": f"Converted {success_count} of {len(results)} files",
            "details": results
        })
        
    except Exception as e:
        return json.dumps({"error": str(e)})

object = {
    "name": "file_converter",
    "description": "Convert files between various formats (audio, video, images) using local tools.",
    "parameters": {
        "type": "object",
        "properties": {
            "input_file": {
                "type": "string",
                "description": "The path to the input file or folder to be converted. If the parent folder of the input file/folder is not specified, assume it's in home directory."
            },
            "output_format": {
                "type": "string",
                "description": "The desired output format (e.g., 'mp3', 'wav', 'jpg', etc.)"
            },
            "output_file": {
                "type": "string",
                "description": "The path to save the converted file (only used for single file conversion)"
            },
            "folder_mode": {
                "type": "boolean",
                "description": "Set to true to select a folder instead of a file when using the file explorer"
            }
        },
        "required": ["input_file", "output_format"]
    }
}