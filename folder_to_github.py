import os
import subprocess
import json

public_description = "Create a GitHub repository from a local folder."

def upload_folder_to_github(folder_path, repo_name, github_username, github_token, private=True):
    original_dir = os.getcwd()
    
    try:
        os.chdir(folder_path)
        subprocess.run(["git", "init"], check=True)

        try:
            subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.PIPE)
        except:
            pass 

        subprocess.run(["git", "add", "."], check=True)
        try:
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        except:
            subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial commit"], check=True)
        
        create_repo_data = f'{{"name":"{repo_name}","private":{str(private).lower()}}}'
        
        create_repo_cmd = [
            "curl", "-s", "-X", "POST",
            "-H", f"Authorization: token {github_token}", 
            "-H", "Accept: application/vnd.github.v3+json",
            "https://api.github.com/user/repos", 
            "-d", create_repo_data
        ]
        
        result = subprocess.run(create_repo_cmd, capture_output=True, text=True)
        
        if "Bad credentials" in result.stdout or "Bad credentials" in result.stderr:
            return {"error": "GitHub token is invalid. Please check your token has the 'repo' scope."}
        
        if "already exists" in result.stdout or "already exists" in result.stderr:
            print(f"Repository {repo_name} already exists, continuing with push.")

        remote_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)

        push_result = subprocess.run(["git", "push", "-u", "origin", "master"], capture_output=True, text=True)
        
        if push_result.returncode == 0:
            return {"message": f"Successfully uploaded folder to https://github.com/{github_username}/{repo_name}"}
        else:
            push_main_result = subprocess.run(["git", "push", "-u", "origin", "master:main"], capture_output=True, text=True)
            if push_main_result.returncode == 0:
                return {"message": f"Successfully uploaded folder to https://github.com/{github_username}/{repo_name} (main branch)"}
            else:
                return {"error": f"Push failed: {push_main_result.stderr}"}
        
    except subprocess.CalledProcessError as e:
        return {"error": f"Git operation failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Error during GitHub upload: {str(e)}"}
    finally:
        os.chdir(original_dir)

async def function(args):
    try:
        folder_path = os.path.expanduser(args.get("folder_path", ""))
        repo_name = args.get("repo_name", "")
        github_username = args.get("github_username", "")
        github_token = args.get("github_token", "")
        is_private = args.get("private", True)
        
        if not folder_path or not repo_name or not github_username or not github_token:
            return json.dumps({
                "error": "Missing required parameters",
                "token_instructions": "To create a GitHub token:\n1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)\n2. Click 'Generate new token' → 'Generate new token (classic)'\n3. Name your token (e.g., 'Repo Creator')\n4. Select the 'repo' scope checkbox\n5. Click 'Generate token' at the bottom\n6. Copy your token"
            })
        
        if not os.path.exists(folder_path):
            return json.dumps({"error": f"Folder not found: {folder_path}"})
            
        result = upload_folder_to_github(folder_path, repo_name, github_username, github_token, is_private)
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

object = {
    "name": "github_upload",
    "description": """Create a GitHub repository from a local folder and upload all its contents.

Example:
"upload my project folder to GitHub"
→ {"folder_path": "~/Projects/my-app", "repo_name": "my-app", "github_username": "username", "github_token": "your-token", "private": true}

Note: You need a GitHub personal access token with 'repo' scope to use this function.""",
    "parameters": {
        "type": "object",
        "properties": {
            "folder_path": {
                "type": "string",
                "description": "Path to the local folder to upload (use ~ for home directory)"
            },
            "repo_name": {
                "type": "string",
                "description": "Name for the new GitHub repository"
            },
            "github_username": {
                "type": "string",
                "description": "GitHub username"
            },
            "github_token": {
                "type": "string",
                "description": "GitHub personal access token with repo scope"
            },
            "private": {
                "type": "boolean",
                "description": "Whether the GitHub repository should be private",
                "default": True
            }
        },
        "required": ["folder_path", "repo_name", "github_username", "github_token"]
    }
}