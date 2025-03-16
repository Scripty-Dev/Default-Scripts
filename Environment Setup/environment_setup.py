from ..typings.scripty import script_dir
from tkinter import filedialog
import tkinter as tk
import subprocess
import shutil
import json
import os

public_description = "Set up a new project environment."

def copyFolder(project_path, env_type, folder_name = None):
    if folder_name:
        shutil.copytree(os.path.join(script_dir, "templates", env_type, folder_name), os.path.join(project_path, folder_name))
    else:
        shutil.copytree(os.path.join(script_dir, "templates", env_type), project_path)

def copyResources(folder_path, resource_name):
    source_path = os.path.join(script_dir, "resources", resource_name)

    for item in os.listdir(source_path):
        source_item = os.path.join(source_path, item)
        dest_item = os.path.join(folder_path, item)
        shutil.copy2(source_item, dest_item)

def installBunDependencies(folder_path, dependencies):
    for dependency in dependencies:
        subprocess.run(["bun", "i", dependency], cwd=folder_path, check=True)

def installBunDevDependencies(folder_path, dependencies):
    if "@types/bun" not in dependencies:
        dependencies.extend(["@types/bun", "ts-node", "typescript"])

    for dependency in dependencies:
        subprocess.run(["bun", "i", "-D", dependency], cwd=folder_path, check=True)
        
def initializeNext(folder_path):
    installBunDependencies(folder_path, ["next", "react", "react-dom"])
    installBunDevDependencies(folder_path, ["@types/react", "@types/react-dom", "eslint", "eslint-config-next", "@eslint/eslintrc", "postcss", "tailwindcss", "@tailwindcss/postcss"])
    copyResources(folder_path, "next")

def setup_express_mongo(project_path):
    copyFolder(project_path, "express-mongo")
    installBunDependencies(project_path, [
        "bcryptjs", 
        "cors", 
        "dotenv", 
        "express", 
        "jsonwebtoken", 
        "mongoose",
        "helmet",
        "morgan"
    ])
    installBunDevDependencies(project_path, [
        "@types/bcryptjs", 
        "@types/cors", 
        "@types/dotenv", 
        "@types/express", 
        "@types/jsonwebtoken", 
        "@types/mongoose",
        "@types/helmet",
        "@types/morgan",
        "nodemon"
    ])

def setup_mern_next(project_path):
    copyFolder(project_path, "mern-next", "backend")
    installBunDependencies(os.path.join(project_path, "backend"), ["bcryptjs", "cors", "dotenv", "express", "jsonwebtoken", "mongoose"])
    installBunDevDependencies(os.path.join(project_path, "backend"), ["@types/bcryptjs", "@types/cors", "@types/dotenv", "@types/express", "@types/jsonwebtoken", "@types/mongoose"])

    copyFolder(project_path, "mern-next", "frontend")
    initializeNext(os.path.join(project_path, "frontend"))
    installBunDependencies(os.path.join(project_path, "frontend"), ["axios"])

def setup_next(project_path):
    copyFolder(project_path, "next")
    initializeNext(project_path)

async def function(args):
    env_type = args["env_type"]
    folder_name = args["folder_name"]

    root = tk.Tk()
    root.withdraw()

    selected_path = filedialog.askdirectory(title=f"Select location for your {env_type} project")
    if not selected_path:
        return json.dumps({
            "message": "Project setup was cancelled",
        })
    
    project_path = os.path.join(selected_path, folder_name)

    if env_type == "mern-next":
        setup_mern_next(project_path)
    elif env_type == "next":
        setup_next(project_path)
    elif env_type == "express-mongo":
        setup_express_mongo(project_path)
    
    shutil.copy2(os.path.join(script_dir, "templates", env_type, "README.md"), os.path.join(project_path, "README.md"))

    return json.dumps({
        "message": "Project setup was successful",
    })
        
object = {
    "name": "environment_setup",
    "description": "Set up a new environment for a project",
    "parameters": {
        "type": "object",
        "properties": {
            "env_type": {
                "type": "string",
                "description": "The type of environment to set up",
                "enum": ["express-mongo", "mern-next", "next"]
            },
            "folder_name": {
                "type": "string",
                "description": "The name of the folder to create"
            }
        },
        "required": ["env_type", "folder_name"]
    }
}