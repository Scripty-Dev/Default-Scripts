from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import os
import hashlib
import json
from pathlib import Path
from jinja2 import Template

def get_base_directory():
    """Get the base directory in user's home folder"""
    home = str(Path.home())
    base = os.path.join(home, "Job Search Results")
    os.makedirs(base, exist_ok=True)
    return base

def generate_jobs_html(jobs_data):
    """Generate HTML table view of jobs data"""
    html_template = """
    <style>
        .jobs-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #1f1f1f;
            color: #e8eaed;
        }
        .jobs-table thead tr {
            border-bottom: 2px solid #5f6368;
            color: #e8eaed;
            text-align: left;
        }
        .jobs-table th,
        .jobs-table td {
            padding: 12px 15px;
            border: 1px solid #3c4043;
        }
        .jobs-table tbody tr {
            border-bottom: 1px solid #3c4043;
        }
        .jobs-table tbody tr:hover {
            background-color: #292929;
        }
        .jobs-table a {
            color: #8ab4f8;
            text-decoration: none;
        }
        .jobs-table a:hover {
            text-decoration: underline;
        }
        /* Wrapper to ensure dark background extends fully */
        .table-wrapper {
            background-color: #1f1f1f;
            padding: 20px;
            border-radius: 8px;
        }
    </style>
    <div class="table-wrapper">
        <table class="jobs-table">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Date Posted</th>
                    <th>Salary</th>
                    <th>Type</th>
                    <th>Remote</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for job in jobs %}
                <tr>
                    <td><a href="{{ job.job_url }}" target="_blank">{{ job.title }}</a></td>
                    <td>{{ job.company }}</td>
                    <td>{{ job.location }}</td>
                    <td>{{ job.date_posted }}</td>
                    <td>{{ job.salary }}</td>
                    <td>{{ job.job_type if job.job_type else 'N/A' }}</td>
                    <td>{{ 'Yes' if job.is_remote else 'No' }}</td>
                    <td>{{ job.status }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    """
    template = Template(html_template)
    return template.render(jobs=jobs_data)

def save_description(description, descriptions_dir):
    """Save description to a separate file and return its ID"""
    if pd.isna(description) or description.strip() == '':
        return None
        
    desc_id = hashlib.md5(str(description).encode()).hexdigest()[:10]
    filepath = os.path.join(descriptions_dir, f"{desc_id}.txt")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(description))
    
    return desc_id

def format_salary(row):
    """Format salary from min/max amounts into readable string"""
    try:
        if pd.isna(row.get('min_amount')):
            return 'Not specified'
        
        min_amt = str(row['min_amount']) if pd.notna(row.get('min_amount')) else ''
        max_amt = str(row['max_amount']) if pd.notna(row.get('max_amount')) else ''
        currency = str(row['currency']) if pd.notna(row.get('currency')) else 'CAD'  # Default to CAD for Toronto
        interval = str(row['interval']) if pd.notna(row.get('interval')) else 'yearly'
        
        if min_amt and max_amt:
            return f"{min_amt} - {max_amt} {currency} {interval}"
        elif min_amt:
            return f"{min_amt} {currency} {interval}"
        else:
            return 'Not specified'
    except:
        return 'Not specified'

def parse_time_expression(time_str):
    """Parse natural language time expression into hours"""
    if not time_str:
        return 72  # Default value
        
    time_str = time_str.lower().strip()
    if time_str.isdigit():
        return int(time_str)  # Assume hours if just a number
        
    parts = time_str.split()
    try:
        value = int(parts[0])
        unit = parts[1].lower().rstrip('s')  # Remove plural 's' if present
        
        multipliers = {
            'hour': 1,
            'day': 24,
            'week': 24 * 7,
            'month': 24 * 30,  # Approximate
            'year': 24 * 365   # Approximate
        }
        
        if unit in multipliers:
            return value * multipliers[unit]
        return 72  # Default if unit not recognized
    except:
        return 72  # Default if parsing fails

def search_jobs(job_title, location, results_wanted=100, time_range=None):
    """Main function to search for jobs"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        base_dir = get_base_directory()
        search_dir = os.path.join(base_dir, f"search_{timestamp}")
        os.makedirs(search_dir, exist_ok=True)

        hours_old = parse_time_expression(time_range)

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
            hours_old=hours_old,
            description_format="markdown",
            fetch_full_description=True,
            return_as_df=True,
            delay=[2, 5],
            random_headers=True
        )
        
        # Convert jobs DataFrame to records and back to ensure numpy arrays are converted
        jobs_records = jobs.to_dict('records')
        filtered_jobs = pd.DataFrame(jobs_records)
        
        # Convert date_posted to string format, handling both datetime and string inputs
        if 'date_posted' in filtered_jobs.columns:
            filtered_jobs['date_posted'] = pd.to_datetime(filtered_jobs['date_posted']).dt.strftime('%Y-%m-%d')
        
        filtered_jobs['salary'] = filtered_jobs.apply(format_salary, axis=1)
        filtered_jobs['status'] = 'Not Applied'
        
        relevant_columns = [
            'title', 'company', 'location', 'date_posted', 'job_type',
            'is_remote', 'company_industry', 'job_url', 'salary', 'status'
        ]
        
        existing_columns = [col for col in relevant_columns if col in filtered_jobs.columns]
        filtered_jobs = filtered_jobs[existing_columns]
        
        filtered_jobs = filtered_jobs.drop_duplicates(
            subset=['title', 'company', 'job_url'], 
            keep='first'
        )
        
        if 'date_posted' in filtered_jobs.columns:
            filtered_jobs = filtered_jobs.sort_values('date_posted', ascending=False)
        
        csv_path = os.path.join(search_dir, "jobs.csv")
        filtered_jobs.to_csv(csv_path, index=False)
        
        metadata = {
            'timestamp': timestamp,
            'total_jobs': len(filtered_jobs),
            'search_term': search_term,
            'location': location,
            'date_range': time_range or '72 hours'
        }
        with open(os.path.join(search_dir, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=2)

        results = filtered_jobs.to_dict('records')
        html_view = generate_jobs_html(results)
        
        print(f"\nFound {len(filtered_jobs)} jobs")
        print(f"Results saved to: {csv_path}")
        
        time_range_str = time_range or "72 hours"
        result = {
            "success": True,
            "message": f"Found {len(filtered_jobs)} jobs for '{job_title}' in {location} from the past {time_range_str}.\nResults saved to: {csv_path}",
            "csv_path": csv_path,
            "html": html_view
        }
            
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# API definition
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
            },
            "time_range": {
                "type": "string",
                "description": "Time range for job posts (e.g., '3 days', '2 weeks', '1 month', default: '72 hours')",
                "default": "72 hours"
            }
        },
        "required": ["job_title", "location"]
    }
}

async def func(args):
    """Handler function for the API"""
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
            results_wanted=args.get("results_wanted", 100),
            time_range=args.get("time_range")
        )
        return json.dumps(result)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })
