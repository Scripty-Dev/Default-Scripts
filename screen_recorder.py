import json
import platform

public_description = "Capture desktop screen using 'start' and 'stop' commands."
PLATFORM = platform.system().lower()

async def function(args):
    if args.get("action") == "start":
        result = start_recording(
            fps=60,
            record_audio=True
        )
        
        if result.get("success"):
            recording_id = result.get("recording_id", "unknown")
            return json.dumps({
                "status": "success",
                "message": f"Recording started and will be saved to {result.get('path', 'unknown')}",
            })
        else:
            return json.dumps({
                "status": "error",
                "message": f"Failed to start recording: {result.get('error', 'Unknown error')}"
            })
            
    elif args.get("action") == "stop":
        try:
            result = stop_recording()
            
            if result.get("success"):
                return json.dumps({
                    "status": "success",
                    "message": "Recording stopped successfully",
                    "path": result.get("path", "")
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Failed to stop recording: {result.get('error', 'Unknown error')}"
                })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error stopping recording: {str(e)}"
            })
    
    else:
        return json.dumps({
            "status": "error",
            "message": f"Unknown action: {args.get('action')}. Use 'start' or 'stop'."
        })

object = {
    "name": "screen_recorder",
    "description": "Record screen using 'start' and 'stop' commands",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to take: 'start' or 'stop' the recording",
                "enum": ["start", "stop"]
            }
        }
    }
}