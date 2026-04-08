import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def search_cannabis_consultants():
    print("Finding Alberta cannabis consultants and advisors...")
    
    sources = [
        {
            "name": "Cannabis Council of Canada Members",
            "url": "https://www.cannabiscouncil.ca/members/"
        },
        {
            "name": "Alberta Cannabis Industry",
            "url": "https://albertacannabis.org"
        }
    ]
    
    contacts = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    for source in sources:
        print(f"\nSearching: {source['name']}")
        try:
            response = requests.get(source['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract any email addresses
            import re
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            
            # Extract any company/person names
            text = soup.get_text()
            print(f"Page loaded — {len(emails)} emails found")
            
            for email in emails:
                if not any(skip in email.lower() for skip in ['noreply', 'example', 'test', 'wordpress']):
                    contacts.append({
                        'source': source['name'],
                        'email': email,
                        'type': 'Cannabis Industry'
                    })
                    
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)
    
    if contacts:
        df = pd.DataFrame(contacts).drop_duplicates(subset=['email'])
        df.to_csv("../data/cannabis_industry_contacts.csv", index=False)
        print(f"\nTotal industry contacts found: {len(df)}")
        print(df.head(10))
    else:
        print("No contacts found from web — focus on LinkedIn manual search")

if __name__ == "__main__":
    search_cannabis_consultants()