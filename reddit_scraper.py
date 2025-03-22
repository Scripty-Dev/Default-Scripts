import requests
import json
import time
import re

public_description = "Fetch posts from any subreddit with customizable sorting and limits."

def clean_text(text):
    # Remove extra whitespace and clean up text
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_preview(text, max_length=150):
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def scrape_subreddit(subreddit, post_limit=100, sort_by="hot"):
    """
    Scrape posts from a subreddit without using API credentials.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    base_url = f"https://www.reddit.com/r/{subreddit}/{sort_by}.json"
    params = {"limit": min(100, post_limit)}
    
    all_posts = []
    
    try:
        while len(all_posts) < post_limit:
            response = requests.get(base_url, headers=headers, params=params)
            
            # Handle potential rate limiting
            if response.status_code == 429:
                print("Rate limited. Waiting before trying again...")
                time.sleep(5)
                continue
                
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                break
                
            data = response.json()
            posts = data['data']['children']
            
            if not posts:
                break
                
            for post in posts:
                post_data = post['data']
                all_posts.append({
                    'title': post_data['title'],
                    'score': post_data['score'],
                    'url': f"https://www.reddit.com{post_data['permalink']}",
                    'created_utc': post_data['created_utc'],
                    'author': post_data['author'],
                    'num_comments': post_data['num_comments'],
                    'text': get_preview(clean_text(post_data['selftext'])),
                    'subreddit': post_data['subreddit'],
                    'is_video': post_data['is_video'],
                    'upvote_ratio': post_data['upvote_ratio']
                })
                
                if len(all_posts) >= post_limit:
                    break
                    
            # For pagination - get the 'after' token
            after = data['data']['after']
            if not after:
                break
                
            params['after'] = after
            time.sleep(2)  # Be gentle with requests to avoid rate limiting
    
    except Exception as e:
        print(f"Error scraping r/{subreddit}: {str(e)}")
        
    return all_posts

async def function(args):
    try:
        # Parse arguments
        subreddit = args.get("subreddit", "")
        if not subreddit:
            return json.dumps({
                "success": False,
                "error": "Subreddit name is required"
            })
            
        limit = int(args.get("limit", 100))
        sort_by = args.get("sort_by", "hot").lower()
        
        # Validate sort_by
        valid_sorts = ["hot", "new", "top", "rising"]
        if sort_by not in valid_sorts:
            sort_by = "hot"
        
        # Perform the scrape
        posts = scrape_subreddit(subreddit, limit, sort_by)
        
        return json.dumps({
            "success": True,
            "message": posts
        })
        
    except Exception as e: 
        return json.dumps({
            "success": False,
            "error": str(e)
        })

object = {
    "name": "get_reddit_posts",
    "description": "Fetch posts from a specified subreddit with customizable sorting and limits",
    "parameters": {
        "type": "object",
        "properties": {
            "subreddit": {
                "type": "string", 
                "description": "Name of the subreddit to scrape (without 'r/')"
            },
            "limit": {
                "type": "integer", 
                "description": "Maximum number of posts to return (default: 100)"
            },
            "sort_by": {
                "type": "string",
                "description": "How to sort posts: 'hot', 'new', 'top', or 'rising' (default: 'hot')"
            }
        },
        "required": ["subreddit"]
    }
}