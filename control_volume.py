import subprocess
import platform
import json
import re

public_description = "Control system and application-specific volume."
PLATFORM = platform.system().lower()

async def function(args):
    if PLATFORM == "windows":
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        VOLUME_INTERFACE = cast(interface, POINTER(IAudioEndpointVolume))
    
    try:
        # Handle app-specific volume control if app parameter is provided
        if 'app' in args:
            app_name = args['app'].lower()
            
            if PLATFORM == "windows":
                # Windows approach - using pycaw to control app-specific volume
                sessions = AudioUtilities.GetAllSessions()
                app_found = False
                
                for session in sessions:
                    if session.Process and session.Process.name().lower().startswith(app_name):
                        volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                        app_found = True
                        
                        if 'set' in args:
                            target = max(0, min(100, int(args['set'])))
                            volume_interface.SetMasterVolume(target / 100.0, None)
                            return json.dumps({"message": f"{session.Process.name()} volume set to {target}%"})
                            
                        elif 'adjust' in args:
                            change = max(-100, min(100, int(args['adjust'])))
                            current_vol = volume_interface.GetMasterVolume()
                            new_vol = max(0.0, min(1.0, current_vol + (change / 100.0)))
                            volume_interface.SetMasterVolume(new_vol, None)
                            return json.dumps({"message": f"{session.Process.name()} volume adjusted by {change}% to {int(new_vol * 100)}%"})
                
                if not app_found:
                    return json.dumps({"error": f"Application '{args['app']}' not found or not playing audio"})
                    
            elif PLATFORM == "darwin":
                # macOS approach - using AppleScript
                if 'set' in args:
                    target = max(0, min(100, int(args['set'])))
                    script = f'''
                    tell application "System Events"
                        set appVolume to {target / 100.0}
                        if application process "{args['app']}" exists then
                            tell application process "{args['app']}"
                                set volume appVolume
                            end tell
                            return "Volume set to {target}%"
                        else
                            return "Application not found"
                        end if
                    end tell
                    '''
                    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
                    if "not found" in result.stdout:
                        return json.dumps({"error": f"Application '{args['app']}' not found or not supported"})
                    return json.dumps({"message": f"{args['app']} volume set to {target}%"})
                    
                elif 'adjust' in args:
                    change = max(-100, min(100, int(args['adjust'])))
                    script = f'''
                    tell application "System Events"
                        if application process "{args['app']}" exists then
                            tell application process "{args['app']}"
                                set currentVolume to volume
                                set volume to max(0, min(1, currentVolume + {change / 100.0}))
                                set newVolume to volume
                                return newVolume * 100
                            end tell
                        else
                            return "Application not found"
                        end if
                    end tell
                    '''
                    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
                    if "not found" in result.stdout:
                        return json.dumps({"error": f"Application '{args['app']}' not found or not supported"})
                    try:
                        new_vol = int(float(result.stdout.strip()))
                        return json.dumps({"message": f"{args['app']} volume adjusted by {change}% to {new_vol}%"})
                    except ValueError:
                        return json.dumps({"error": f"Failed to adjust volume for {args['app']}"})
                        
            elif PLATFORM == "linux":
                # Linux approach - using pactl (PulseAudio) or wpctl (PipeWire)
                # First, check if system uses PulseAudio or PipeWire
                try:
                    # Check if pactl is available (PulseAudio)
                    subprocess.run(["pactl", "--version"], capture_output=True, check=True)
                    use_pulseaudio = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Check if wpctl is available (PipeWire)
                    try:
                        subprocess.run(["wpctl", "--version"], capture_output=True, check=True)
                        use_pulseaudio = False
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        return json.dumps({"error": "Neither PulseAudio nor PipeWire available on this Linux system"})
                
                # Get the sink-input ID for the app
                app_id = None
                if use_pulseaudio:
                    result = subprocess.run(["pactl", "list", "sink-inputs"], capture_output=True, text=True)
                    lines = result.stdout.split('\n')
                    current_id = None
                    for line in lines:
                        if line.startswith("Sink Input #"):
                            current_id = line.split("#")[1].strip()
                        elif "application.name" in line and args['app'].lower() in line.lower():
                            app_id = current_id
                            break
                        elif "application.process.binary" in line and args['app'].lower() in line.lower():
                            app_id = current_id
                            break
                else:  # PipeWire with wpctl
                    result = subprocess.run(["wpctl", "status"], capture_output=True, text=True)
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if args['app'].lower() in line.lower() and "│" in line:
                            matches = re.search(r'(\d+)\.\s+', line)
                            if matches:
                                app_id = matches.group(1)
                                break
                
                if app_id is None:
                    return json.dumps({"error": f"Application '{args['app']}' not found or not playing audio"})
                
                if 'set' in args:
                    target = max(0, min(100, int(args['set'])))
                    if use_pulseaudio:
                        subprocess.run(["pactl", "set-sink-input-volume", app_id, f"{target}%"])
                    else:  # PipeWire
                        volume_float = target / 100.0
                        subprocess.run(["wpctl", "set-volume", app_id, f"{volume_float:.2f}"])
                    return json.dumps({"message": f"{args['app']} volume set to {target}%"})
                
                elif 'adjust' in args:
                    change = max(-100, min(100, int(args['adjust'])))
                    if use_pulseaudio:
                        if change >= 0:
                            subprocess.run(["pactl", "set-sink-input-volume", app_id, f"+{change}%"])
                        else:
                            subprocess.run(["pactl", "set-sink-input-volume", app_id, f"{change}%"])
                    else:  # PipeWire
                        change_float = change / 100.0
                        if change >= 0:
                            subprocess.run(["wpctl", "set-volume", app_id, f"{change_float:+.2f}"])
                        else:
                            subprocess.run(["wpctl", "set-volume", app_id, f"{change_float:.2f}"])
                    
                    # Get the new volume level for reporting
                    current_vol = None
                    if use_pulseaudio:
                        result = subprocess.run(["pactl", "list", "sink-inputs"], capture_output=True, text=True)
                        lines = result.stdout.split('\n')
                        reading_target = False
                        for line in lines:
                            if line.startswith(f"Sink Input #{app_id}"):
                                reading_target = True
                            elif reading_target and "Volume:" in line:
                                match = re.search(r'(\d+)%', line)
                                if match:
                                    current_vol = int(match.group(1))
                                    break
                    else:  # PipeWire
                        # Just report the adjustment for now as wpctl doesn't easily report current volume
                        pass
                    
                    if current_vol is not None:
                        return json.dumps({"message": f"{args['app']} volume adjusted by {change}% to {current_vol}%"})
                    else:
                        return json.dumps({"message": f"{args['app']} volume adjusted by {change}%"})
            
            return json.dumps({"error": f"Application-specific volume control not supported on {PLATFORM}"})
            
        # Handle system-wide volume control (original functionality)
        if 'set' in args:
            target = max(0, min(100, int(args['set'])))
            
            if PLATFORM == "darwin":
                subprocess.run(["osascript", "-e", f"set volume output volume {target}"])
                return json.dumps({"message": f"System volume set to {target}%"})
                
            elif PLATFORM == "linux":
                try:
                    # Try with PulseAudio first
                    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{target}%"])
                except FileNotFoundError:
                    # Fall back to amixer if pactl is not available
                    subprocess.run(["amixer", "-q", "sset", "Master", f"{target}%"])
                return json.dumps({"message": f"System volume set to {target}%"})
                
            elif PLATFORM == "windows":
                if VOLUME_INTERFACE:
                    VOLUME_INTERFACE.SetMasterVolumeLevelScalar(target / 100.0, None)
                    return json.dumps({"message": f"System volume set to {target}%"})
                return json.dumps({"error": "Windows volume control requires pycaw package"})
                    
            return json.dumps({"error": f"Unsupported operating system: {PLATFORM}"})
        
        elif 'adjust' in args:
            change = max(-100, min(100, int(args['adjust'])))
            
            if PLATFORM == "darwin":
                current = subprocess.getoutput("osascript -e 'output volume of (get volume settings)'")
                new_vol = max(0, min(100, int(current) + change))
                subprocess.run(["osascript", "-e", f"set volume output volume {new_vol}"])
                return json.dumps({"message": f"System volume adjusted by {change}% to {new_vol}%"})
                
            elif PLATFORM == "linux":
                try:
                    # Try with PulseAudio first
                    if change >= 0:
                        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"+{change}%"])
                    else:
                        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{change}%"])
                except FileNotFoundError:
                    # Fall back to amixer if pactl is not available
                    sign = "+" if change > 0 else "-"
                    subprocess.run(["amixer", "-q", "sset", "Master", f"{abs(change)}%{sign}"])
                return json.dumps({"message": f"System volume adjusted by {change}%"})
                
            elif PLATFORM == "windows":
                if VOLUME_INTERFACE:
                    current_vol = VOLUME_INTERFACE.GetMasterVolumeLevelScalar()
                    new_vol = max(0.0, min(1.0, current_vol + (change / 100.0)))
                    VOLUME_INTERFACE.SetMasterVolumeLevelScalar(new_vol, None)
                    return json.dumps({"message": f"System volume adjusted by {change}% to {int(new_vol * 100)}%"})
                return json.dumps({"error": "Windows volume control requires pycaw package"})
                    
            return json.dumps({"error": f"Unsupported operating system: {PLATFORM}"})
            
        return json.dumps({"error": "Please specify either 'set' or 'adjust' in the arguments"})
    except Exception as e:
        return json.dumps({"error": str(e)})

object = {
    "name": "control_volume",
    "description": f"Control system or application volume. Required format: For system volume use {{\"set\": number}} or {{\"adjust\": number}}. For app-specific volume use {{\"app\": \"appname\", \"set\": number}} or {{\"app\": \"appname\", \"adjust\": number}}.",
    "parameters": {
        "type": "object",
        "properties": {
            "set": {
                "type": "integer",
                "description": "Set volume to specific level (0-100)"
            },
            "adjust": {
                "type": "integer", 
                "description": "Adjust volume by relative amount (-100 to +100)"
            },
            "app": {
                "type": "string",
                "description": "Application name to control (e.g., 'spotify', 'chrome', 'zoom')"
            }
        },
        "oneOf": [
            {"required": ["set"]},
            {"required": ["adjust"]},
            {"required": ["app", "set"]},
            {"required": ["app", "adjust"]}
        ]
    }
}
