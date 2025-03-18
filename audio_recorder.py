import platform
import subprocess
import json
import os
import time

public_description = "Record audio from the microphone and save to file."
PLATFORM = platform.system().lower()
STATE_FILE = os.path.expanduser("~/.audio_recorder_state.json")

async def function(args):
    try:
        command = args.get("command", "")
        output_dir = args.get("output_dir", "~/Documents")
        output_dir = os.path.expanduser(output_dir)
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                return json.dumps({"error": f"Failed to create output directory: {str(e)}"})

        recording_state = {}
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    recording_state = json.load(f)
            except:
                recording_state = {}
        
        if command == "start":
            if recording_state.get("active", False):
                pid = recording_state.get("pid")
                if _is_process_running(pid):
                    return json.dumps({"error": "Recording already in progress"})
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"recording_{timestamp}.mp3")
            
            try:
                cmd = []
                
                if PLATFORM == "darwin":
                    cmd = [
                        "ffmpeg", 
                        "-f", "avfoundation", 
                        "-i", ":0",
                        "-y",
                        "-c:a", "libmp3lame",
                        "-q:a", "2",
                        "-ar", "44100",
                        output_file
                    ]
                elif PLATFORM == "windows":
                    cmd = [
                        "ffmpeg",
                        "-f", "dshow",
                        "-i", "audio=Microphone Array (Realtek(R) Audio)",
                        "-y",
                        "-c:a", "libmp3lame",
                        "-q:a", "2",
                        "-ar", "44100",
                        output_file
                    ]
                elif PLATFORM == "linux":
                    cmd = [
                        "ffmpeg",
                        "-f", "pulse",
                        "-i", "default",
                        "-y",
                        "-c:a", "libmp3lame",
                        "-q:a", "2",
                        "-ar", "44100",
                        output_file
                    ]
                else:
                    return json.dumps({"error": f"Unsupported platform: {PLATFORM}"})
                
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                time.sleep(0.5)
                if process.poll() is not None:
                    _, stderr = process.communicate()
                    return json.dumps({
                        "error": f"FFmpeg failed to start recording: {stderr}"
                    })
                
                serializable_state = {
                    "active": True,
                    "pid": process.pid,
                    "file": output_file,
                    "started_at": time.time(),
                    "command": " ".join(cmd)
                }
                
                with open(STATE_FILE, 'w') as f:
                    json.dump(serializable_state, f)
                
                return json.dumps({
                    "message": "Recording started",
                    "file": output_file,
                    "process_id": process.pid
                })
            except Exception as e:
                return json.dumps({"error": f"Failed to start recording: {str(e)}"})
                
        elif command == "stop":
            if not recording_state.get("active", False):
                return json.dumps({"error": "No recording in progress"})
            
            pid = recording_state.get("pid")
            output_file = recording_state.get("file", "")
            
            try:
                if _is_process_running(pid):
                    if PLATFORM == "windows":
                        subprocess.run(["taskkill", "/PID", str(pid)])
                        time.sleep(0.5)
                        if _is_process_running(pid):
                            subprocess.run(["taskkill", "/F", "/PID", str(pid)])
                    else:
                        os.kill(pid, 15)
                        time.sleep(0.5)
                        if _is_process_running(pid):
                            os.kill(pid, 9)
                    
                    time.sleep(1)
                
                recording_state = {"active": False}
                with open(STATE_FILE, 'w') as f:
                    json.dump(recording_state, f)
                
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    return json.dumps({
                        "message": "Recording stopped successfully",
                        "file": output_file,
                        "file_size_bytes": file_size
                    })
                else:
                    return json.dumps({
                        "message": "Recording stopped but file not found",
                        "file": output_file,
                        "error": "Recording file not created properly"
                    })
            except Exception as e:
                return json.dumps({"error": f"Failed to stop recording: {str(e)}"})
        else:
            return json.dumps({"error": "Invalid command. Use 'start' or 'stop'."})
    
    except Exception as e:
        return json.dumps({"error": str(e)})

def _is_process_running(pid):
    if pid is None:
        return False
        
    try:
        if PLATFORM == "windows":
            output = subprocess.check_output(["tasklist", "/FI", f"PID eq {pid}"])
            return str(pid) in str(output)
        else:
            os.kill(pid, 0)
            return True
    except:
        return False

object = {
    "name": "audio_recorder",
    "description": """Record audio from the default microphone and save to file.

Examples:
"start recording audio"
→ {"command": "start", "output_dir": "~/Documents"}

"stop recording audio"
→ {"command": "stop"}""",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "enum": ["start", "stop"],
                "description": "Command to start or stop recording"
            },
            "output_dir": {
                "type": "string",
                "description": "Directory to save recordings (default: ~/Documents)"
            }
        },
        "required": ["command"]
    }
} 