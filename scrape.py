import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from bs4 import BeautifulSoup
import os

def scrape_website(website, timeout=20):
    print("Launching chrome browser...")

    # Better Chrome options for speed and reliability
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--blink-settings=imagesEnabled=false")  
    
    
    chrome_driver_path = "./chromedriver.exe" if os.name == 'nt' else "./chromedriver"
    
    try:
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        driver.set_page_load_timeout(timeout)
        
        try:
            driver.get(website)
            print("Page loaded...")
            
            # Wait for body content to be available
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                print("Warning: Timed out waiting for body element, continuing anyway...")
            
            html = driver.page_source
            return html
            
        except TimeoutException:
            print(f"Error: Timed out loading page after {timeout} seconds")
            return None
        except WebDriverException as e:
            print(f"Error loading page: {str(e)}")
            return None
    except Exception as e:
        print(f"Error initializing Chrome: {str(e)}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

def extract_body_content(html_content):
    if not html_content:
        return ""
    
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        if body_content:
            return str(body_content)
        return ""
    except Exception as e:
        print(f"Error extracting body content: {str(e)}")
        return ""

def clean_body_content(body_content):
    if not body_content:
        return ""
    
    try:
        soup = BeautifulSoup(body_content, "html.parser")
        
        # Remove script, style, svg, and canvas elements
        for tag in soup(['script', 'style', 'svg', 'canvas', 'noscript', 'iframe']):
            tag.extract()
        
        # Get text with proper line breaks for structure
        cleaned_content = soup.get_text(separator="\n")
        
     
        lines = [line.strip() for line in cleaned_content.splitlines()]
        cleaned_content = "\n".join(line for line in lines if line)
        
        return cleaned_content
    except Exception as e:
        print(f"Error cleaning body content: {str(e)}")
        return body_content  # Return original if cleaning fails

def split_dom_content(dom_content, max_length=6000):
    if not dom_content:
        return []
    
    # Improved splitting that tries to split at paragraph boundaries
    paragraphs = dom_content.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # If adding this paragraph exceeds max length and we already have content,
        # store the current chunk and start a new one
        if len(current_chunk) + len(para) > max_length and current_chunk:
            chunks.append(current_chunk)
            current_chunk = para
        # If the paragraph itself exceeds max length, split it
        elif len(para) > max_length:
            # Add any existing content to chunks
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
                
            # Split the long paragraph
            for i in range(0, len(para), max_length):
                chunks.append(para[i:i+max_length])
        # Otherwise add to current chunk
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks