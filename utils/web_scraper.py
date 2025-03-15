import requests
from bs4 import BeautifulSoup
import re

def scrape_job_description(url):
    """
    Scrape job description from a given URL.
    
    Args:
        url (str): URL of the job posting
        
    Returns:
        str: Extracted job description
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Try to find job description section
        job_desc_patterns = [
            r'(?i)job description',
            r'(?i)about the job',
            r'(?i)about this role',
            r'(?i)responsibilities',
            r'(?i)what you\'ll do',
            r'(?i)requirements'
        ]
        
        for pattern in job_desc_patterns:
            match = re.search(pattern, text)
            if match:
                start_idx = match.start()
                # Get text from the match to the end, but limit to 5000 chars
                job_text = text[start_idx:start_idx + 5000]
                return job_text
        
        # If no specific section found, return a reasonable chunk of the page
        return text[:5000]
        
    except Exception as e:
        raise Exception(f"Error scraping job description: {str(e)}")
