Creating a price-tracking application like `shop-saver` involves several components. Here, I’ll draft a simple version in Python that includes web scraping to track prices from e-commerce platforms, sending email alerts for price changes, and error handling.

For this demonstration, I'll mock a simple price tracker using a hypothetical e-commerce platform. Keep in mind that real implementation would require handling more complex logic, API calls, and complying with the Terms of Service of the e-commerce sites.

```python
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Product URLs and desired prices
tracked_items = {
    'https://example.com/product1': 150.00,
    'https://example.com/product2': 99.99,
}

# Email configuration
email_user = "youremail@gmail.com"
email_password = "yourpassword"
email_to = "toemail@gmail.com"

def send_email(subject, body):
    try:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = email_user
        message['To'] = email_to
        message['Subject'] = subject

        # Attach the message body
        message.attach(MIMEText(body, 'plain'))
        
        # Setup the server connection
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_user, email_password)

        # Send the email
        text = message.as_string()
        server.sendmail(email_user, email_to, text)
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_price(url):
    try:
        # Request the product page
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product price
        # This would need to be adapted to the actual HTML structure of the page
        price_tag = soup.find(class_='product-price')  # Example class
        price = float(price_tag.get_text().strip().replace('$', ''))

        return price
    except requests.RequestException as e:
        print(f"Network error while accessing {url}: {e}")
    except AttributeError:
        print(f"Failed to parse price for {url}")

def track_prices():
    for url, target_price in tracked_items.items():
        try:
            current_price = check_price(url)
            
            if current_price is not None and current_price < target_price:
                subject = "Price Drop Alert!"
                body = f"The price for the product at {url} has dropped to {current_price}!"
                send_email(subject, body)
            else:
                print(f"No price drop for products at {url} (Current: {current_price}, Target: {target_price})")
        except Exception as e:
            print(f"Error tracking price for {url}: {e}")

if __name__ == "__main__":
    while True:
        track_prices()
        # Wait for 60 minutes before checking again
        time.sleep(3600)
```

### Key Points:
1. **Web Scraping**: This script uses BeautifulSoup for HTML parsing to find product prices. The actual `class_='product-price'` will vary depending on the site structure.
2. **Error Handling**: Includes basic error handling for network issues and parsing errors using try-except blocks.
3. **Email Alerts**: The script sends an email when a price drop is detected. Make sure to allow "less secure apps" or use an app-specific password for Gmail.
4. **Looping**: The script runs infinitely, checking for price changes every hour. Adjust sleep time as desired.
5. **Caveats**: This is a simplified version meant for demonstration purposes. Production quality code should consider additional factors such as handling more errors, respecting website scraping policies, caching data, concurrent price checks, etc.

Modify these elements based on your needs and adhere to website scraping guidelines and legal considerations.