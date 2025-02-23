import json
from typing import List, Dict

def get_tasks() -> List[Dict]:
    tasks = get_config("tasks")
    return tasks if tasks else []

def add_task(title: str, description: str = "", due_date: str = "") -> Dict:
    tasks = get_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    }
    
    tasks.append(new_task)
    set_config("tasks", tasks)
    
    return {
        "success": True,
        "message": "Task added successfully",
        "task": new_task,
        "tasks": tasks
    }

async def func(args):
    try:
        action = args.get("action", "get")
        
        if action == "get":
            tasks = get_tasks()
            task_list = "\n".join([f"- {task['title']}" for task in tasks])
            return json.dumps({
                "success": True,
                "message": f"Current tasks:\n{task_list}" if tasks else "No tasks found",
                "tasks": tasks
            })
            
        if action == "add":
            title = args.get("title")
            if not title:
                return json.dumps({
                    "success": False,
                    "error": "Title is required"
                })
                
            result = add_task(
                title=title,
                description=args.get("description", ""),
                due_date=args.get("due_date", "")
            )
            task_list = "\n".join([f"- {task['title']}" for task in result["tasks"]])
            result["message"] = f"Task '{title}' added successfully.\n\nCurrent tasks:\n{task_list}"
            return json.dumps(result)
            
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
    "name": "task_manager",
    "description": "Add and manage tasks",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["get", "add"],
                "description": "Action to perform (get or add tasks)"
            },
            "title": {
                "type": "string",
                "description": "Title of the task (required for add)"
            },
            "description": {
                "type": "string",
                "description": "Optional description of the task"
            },
            "due_date": {
                "type": "string",
                "description": "Optional due date for the task"
            }
        }
    }
}

public_description = "Add and manage tasks"
