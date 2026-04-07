import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def extract_emails_from_website(url):
    """Extract email addresses from a website"""
    if not url or pd.isna(url):
        return None
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=8)
        
        # Search for emails in page content
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, response.text)
        
        # Filter out common non-contact emails
        skip = ['noreply', 'no-reply', 'donotreply', 'wordpress', 
                'wix', 'example', 'domain', 'email', 'test']
        
        valid_emails = [
            e for e in emails 
            if not any(s in e.lower() for s in skip)
            and len(e) < 60
        ]
        
        if valid_emails:
            return valid_emails[0]
            
    except Exception as e:
        pass
    
    return None

def build_email_list():
    print("Extracting emails from store websites...")
    
    contacts = pd.read_csv("../data/calgary_contact_list.csv")
    print(f"Processing {len(contacts)} stores with websites...")
    
    emails = []
    
    for idx, row in contacts.iterrows():
        store_name = row['Establishment Name']
        website = row['website']
        
        print(f"Scraping: {store_name} — {website}")
        email = extract_emails_from_website(website)
        emails.append(email)
        
        time.sleep(0.5)
    
    contacts['email'] = emails
    
    # Save full list
    contacts.to_csv("../data/calgary_email_list.csv", index=False)
    
    # Save only stores with emails
    with_emails = contacts[contacts['email'].notna()]
    with_emails.to_csv("../data/calgary_emails_found.csv", index=False)
    
    print(f"\nTotal stores processed: {len(contacts)}")
    print(f"Emails found: {len(with_emails)}")
    print("\nSample emails:")
    print(with_emails[['Establishment Name', 'email']].head(15).to_string(index=False))

if __name__ == "__main__":
    build_email_list()