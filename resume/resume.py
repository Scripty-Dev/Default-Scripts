from ..typings.scripty import script_dir
from jinja2 import Template
import json
import os

async def func(args):
    try:
        builder = ResumeBuilder(script_dir)
        result = builder.update_resume_data(args)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

class ResumeBuilder:
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.data_file = os.path.join(script_dir, 'resume_data.json')
        self.styles_dir = os.path.join(script_dir, 'styles')
        self.style_files = [f for f in os.listdir(self.styles_dir) if f.startswith('style_') and f.endswith('.css')]
        self.current_style = self.style_files[0].replace('style_', '').replace('.css', '')
        
        with open(os.path.join(self.styles_dir, self.style_files[0]), 'r') as css_file:
            self.css = css_file.read()
        with open(os.path.join(script_dir, 'resume_template.jinja'), 'r') as template_file:
            self.template = template_file.read()

    def update_resume_data(self, new_data):
        current_data = self._load_current_data()
        current_data.update(new_data)
        self._save_current_data(current_data)
        
        missing_fields = self._get_missing_fields(current_data)
        
        if not missing_fields["required"]:
            html = self.generate_resume(current_data)
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            return {
                "message": "All required data collected",
                "missing_optional": missing_fields["optional"],
                "html": html,
                "second_response": "Here is the resume. Would you like to make any adjustments?"
            }
        
        return {
            "message": "Additional fields required",
            "missing_fields": missing_fields
        }

    def _load_current_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_current_data(self, data):
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def _get_missing_fields(self, current_data):
        required_fields = ["name", "email", "phone", "location", "linkedin", 
                          "experience", "education", "skills"]
        optional_fields = ["summary", "website"]
        
        missing = {
            "required": [field for field in required_fields if field not in current_data],
            "optional": [field for field in optional_fields if field not in current_data]
        }
        return missing

    def generate_resume(self, data):
        data = data.copy()
        data['css'] = self.css
        data['current_style'] = self.current_style
        data['available_styles'] = [f.replace('style_', '').replace('.css', '') for f in self.style_files]
        data['style_contents'] = []
        
        for style_file in self.style_files:
            with open(os.path.join(self.styles_dir, style_file), 'r') as f:
                data['style_contents'].append(f.read())
                
        skills_total = len(data['skills'])
        data['skills_first_half'] = data['skills'][:skills_total//2]
        data['skills_second_half'] = data['skills'][skills_total//2:]
        template = Template(self.template)
        return template.render(**data)

object = {
    "name": "generate_resume",
    "description": """Generate an HTML resume from provided data.
You don't need to include everything at once, you can update the resume later by asking the user.
Do not put any information that is not provided by the user in the resume.""",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Full name"},
            "email": {"type": "string", "description": "Email address"},
            "phone": {"type": "string", "description": "Phone number"},
            "location": {"type": "string", "description": "Location"},
            "linkedin": {"type": "string", "description": "LinkedIn profile URL"},
            "summary": {"type": "string", "description": "Professional summary", "optional": True},
            "website": {"type": "string", "description": "Personal website URL", "optional": True},

            "experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "company": {"type": "string"},
                        "location": {"type": "string"},
                        "dates": {"type": "string"},
                        "achievements": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "degree": {"type": "string"},
                        "school": {"type": "string"},
                        "location": {"type": "string"},
                        "dates": {"type": "string"}
                    }
                }
            },
            "skills": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
}
