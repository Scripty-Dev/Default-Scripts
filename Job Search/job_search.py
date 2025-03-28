from ..typings.scripty import script_dir
from jobspy import scrape_jobs
from jinja2 import Template
from pathlib import Path
import pandas as pd
import hashlib
import json
import os

public_description = "Search for jobs across multiple platforms and save results to CSV."

def get_base_directory():
    home = str(Path.home())
    base = os.path.join(home, "Job Search Results")
    os.makedirs(base, exist_ok=True)
    return base

def generate_jobs_html(jobs_data):
    with open(os.path.join(script_dir, 'job_list_template.jinja'), 'r') as file:
        html_template = file.read()
    template = Template(html_template)
    return template.render(jobs=jobs_data)

def save_description(description, descriptions_dir):
    if pd.isna(description) or description.strip() == '':
        return None
        
    desc_id = hashlib.md5(str(description).encode()).hexdigest()[:10]
    filepath = os.path.join(descriptions_dir, f"{desc_id}.txt")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(description))
    
    return desc_id

def format_salary(row):
    try:
        min_amt = row.get('min_amount')
        max_amt = row.get('max_amount')
        
        if pd.isna(min_amt) and pd.isna(max_amt):
            return 'Not specified'
        
        currency = str(row.get('currency', 'CAD')) if pd.notna(row.get('currency')) else 'CAD'
        interval = str(row.get('interval', 'yearly')) if pd.notna(row.get('interval')) else 'yearly'
        
        if pd.notna(min_amt) and pd.notna(max_amt):
            return f"{int(min_amt):,} - {int(max_amt):,} {currency} {interval}"
        elif pd.notna(min_amt):
            return f"{int(min_amt):,} {currency} {interval}"
        elif pd.notna(max_amt):
            return f"{int(max_amt):,} {currency} {interval}"
        else:
            return 'Not specified'
    except:
        return 'Not specified'

def clean_dataframe(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Not specified')
    return df

def search_jobs(job_title, location, results_wanted=100):
    try:
        import datetime
        
        base_dir = get_base_directory()
        
        # Create timestamped folder name
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        search_dir = os.path.join(base_dir, f"search_{timestamp}")
        os.makedirs(search_dir, exist_ok=True)

        city = location.split(',')[0].strip()
        country = "Canada" if "ON" in location.upper() else "USA"
        
        search_term = f'"{job_title}"'
        google_search_term = f"{job_title} jobs in {city}"

        print(f"Searching for {job_title} jobs in {location}...")
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
            search_term=search_term,
            location=location,
            google_search_term=google_search_term,
            country_indeed=country,
            results_wanted=results_wanted,
            description_format="markdown",
            fetch_full_description=True,
            return_as_df=True,
            delay=[2, 5],
            random_headers=True
        )
        
        jobs_records = jobs.to_dict('records')
        filtered_jobs = pd.DataFrame(jobs_records)
        
        if 'job_type' in filtered_jobs.columns:
            filtered_jobs['job_type'] = filtered_jobs['job_type'].str.capitalize().fillna('Not specified')
        
        filtered_jobs['salary'] = filtered_jobs.apply(format_salary, axis=1)
        
        relevant_columns = [
            'title', 'company', 'location', 'job_type',
            'is_remote', 'company_industry', 'job_url', 'salary'
        ]
            
        existing_columns = [col for col in relevant_columns if col in filtered_jobs.columns]
        filtered_jobs = filtered_jobs[existing_columns]
        
        filtered_jobs = filtered_jobs.drop_duplicates(
            subset=['title', 'company', 'job_url'], 
            keep='first'
        )
        
        filtered_jobs = clean_dataframe(filtered_jobs)
        
        csv_path = os.path.join(search_dir, "jobs.csv")
        filtered_jobs.to_csv(csv_path, index=False)
        
        metadata = {
            'total_jobs': len(filtered_jobs),
            'search_term': search_term,
            'location': location,
            'timestamp': timestamp,
            'search_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(os.path.join(search_dir, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=2)

        results = filtered_jobs.to_dict('records')
        html_view = generate_jobs_html(results)
        
        print(f"\nFound {len(filtered_jobs)} jobs")
        print(f"Results saved to: {csv_path}")
        
        top_jobs_text = ""
        for i, job in enumerate(results[:3], 1):
            company = job.get('company', 'Not specified')
            title = job.get('title', 'Not specified')
            location = job.get('location', 'Not specified')
            salary = job.get('salary', 'Not specified')
            job_type = job.get('job_type', 'Not specified')
            
            top_jobs_text += f"{i}. {title} at {company}\n   Location: {location}\n   Salary: {salary}\n   Type: {job_type}\n\n"
        
        result = {
            "success": True,
            "message": f"""Found {len(filtered_jobs)} jobs for '{job_title}' in {location}.
Top 3 jobs:
{top_jobs_text}
Results saved to: {csv_path}""",
            "csv_path": csv_path,
            "html": html_view
        }
            
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    
async def function(args):
    try:
        if not args.get("job_title"):
            return json.dumps({
                "success": False,
                "error": "Job title is required"
            })
            
        if not args.get("location"):
            return json.dumps({
                "success": False,
                "error": "Location is required"
            })
            
        result = search_jobs(
            args["job_title"],
            args["location"],
            results_wanted=args.get("results_wanted", 100)
        )
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

object = {
    "name": "job_search",
    "description": "Search for jobs across multiple platforms and save results to CSV.",
    "parameters": {
        "type": "object",
        "properties": {
            "job_title": {
                "type": "string",
                "description": "Job title to search for (e.g., 'software engineer', 'data scientist')"
            },
            "location": {
                "type": "string",
                "description": "Location to search in (e.g., 'Toronto, ON', 'San Francisco, CA')"
            },
            "results_wanted": {
                "type": "integer",
                "description": "Number of results to fetch (default: 100)",
                "default": 100
            }
        },
        "required": ["job_title", "location"]
    }
}
