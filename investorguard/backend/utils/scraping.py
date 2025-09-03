# Scraping utils
import requests
from bs4 import BeautifulSoup

def scrape_social_media(platform, query):
    # Mock for demo (real needs API keys)
    if platform == 'X':
        return {'posts': ['Mock post 1', 'Mock post 2']}
    elif platform == 'Reddit':
        return {'posts': ['Mock Reddit thread']}
    return {'posts': []}