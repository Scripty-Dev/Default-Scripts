from ..typings.scripty import script_dir
from tkinter import filedialog, messagebox
import tkinter as tk
import subprocess
import shutil
import os

public_description = "Set up a new project environment."

class EnvironmentSetup:
    def __init__(self, template_name, project_title, default_folder_name, commands):
        self.template_name = template_name
        self.project_title = project_title
        self.default_folder_name = default_folder_name
        self.commands = commands
        
    def run_command(self, command, cwd=None):
        try:
            process = subprocess.Popen(
                command, 
                cwd=cwd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Command failed: {stderr}")
                return False
            return True
        except Exception as e:
            print(f"Error executing command: {str(e)}")
            return False

    def copy_template_file(self, template_path, dest_path, replacements=None):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            if not replacements:
                shutil.copy2(template_path, dest_path)
                return True
            
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                is_text = True
            except UnicodeDecodeError:
                shutil.copy2(template_path, dest_path)
                return True
                
            if is_text:
                for key, value in replacements.items():
                    content = content.replace(key, value)
                    
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            return True
        except Exception as e:
            print(f"Error copying template file: {str(e)}")
            return False
    
    def create_project_directories(self, full_path, directories=None):
        os.makedirs(full_path, exist_ok=True)
        
        if directories:
            for directory in directories:
                dir_path = os.path.join(full_path, directory)
                os.makedirs(dir_path, exist_ok=True)
                print(f"Created directory: {dir_path}")
        
        return True
    
    def copy_template_directory_recursive(self, template_dir, dest_dir, replacements=None):
        try:
            os.makedirs(dest_dir, exist_ok=True)

            try:
                shutil.copytree(template_dir, dest_dir, dirs_exist_ok=True)
            except TypeError:
                for item in os.listdir(template_dir):
                    src_item = os.path.join(template_dir, item)
                    dst_item = os.path.join(dest_dir, item)
                    if os.path.isdir(src_item):
                        if not os.path.exists(dst_item):
                            shutil.copytree(src_item, dst_item)
                        else:
                            self.copy_template_directory_recursive(src_item, dst_item)
                    else:
                        shutil.copy2(src_item, dst_item)
            
            readme_path = os.path.join(template_dir, "README.md")
            readme_dest = os.path.join(dest_dir, "README.md")
            
            if os.path.exists(readme_path) and not os.path.exists(readme_dest):
                print(f"README.md not copied automatically, copying manually...")
                shutil.copy2(readme_path, readme_dest)
            
            if replacements:
                self._apply_replacements_recursive(dest_dir, replacements)
                
            if os.path.exists(readme_path):
                print(f"Verifying README.md was copied to {readme_dest}")
                if not os.path.exists(readme_dest):
                    print(f"README.md still missing, forcing copy...")
                    with open(readme_path, 'rb') as src, open(readme_dest, 'wb') as dst:
                        dst.write(src.read())
            
            return True
        except Exception as e:
            print(f"Error copying template directory: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def _apply_replacements_recursive(self, directory, replacements):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if self._is_binary_file(file_path):
                        continue
                        
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    modified = False
                    for key, value in replacements.items():
                        if key in content:
                            content = content.replace(key, value)
                            modified = True
                    
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"Warning: Could not process replacements in {file_path}: {e}")
    
    def _is_binary_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)
                return False
        except UnicodeDecodeError:
            return True

    def install_dependencies(self, full_path, commands):
        for cmd in commands:
            if not self.run_command(cmd, cwd=full_path):
                return False
        
        return True

    def setup_project(self, folder_name=None):
        try:
            if not folder_name:
                folder_name = self.default_folder_name

            root = tk.Tk()
            root.withdraw()
            
            print(f"Select a parent directory for your {self.project_title} project...")
            parent_directory = filedialog.askdirectory(
                title=f"Select parent directory for {self.project_title} project",
                initialdir=os.getcwd()
            )
            
            if not parent_directory:
                print("Project setup cancelled.")
                return False
            
            full_path = os.path.join(parent_directory, folder_name)
            
            if os.path.exists(full_path) and os.listdir(full_path):         
                root = tk.Tk()
                root.withdraw()
                
                overwrite = messagebox.askyesno(
                    "Directory exists",
                    f"Directory {full_path} already exists and contains files. Overwrite?",
                )
                
                if not overwrite:
                    print("Project setup cancelled.")
                    return False
                
            template_dir = os.path.join(script_dir, "templates", self.template_name)
            
            if not os.path.exists(template_dir):
                print(f"Template directory {template_dir} not found.")
                return False
                
            replacements = {
                "{{PROJECT_NAME}}": folder_name,
                "{{PROJECT_TITLE}}": self.project_title
            }
            
            if self.template_name == "express":
                return express_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "fastapi":
                return fastapi_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "flask":
                return flask_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "mern-next":
                return mern_next_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "next":
                return next_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "sveltekit":
                return sveltekit_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "vite":
                return vite_setup_commands(self, full_path, template_dir, replacements)
            elif self.template_name == "vue":
                return vue_setup_commands(self, full_path, template_dir, replacements)
            else:
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                
                if self.copy_template_directory_recursive(template_dir, full_path, replacements):
                    if self.commands:
                        self.install_dependencies(full_path, self.commands)
                    print(f"{self.project_title} project setup complete! Navigate to {full_path} to get started.")
                    return True
                return False
                
        except Exception as e:
            print(f"Error setting up project: {e}")
            return False

def express_setup_commands(setup, full_path, template_dir, replacements):
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "bun install"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"Express.js project setup complete! Navigate to {full_path} and run 'bun run dev' to start the development server.")
    return True

def fastapi_setup_commands(setup, full_path, template_dir, replacements):
    if not setup.create_project_directories(full_path):
        return False
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "python -m venv venv",
        f"{os.path.join('venv', 'Scripts', 'activate') if os.name == 'nt' else f'source {os.path.join('venv', 'bin', 'activate')}'}",
        "pip install -r requirements.txt"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"FastAPI project setup complete! Navigate to {full_path} and run 'uvicorn main:app --reload' to start the development server.")
    return True

def flask_setup_commands(setup, full_path, template_dir, replacements):
    if not setup.create_project_directories(full_path):
        return False
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "python -m venv venv",
        f"{os.path.join('venv', 'Scripts', 'activate') if os.name == 'nt' else f'source {os.path.join('venv', 'bin', 'activate')}'}",
        "pip install -r requirements.txt"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"Flask project setup complete! Navigate to {full_path} and run 'flask run' to start the development server.")
    return True

def mern_next_setup_commands(setup, full_path, template_dir, replacements):
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    backend_commands = [
        "bun install"
    ]
    if not setup.install_dependencies(os.path.join(full_path, "backend"), backend_commands):
        return False
    
    frontend_commands = [
        "bun install"
    ]
    if not setup.install_dependencies(os.path.join(full_path, "frontend"), frontend_commands):
        return False
    
    print(f"MERN + Next.js project setup complete!")
    return True

def next_setup_commands(setup, full_path, template_dir, replacements):
    if not setup.create_project_directories(full_path):
        return False
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "bun install"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"Next.js project setup complete! Navigate to {full_path} and run 'bun run dev' to start the development server.")
    return True

def sveltekit_setup_commands(setup, full_path, template_dir, replacements):
    if not setup.create_project_directories(full_path):
        return False
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "bun install"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"SvelteKit project setup complete! Navigate to {full_path} and run 'bun run dev' to start the development server.")
    return True

def vite_setup_commands(setup, full_path, template_dir, replacements):
    if not setup.create_project_directories(full_path):
        return False
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "bun install"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"Vite + React project setup complete! Navigate to {full_path} and run 'bun run dev' to start the development server.")
    return True

def vue_setup_commands(setup, full_path, template_dir, replacements):
    if not setup.create_project_directories(full_path):
        return False
    
    if not setup.copy_template_directory_recursive(template_dir, full_path, replacements):
        return False
    
    commands = [
        "bun install"
    ]
    if not setup.install_dependencies(full_path, commands):
        return False
    
    print(f"Vue.js project setup complete! Navigate to {full_path} and run 'bun run dev' to start the development server.")
    return True

express_setup = EnvironmentSetup('express', 'Express.js + TypeScript', 'express-api', express_setup_commands)
fastapi_setup = EnvironmentSetup('fastapi', 'FastAPI + React', 'fastapi-react', fastapi_setup_commands)
flask_setup = EnvironmentSetup('flask', 'Flask + React', 'flask-react', flask_setup_commands)
mern_next_setup = EnvironmentSetup('mern-next', 'MERN Stack + Next.js', 'mern-next-app', mern_next_setup_commands)
next_setup = EnvironmentSetup('next', 'Next.js + TypeScript', 'next-app', next_setup_commands)
sveltekit_setup = EnvironmentSetup('sveltekit', 'SvelteKit + TypeScript', 'sveltekit-app', sveltekit_setup_commands)
vite_setup = EnvironmentSetup('vite', 'Vite + React', 'vite-react-app', vite_setup_commands)
vue_setup = EnvironmentSetup('vue', 'Vue.js + TypeScript', 'vue-app', vue_setup_commands)

environments = {
    'express': express_setup,
    'fastapi': fastapi_setup,
    'flask': flask_setup,
    'mern-next': mern_next_setup,
    'next': next_setup,
    'sveltekit': sveltekit_setup,
    'vite': vite_setup,
    'vue': vue_setup
}

async def function(args):
    if not args:
        print("Please specify which environment to set up: 'express', 'fastapi', 'flask', 'mern-next', 'next', 'sveltekit', 'vite', or 'vue'")
        return
    
    env_type = args['env_type'].lower()
    folder_name = args['folder_name']
    
    if env_type not in environments:
        return {
            'success': False,
            'message': f"Invalid environment type. Available options: {', '.join(environments.keys())}"
        }
    
    env_setup = environments[env_type]
    success = env_setup.setup_project(folder_name)
    
    if success:
        return {
            'success': True,
            'message': f"{env_setup.project_title} project setup complete!"
        }
    else:
        return {
            'success': False,
            'message': f"Failed to setup {env_setup.project_title} project."
        }

object = {
    "name": "environment_setup",
    "description": "Set up a new environment for a project",
    "parameters": {
        "type": "object",
        "properties": {
            "env_type": {
                "type": "string",
                "description": "The type of environment to set up",
                "enum": ["express", "fastapi", "flask", "mern-next", "next", "sveltekit", "vite", "vue"]
            },
            "folder_name": {
                "type": "string",
                "description": "The name of the folder to create"
            }
        },
        "required": ["env_type"]
    }
}