# CSS files borrowed from https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk/tree/main/src/libs/resume_and_cover_builder/resume_style

import aiohttp
import json
import os
import tkinter as tk
from tkinter import filedialog
import fitz
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

                parsed_raw_content = fix_encoding(raw_content)
                prompt = f"Clean up the following job description: {parsed_raw_content}"
                response = call_ai(prompt)
                
                return response.get("content")
    except Exception as e:
        print(f"Error fetching job link: {str(e)}")
        return ""

def parse_pdf_resume(pdf_path):
    try:
        resume_text = ""
        doc = fitz.open(pdf_path)
        
        for page in doc:
            page_text = page.get_text()
            fixed_text = fix_encoding(page_text)
            resume_text += fixed_text
        
        return resume_text
    except Exception as e:
        print(f"Error parsing PDF: {str(e)}")
        return ""

def fix_encoding(text):
    replacements = {
        "â€™": "'",
        "â€\"": "–",
        "â€œ": """,
        "â€": """,
        "Ã©": "é",
        "Ã¨": "è",
        "Ã«": "ë",
        "Ã¯": "ï",
        "Ã®": "î",
        "Ã´": "ô",
        "Ã»": "û",
        "Ã¹": "ù",
        "Ã¢": "â",
        "Ãª": "ê",
        "Ã§": "ç"
    }
    
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    try:
        return text.encode('cp1252', errors='replace').decode('utf-8', errors='replace')
    except Exception:
        pass
    
    try:
        return text.encode('latin1', errors='replace').decode('utf-8', errors='replace')
    except Exception:
        pass
    
    return text.replace('', '')

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file_path = filedialog.askopenfilename(
        title="Select Resume PDF File",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    root.destroy()
    return file_path

async def function(args):
    global job_description, original_resume, previous_sections
    
    try:
        # Add preprocessing for manually input text
        if 'resume_text' in args and args['resume_text']:
            original_resume = fix_encoding(args.pop('resume_text'))
        else:
            resume_path = open_file_dialog()
            
            if not resume_path:
                return json.dumps({
                    "error": "No file selected. Please try again and select a resume PDF file."
                })
                
            original_resume = parse_pdf_resume(resume_path)

        if 'job_description' in args:
            job_description = fix_encoding(args.pop('job_description'))

        resume_parser_tool = {
            "type": "function",
            "function": {
                "name": "parse_resume",
                "description": "Parse and structure resume content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Full name of the candidate"},
                        "email": {"type": "string", "description": "Email address"},
                        "phone": {"type": "string", "description": "Phone number"},
                        "location": {"type": "string", "description": "Location/address"},
                        "linkedin": {"type": "string", "description": "LinkedIn profile URL"},
                        "website": {"type": "string", "description": "Personal website URL"},
                        "summary": {"type": "string", "description": "Professional summary"},
                        "skills": {"type": "array", "items": {"type": "string"}, "description": "List of skills"},
                        "achievements": {"type": "array", "items": {"type": "string"}, "description": "List of key achievements"},
                        "experience": {
                            "type": "array", 
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "Job title"},
                                    "company": {"type": "string", "description": "Company name"},
                                    "location": {"type": "string", "description": "Job location"},
                                    "dates": {"type": "string", "description": "Employment dates"},
                                    "achievements": {"type": "array", "items": {"type": "string"}, "description": "Job achievements"}
                                }
                            },
                            "description": "Work experience"
                        },
                        "education": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "degree": {"type": "string", "description": "Degree obtained"},
                                    "school": {"type": "string", "description": "School name"},
                                    "location": {"type": "string", "description": "School location"},
                                    "dates": {"type": "string", "description": "Education dates"}
                                }
                            },
                            "description": "Education history"
                        },
                        "projects": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Project name"},
                                    "url": {"type": "string", "description": "Project URL"},
                                    "dates": {"type": "string", "description": "Project dates"},
                                    "description": {"type": "string", "description": "Project description"},
                                    "technologies": {"type": "array", "items": {"type": "string"}, "description": "Technologies used"}
                                }
                            },
                            "description": "Projects"
                        },
                        "certifications": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Certification name"},
                                    "issuer": {"type": "string", "description": "Certification issuer"},
                                    "date": {"type": "string", "description": "Date obtained"}
                                }
                            },
                            "description": "Professional certifications and credentials"
                        }
                    },
                    "required": ["name", "email", "phone", "location", "skills", "experience", "education"]
                }
            }
        }

        prompt = f"Parse this resume into a structured format for optimization:\n\n{original_resume}"
        response = call_ai(
            prompt,
            tools=[resume_parser_tool],
            tool_choice="required"
        )
        
        if response.get("tool_calls"):
            args.update(json.loads(response["tool_calls"][0]["function"]["arguments"]))
            print(args)

        if job_description:
            professional_summary_prompt = "Generate a straight to the point professional summary that highlights relevant expertise and skills, clear evidence of value and impact, and a concise narrative."
            professional_summary = generate_resume_section(professional_summary_prompt)
            previous_sections = "Professional Summary:\n" + professional_summary
            args['summary'] = professional_summary
            
            if 'achievements' in args and args['achievements']:
                optimized_achievements = []
                achievements_prompt = """Optimize the following key achievements to highlight accomplishments that are most relevant to the job description. 
                Focus on quantifiable results and impactful contributions. Make each bullet point concise and impressive.
                You are allowed to make up minor details to better fit the job description, as long as they are believable and a possible outcome of the person's career."""
                
                original_achievements = "\n".join([f"- {a}" for a in args['achievements']])
                achievements_section = generate_resume_section(f"{achievements_prompt}\n\nOriginal achievements:\n{original_achievements}")
                
                for line in achievements_section.strip().split('\n'):
                    line = line.strip()
                    if line.startswith('- '):
                        line = line[2:]
                    elif line.startswith('• '):
                        line = line[2:]
                    if line:
                        optimized_achievements.append(line)
                
                args['achievements'] = optimized_achievements
                
                achievements_summary = "Key Achievements:\n" + "\n".join([f"- {a}" for a in optimized_achievements])
                previous_sections += f"\n\n{achievements_summary}"
            
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
        
            if 'projects' in args and args['projects']:
                optimized_projects = []
                for idx, proj in enumerate(args['projects']):
                    proj_title = f"{proj.get('name', '')}"
                    
                    if 'description' in proj and proj['description']:
                        description_prompt = f"""Optimize the following project description for {proj_title}. Focus on the technical aspects, skills, and outcomes most relevant to the job description.
                        Highlight technologies used and quantifiable results if available. Make the description impactful and concise.
                        You are allowed to make up minor details to better fit the job description, as long as they are believable and technically feasible."""
                        
                        original_description = proj['description']
                        optimized_description = generate_resume_section(f"{description_prompt}\n\nOriginal description:\n{original_description}")
                        proj['description'] = optimized_description
                    
                    optimized_projects.append(proj)
                    
                    proj_summary = f"Project {idx+1}: {proj_title}\n{proj.get('description', '')}"
                    previous_sections += f"\n\n{proj_summary}"
                
                args['projects'] = optimized_projects
            
            # Add optimization for certifications if present
            if 'certifications' in args and args['certifications']:
                optimized_certifications = []
                for idx, cert in enumerate(args['certifications']):
                    cert_title = f"{cert.get('name', '')} - {cert.get('issuer', '')}"
                    
                    certification_prompt = f"""Optimize the following certification entry. 
                    Focus on making it relevant to the job description while maintaining accuracy.
                    Keep the certification details factual but highlight aspects most valuable for the role."""
                    
                    original_cert = json.dumps(cert)
                    optimized_cert_response = generate_resume_section(f"{certification_prompt}\n\nOriginal certification:\n{original_cert}")
                    
                    try:
                        optimized_cert = json.loads(optimized_cert_response)
                        optimized_certifications.append(optimized_cert)
                    except:
                        # If parsing fails, keep original certification
                        optimized_certifications.append(cert)
                    
                    cert_summary = f"Certification {idx+1}: {cert_title}"
                    previous_sections += f"\n\n{cert_summary}"
                
                args['certifications'] = optimized_certifications
        
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
    "description": "Optimize a resume for a job application.",
    "parameters": {
        "type": "object",
        "properties": {
            "job_description": {"type": "string", "description": "The job description text for which to optimize the resume."},
            "resume_text": {"type": "string", "description": "Optional resume text if provided by the user."}
        },
        "required": ["job_description"]
    }
}