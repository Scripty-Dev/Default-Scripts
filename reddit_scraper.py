import requests
import json
import time
import re

public_description = "Fetch posts and comments from any subreddit with customizable options."

def clean_text(text):
    """Remove extra whitespace and clean up text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_preview(text, max_length=150):
    """Return a preview of text with limited length"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def scrape_subreddit(subreddit, post_limit=100, sort_by="hot"):
    """
    Scrape posts from a subreddit without using API credentials.
    
    Args:
        subreddit (str): Name of the subreddit to scrape (without r/)
        post_limit (int): Maximum number of posts to retrieve
        sort_by (str): How to sort posts ('hot', 'new', 'top', 'rising')
    
    Returns:
        list: List of post dictionaries with metadata
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
                    'id': post_data['id'],
                    'title': post_data['title'],
                    'score': post_data['score'],
                    'url': f"https://www.reddit.com{post_data['permalink']}",
                    'created_utc': post_data['created_utc'],
                    'author': post_data['author'],
                    'num_comments': post_data['num_comments'],
                    'text': get_preview(clean_text(post_data['selftext'])),
                    'subreddit': post_data['subreddit'],
                    'is_video': post_data['is_video'],
                    'upvote_ratio': post_data['upvote_ratio'],
                    'permalink': post_data['permalink']
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

def scrape_comments(post_permalink, comment_limit=100, include_nested=True):
    """
    Scrape comments from a Reddit post using the post's permalink.
    
    Args:
        post_permalink (str): The permalink to the Reddit post (e.g., "/r/subreddit/comments/id/title/")
        comment_limit (int): Maximum number of comments to retrieve
        include_nested (bool): Whether to include nested comments (replies)
    
    Returns:
        list: List of comment dictionaries with metadata
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Ensure the permalink starts with /r/ and ends with .json
    if not post_permalink.startswith('/'):
        post_permalink = '/' + post_permalink
    if not post_permalink.startswith('/r/'):
        post_permalink = '/r/' + post_permalink.lstrip('/')
    if not post_permalink.endswith('.json'):
        post_permalink = post_permalink.rstrip('/') + '.json'
    
    url = f"https://www.reddit.com{post_permalink}"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            print("Rate limited. Waiting before trying again...")
            time.sleep(5)
            response = requests.get(url, headers=headers)
            
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return []
            
        data = response.json()
        
        # Reddit returns an array with 2 elements: 
        # [0] contains the post, [1] contains the comments
        if len(data) < 2 or not data[1].get('data') or not data[1]['data'].get('children'):
            print("No comments found or unexpected data structure")
            return []
        
        comments = []
        collected = 0
        
        # Extract comments recursively
        def extract_comments(comment_list, depth=0):
            nonlocal collected
            result = []
            
            for comment in comment_list:
                # Skip non-comment types (e.g., "more" type)
                if comment['kind'] != 't1':
                    continue
                    
                comment_data = comment['data']
                
                # Skip deleted or removed comments
                if comment_data['author'] == '[deleted]':
                    continue
                
                # Add this comment
                result.append({
                    'id': comment_data['id'],
                    'author': comment_data['author'],
                    'body': clean_text(comment_data['body']),
                    'score': comment_data['score'],
                    'created_utc': comment_data['created_utc'],
                    'depth': depth,
                    'permalink': comment_data['permalink']
                })
                
                collected += 1
                if collected >= comment_limit:
                    return result
                
                # Process replies recursively if needed
                if include_nested and comment_data.get('replies') and isinstance(comment_data['replies'], dict):
                    replies_data = comment_data['replies'].get('data', {}).get('children', [])
                    nested_comments = extract_comments(replies_data, depth + 1)
                    result.extend(nested_comments)
                    
                    if collected >= comment_limit:
                        return result
            
            return result
            
        # Start with top-level comments
        top_comments = data[1]['data']['children']
        all_comments = extract_comments(top_comments)
        
        return all_comments
    
    except Exception as e:
        print(f"Error scraping comments: {str(e)}")
        return []

def search_subreddit(subreddit, keywords, post_limit=100, sort_by="hot", include_comments=False, comment_limit=50):
    """
    Search a subreddit for posts containing specific keywords and optionally fetch comments.
    
    Args:
        subreddit (str): Name of the subreddit to search
        keywords (list): List of keywords to search for
        post_limit (int): Maximum number of posts to retrieve
        sort_by (str): How to sort posts ('hot', 'new', 'top', 'rising')
        include_comments (bool): Whether to include comments for matching posts
        comment_limit (int): Maximum number of comments to retrieve per post
    
    Returns:
        list: List of matching posts with optional comments
    """
    # Make keywords lowercase for case-insensitive matching
    lowercase_keywords = [k.lower() for k in keywords]
    
    # Get posts from the subreddit
    posts = scrape_subreddit(subreddit, post_limit, sort_by)
    
    # Filter posts based on keywords
    matching_posts = []
    for post in posts:
        post_text = (post['title'] + ' ' + post['text']).lower()
        if any(keyword in post_text for keyword in lowercase_keywords):
            # If comments are requested, fetch them
            if include_comments:
                post['comments'] = scrape_comments(post['permalink'], comment_limit)
            matching_posts.append(post)
    
    return matching_posts

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
        include_comments = args.get("include_comments", False)
        comment_limit = int(args.get("comment_limit", 50))
        keywords = args.get("keywords", None)
        
        # Validate sort_by
        valid_sorts = ["hot", "new", "top", "rising"]
        if sort_by not in valid_sorts:
            sort_by = "hot"
        
        # If keywords are provided, perform a search
        if keywords:
            if isinstance(keywords, str):
                keywords = [keyword.strip() for keyword in keywords.split(",")]
            results = search_subreddit(
                subreddit, 
                keywords, 
                limit, 
                sort_by, 
                include_comments, 
                comment_limit
            )
            message = f"Found {len(results)} matching posts for keywords: {', '.join(keywords)}"
        # Otherwise, just get posts (with optional comments)
        else:
            posts = scrape_subreddit(subreddit, limit, sort_by)
            
            # If comments are requested, fetch them for each post
            if include_comments:
                for post in posts:
                    post['comments'] = scrape_comments(post['permalink'], comment_limit)
            
            results = posts
            message = f"Retrieved {len(results)} posts from r/{subreddit}"
        
        return json.dumps({
            "success": True,
            "message": message,
            "results": results
        })
        
    except Exception as e: 
        return json.dumps({
            "success": False,
            "error": str(e)
        })

object = {
    "name": "get_reddit_content",
    "description": "Fetch posts and comments from a specified subreddit with customizable filtering",
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
            },
            "include_comments": {
                "type": "boolean",
                "description": "Whether to include comments for each post (default: false)"
            },
            "comment_limit": {
                "type": "integer",
                "description": "Maximum number of comments to retrieve per post (default: 50)"
            },
            "keywords": {
                "type": "string",
                "description": "Comma-separated keywords to filter posts (e.g., 'fintech,job,interview')"
            }
        },
        "required": ["subreddit"]
    }
}

# Example usage from command line
if __name__ == "__main__":
    import sys
    import asyncio
    
    # Default values
    subreddit = "cscareerquestions"
    sort_by = "new"
    limit = 100
    include_comments = False
    comment_limit = 50
    keywords = None
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        subreddit = sys.argv[1]
    if len(sys.argv) > 2:
        sort_by = sys.argv[2]
    if len(sys.argv) > 3:
        limit = int(sys.argv[3])
    if len(sys.argv) > 4:
        include_comments = sys.argv[4].lower() == "true"
    if len(sys.argv) > 5:
        comment_limit = int(sys.argv[5])
    if len(sys.argv) > 6:
        keywords = sys.argv[6]
        
    # Call the function
    args = {
        "subreddit": subreddit,
        "sort_by": sort_by,
        "limit": limit,
        "include_comments": include_comments,
        "comment_limit": comment_limit
    }
    
    if keywords:
        args["keywords"] = keywords
    
    # Run the async function
    result = asyncio.run(function(args))
    print(result)