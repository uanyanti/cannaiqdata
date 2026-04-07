import smtplib
import pandas as pd
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base, ".env"))

ZOHO_EMAIL = os.getenv("ZOHO_EMAIL")
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD")
SMTP_SERVER = "smtp.zohocloud.ca"
SMTP_PORT = 465

def send_email(to_email, store_name):
    subject = "Calgary cannabis market data — thought this might be useful"
    
    body = f"""Hi {store_name} team,

I built a market intelligence platform specifically for Calgary cannabis retailers.

It shows:
- Which neighbourhoods are oversaturated right now
- Where the lowest competition opportunities are
- New license applications being filed near you
- How your area compares to the rest of Calgary

Free preview at cannaiqdata.ca — no signup needed.

If you'd like full access including the interactive store map and postal code analysis, just reply to this email and I'll send you a beta access code.

— Ben
hello@cannaiqdata.ca
cannaiqdata.ca
"""
    
    msg = MIMEMultipart()
    msg['From'] = ZOHO_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(ZOHO_EMAIL, ZOHO_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending to {to_email}: {e}")
        return False

def run_campaign():
    print("Loading email list...")
    df = pd.read_csv("../data/calgary_emails_found.csv")
    
    # Remove duplicates
    df_unique = df.drop_duplicates(subset=['email'])
    print(f"Unique emails after dedup: {len(df_unique)}")
    
    # Skip first 45 already sent
    remaining = df_unique.iloc[45:]
    print(f"Remaining emails to send: {len(remaining)}")
    
    sent = 0
    failed = 0
    
    for idx, row in remaining.iterrows():
        store_name = row['Establishment Name']
        email = row['email']
        
        print(f"Sending to: {store_name} — {email}")
        success = send_email(email, store_name)
        
        if success:
            sent += 1
            print(f"✅ Sent")
        else:
            failed += 1
            print(f"❌ Failed")
        
        time.sleep(3)
    
    print(f"\n=== Campaign Results ===")
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    run_campaign()