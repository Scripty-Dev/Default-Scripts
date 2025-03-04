# CSS files borrowed from https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk/tree/main/src/libs/resume_and_cover_builder/resume_style

from ..typings.scripty import script_dir
from bs4 import BeautifulSoup
from jinja2 import Template
import aiohttp
import json
import os

public_description = "Generate a resume, or optimize a resume for a job application."

async def function(args):
    try:
        builder = ResumeBuilder(script_dir)
        if 'job_link' in args:
            job_link = args.pop('job_link')
            builder.update_resume_data(args)
            result = await builder.optimize_for_job(args | {'job_link': job_link}, call_ai)
        else:
            result = builder.update_resume_data(args)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

class ResumeBuilder:
    def __init__(self, script_dir):
        self.script_dir = script_dir
        self.styles_dir = os.path.join(script_dir, 'styles')
        self.style_files = [f for f in os.listdir(self.styles_dir) if f.startswith('style_') and f.endswith('.css')]
        self.current_style = self.style_files[0].replace('style_', '').replace('.css', '')
        
        with open(os.path.join(self.styles_dir, self.style_files[0]), 'r', encoding='utf-8') as css_file:
            self.css = css_file.read()
        with open(os.path.join(script_dir, 'resume_template.jinja'), 'r', encoding='utf-8') as template_file:
            self.template = template_file.read()

    def update_resume_data(self, new_data):
        current_data = {}
        current_data.update(new_data)
        
        missing_fields = self._get_missing_fields(current_data)
        
        if len(missing_fields["required"]) == 0:
            html = self.generate_resume(current_data)
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

    async def optimize_for_job(self, args, call_ai):
        if 'job_link' not in args:
            return {"error": "No job link provided"}

        current_data = {}
        current_data.update({k: v for k, v in args.items() if k != 'job_link'})

        try:
            
            async with aiohttp.ClientSession() as session:
                async with session.get(args['job_link']) as response:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    job_content = soup.get_text(separator=' ', strip=True)

            prompt = f"""Given this job posting:
{job_content}
            
And this current resume data:
{json.dumps(current_data, indent=2)}
            
Optimize this resume to better match the job requirements."""
            
            tool = {
                "type": "function",
                "function": {
                    "name": "optimize_resume",
                    "description": "Optimize resume data to match job requirements",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"},
                            "location": {"type": "string"},
                            "linkedin": {"type": "string"},
                            "summary": {"type": "string"},
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
                            "skills": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                }
            }

            response = call_ai(prompt, tools=[tool], tool_choice="required")
            if response.get("tool_calls"):
                optimized_data = json.loads(response["tool_calls"][0]["function"]["arguments"])
                current_data.update(optimized_data)
            
            html = self.generate_resume(current_data)
            return {
                "message": "Resume optimized for job posting",
                "html": html,
                "second_response": "Here is your optimized resume. Would you like to make any adjustments?"
            }
            
        except Exception as e:
            return {"error": str(e)}

object = {
    "name": "generate_resume",
    "description": """Generate an HTML resume from provided data.
You don't need to include everything at once, unless an existing resume is provided.
Don't put any information that isn't provided by the user in the resume.
The arguments aren't required, so don't call the tool with N/A or Not provided or anything similar.""",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Full name"},
            "email": {"type": "string", "description": "Email address"},
            "phone": {"type": "string", "description": "Phone number"},
            "location": {"type": "string", "description": "Location"},
            "linkedin": {"type": "string", "description": "LinkedIn profile URL"},
            "summary": {"type": "string", "description": "Professional summary"},
            "website": {"type": "string", "description": "Personal website URL"},
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
            },
            "job_link": {
                "type": "string",
                "description": "Optional job posting URL to optimize resume for"
            }
        }
    }
}
