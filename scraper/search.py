import requests
from bs4 import BeautifulSoup
import json
import yaml
from termcolor import colored
import os
import chardet
import string
import ast
from prompts.prompts import generate_searches_prompt, get_search_page_prompt, generate_searches_json, get_search_page_json
import time


"""
Input:
Search Engine Query: The primary input to the tool is a search engine query intended for Google Search. This query is generated based on a specified plan and user query.
Output:
Dictionary of Website Content: The output of the tool is a dictionary where:
The key is the URL of the website that is deemed most relevant based on the search results.
The value is the content scraped from that website, presented as plain text.
The source is useful for citation purposes in the final response to the user query.
The content is used to generate a comprehensive response to the user query.
"""


    

    
def format_results(organic_results):

    result_strings = []
    for result in organic_results:
        title = result.get('title', 'No Title')
        link = result.get('link', '#')
        snippet = result.get('snippet', 'No snippet available.')
        result_strings.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n---")
    
    return '\n'.join(result_strings)

def fetch_search_results(search_queries):

    search_url = "https://google.serper.dev/search"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': os.environ['SERPER_DEV_API_KEY']  # Ensure this environment variable is set with your API key
    }
    payload = json.dumps({"q": search_queries})
    
    # Attempt to make the HTTP POST request
    try:
        response = requests.post(search_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX, 5XX)
        results = response.json()
        
        # Check if 'organic' results are in the response
        if 'organic' in results:
            return format_results(results['organic'])
        else:
            return "No organic results found."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request exception occurred: {req_err}"
    except KeyError as key_err:
        return f"Key error in handling response: {key_err}"
    
def scrape_website_content(website_url, failed_sites=[]):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    print("Scraping URL: ", website_url)
    def is_garbled(text):
        # Count non-ASCII characters
        non_ascii_chars = sum(1 for char in text if char not in string.printable)
        try:
            # Calculate the proportion of non-ASCII characters
            return non_ascii_chars / len(text) > 0.2
        except ZeroDivisionError:
            # If the text is empty, it cannot be garbled
            return False

    
    try:
        # Making a GET request to the website
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        
        # Detecting encoding using chardet
        detected_encoding = chardet.detect(response.content)
        response.encoding = detected_encoding['encoding'] if detected_encoding['confidence'] > 0.5 else 'utf-8'
        
        # Handling possible issues with encoding detection
        try:
            content = response.text
        except UnicodeDecodeError:
            content = response.content.decode('utf-8', errors='replace')
        
        # Parsing the page content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(separator='\n')
        # Cleaning up the text: removing excess whitespace
        clean_text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
        split_text = clean_text.split()
        first_5k_words = split_text[500:5000]
        clean_text_5k = ' '.join(first_5k_words)

        if is_garbled(clean_text):
            print(f"Failed to retrieve content from {website_url} due to garbled text.")
            failed = {"source": website_url, "content": "Failed to retrieve content due to garbled text"}
            failed_sites.append(website_url)
            return failed, failed_sites, False
        

        return {"source": website_url, "content": clean_text_5k}, "N/A",  True

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving content from {website_url}: {e}")
        failed = {"source": website_url, "content": f"Failed to retrieve content due to an error: {e}"}
        failed_sites.append(website_url)
        return failed, failed_sites, False
    