import feedparser
import re
import json

public_description = "Fetch latest startup and tech news from multiple sources."

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = ' '.join(cleantext.split())
    return cleantext

def get_first_sentences(text, max_sentences=2):
    sentences = text.split('. ')
    result = '. '.join(sentences[:max_sentences])
    if not result.endswith('.'):
        result += '.'
        
    return result

def get_startup_news():
    feeds = {
        'techcrunch': 'https://techcrunch.com/feed/',
        'ycombinator': 'https://news.ycombinator.com/rss',
        'thenextweb': 'https://thenextweb.com/feed'
    }
    
    articles = []
    
    for source_name, feed_url in feeds.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                summary = entry.get('summary', entry.get('description', ''))
                summary = clean_html(summary)

                if not summary or summary.startswith('Comments'):
                    continue
                    
                article = {
                    'source': source_name,
                    'title': entry.title,
                    'url': entry.link,
                    'date': entry.get('published', '').split('T')[0],
                    'summary': get_first_sentences(summary)
                }
                articles.append(article)
                
        except Exception as e:
            print(f"Error fetching {source_name}: {str(e)}")
            continue
            
    return articles

async def function(args):
    try:
        limit = int(args.get("limit", 15))
        sources = args.get("sources", None)
        
        articles = get_startup_news()
        
        if sources:
            source_list = [s.strip().lower() for s in sources.split(",")]
            articles = [a for a in articles if a['source'].lower() in source_list]
            
        articles = articles[:limit]
        
        return json.dumps({
            "success": True,
            "message": articles
        })
        
    except Exception as e: 
        return json.dumps({
            "success": False,
            "error": str(e)
        })

object = {
    "name": "get_startup_news",
    "description": "Fetch latest startup and tech news from multiple sources",
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer", 
                "description": "Maximum number of articles to return (default: 15)"
            },
            "sources": {
                "type": "string",
                "description": "Comma-separated list of sources to include (e.g., 'techcrunch,ycombinator')"
            }
        }
    }
}