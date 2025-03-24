# CSS files borrowed from https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk/tree/main/src/libs/resume_and_cover_builder/resume_style

import aiohttp
import json
import os
from bs4 import BeautifulSoup
from jinja2 import Template
from ..typings.scripty import script_dir

public_description = "Generate a resume, or optimize a resume for a job application."

job_description = ""
original_resume = ""
previous_sections = ""

def generate_resume_section(instructions):
    prompt = f"""You are an EXTREMELY TALENTED resume optimizer that meticulously optimizes resumes for job applications.
    You are to OPTIMIZE the original resume based on the job description.
    You are also given previous sections of the new resume that have already been generated.
    DO NOT mention the job itself, rather EMPHASIZE the skills and expertise that are most relevant to the job description.
    You will ONLY return the optimized section as it will be copy pasted verbatim into the resume.
    DO NOT prepend the section with anything such as "Work experience:" or "Education:" or anything similar.
    This includes NOT using formatting shenanigans such as asterisks.
    Here are the specific instructions for the section you are generating:
    {instructions}
    """
    if job_description:
        prompt += f"\n\n=== Job description ===\n{job_description}"
    if original_resume:
        prompt += f"\n\n=== Original resume ===\n{original_resume}"
    if previous_sections:
        prompt += f"\n\n=== Previous sections ===\n{previous_sections}"

    response = call_ai(prompt)
    return response.get("content")

def generate_html_resume(data):
    styles_dir = os.path.join(script_dir, 'styles')
    style_files = [f for f in os.listdir(styles_dir) if f.startswith('style_') and f.endswith('.css')]
    current_style = style_files[0].replace('style_', '').replace('.css', '')
    
    with open(os.path.join(styles_dir, style_files[0]), 'r', encoding='utf-8') as css_file:
        css = css_file.read()
    with open(os.path.join(script_dir, 'resume_template.jinja'), 'r', encoding='utf-8') as template_file:
        template_text = template_file.read()
    
    template_data = data.copy()
    template_data['css'] = css
    template_data['current_style'] = current_style
    template_data['available_styles'] = [f.replace('style_', '').replace('.css', '') for f in style_files]
    template_data['style_contents'] = []
    
    for style_file in style_files:
        with open(os.path.join(styles_dir, style_file), 'r') as f:
            template_data['style_contents'].append(f.read())
    
    if 'skills' in template_data:
        skills_total = len(template_data['skills'])
        template_data['skills_first_half'] = template_data['skills'][:skills_total//2]
        template_data['skills_second_half'] = template_data['skills'][skills_total//2:]
    
    template = Template(template_text)
    return template.render(**template_data)

async def get_job_description(job_link):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(job_link) as response:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')
                raw_content = soup.get_text(separator=' ', strip=True)
                parsed_raw_content = raw_content.encode('ascii', 'replace').decode('ascii')
                
                prompt = f"Clean up the following job description: {parsed_raw_content}"
                response = call_ai(prompt)
                
                return response.get("content")
    except Exception as e:
        print(f"Error fetching job link: {str(e)}")
        return ""

async def function(args):
    global job_description, original_resume, previous_sections
    
    try:
        if 'job_link' in args:
            job_link = args.pop('job_link')
            job_description = await get_job_description(job_link)
            
            professional_summary_prompt = "Generate a straight to the point professional summary that highlights relevant expertise and skills, clear evidence of value and impact, and a concise narrative."
            professional_summary = generate_resume_section(professional_summary_prompt)
            previous_sections = "Professional Summary:\n" + professional_summary
            args['summary'] = professional_summary
            
            if 'experience' in args and args['experience']:
                optimized_experience = []
                for idx, exp in enumerate(args['experience']):
                    exp_title = f"{exp.get('title', '')} at {exp.get('company', '')}"
                    
                    if 'achievements' in exp and exp['achievements']:
                        optimized_achievements = []
                        achievements_prompt = f"""Optimize the following job experience achievements for the position of {exp_title}. Focus on quantifiable results and skills relevant to the job description. Make each bullet point impactful and concise.
                        You are allowed to make up minor details to better fit the job description, as long as they are believable and a possible outcome of the experience."""
                        
                        original_achievements = "\n".join([f"- {a}" for a in exp['achievements']])
                        achievements_section = generate_resume_section(f"{achievements_prompt}\n\nOriginal achievements:\n{original_achievements}")
                        
                        for line in achievements_section.strip().split('\n'):
                            line = line.strip()
                            if line.startswith('- '):
                                line = line[2:]
                            elif line.startswith('• '):
                                line = line[2:]
                            if line:
                                optimized_achievements.append(line)
                        
                        exp['achievements'] = optimized_achievements
                    
                    optimized_experience.append(exp)
                    
                    exp_summary = f"{exp_title}\n" + "\n".join([f"- {a}" for a in exp.get('achievements', [])])
                    previous_sections += f"\n\nExperience {idx+1}:\n{exp_summary}"
                
                args['experience'] = optimized_experience
        
        resume_html = generate_html_resume(args)
        
        return json.dumps({
            "message": "Resume generated successfully",
            "html": resume_html,
            "second_response": "Here is your resume. Would you like to make any adjustments?"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

object = {
    "name": "resume_optimizer",
    "description": """Generate an HTML resume from provided data.
NEVER, EVER put any information that isn't provided by the user in the resume.
This includes but is not limited to:
- Dates (such as for education)
- Job titles
- LinkedIn profile URL
- Personal website URL

Making up information WILL get the user into legal trouble, even with made up links such as LinkedIn.
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
        },
        "required": ["name", "email", "phone", "location", "experience", "education", "skills"]
    }
}