import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import json
import os
import sys

public_description = "Connect with professionals on LinkedIn based on title and location."

def click(driver, selector, use_js=False):
    try:
        elements = driver.wait.until(EC.presence_of_all_elements_located((By.XPATH, selector)))
        if elements:
            if use_js:
                driver.execute_script("arguments[0].click();", elements[0])
            else:
                elements[0].click()
        sleep(1)
    except Exception as e:
        print(f'Error clicking element {selector}: {e}')
        return None

def load_connected_profiles():
    file_path = "connected_profiles.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading connected profiles: {e}")
            return []
    return []

def save_connected_profiles(profiles):
    file_path = "connected_profiles.json"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving connected profiles: {e}")
        try:
            sanitized_profiles = []
            for profile in profiles:
                sanitized_profile = {}
                for key, value in profile.items():
                    if isinstance(value, str):
                        sanitized_profile[key] = ''.join(c for c in value if ord(c) < 128)
                    else:
                        sanitized_profile[key] = value
                sanitized_profiles.append(sanitized_profile)
                
            with open(file_path + ".backup", "w") as f:
                json.dump(sanitized_profiles, f, indent=2)
            print("Created backup file with sanitized characters")
        except Exception as backup_error:
            print(f"Failed to create backup file: {backup_error}")

def is_already_connected(driver):
    connect_button = driver.find_elements(By.XPATH, "//button[contains(@aria-label, ' to connect')] | //div[contains(@aria-label, ' to connect')]")
    pending_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Pending')]")
    connected_indicator = driver.find_elements(By.XPATH, "//span[text()='Connected']")
    
    return (len(connect_button) == 0 and len(pending_button) == 0 and len(connected_indicator) > 0) or len(pending_button) > 0

def sanitize_text(text):
    if not text:
        return "N/A"
    try:
        return ''.join(c for c in text if c.isprintable())
    except Exception:
        return "Text contains unsupported characters"

def connect_with_people(title, location, max_connections=20, custom_prompt=""):
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    driver = uc.Chrome()
    connections_made = 0
    connection_details = []
    profiles_processed = 0
    
    connected_profiles = load_connected_profiles()
    connected_urls = [profile["profile_url"] for profile in connected_profiles]
    
    driver.wait = WebDriverWait(driver, 10)
    driver.get("https://www.linkedin.com/login")
    
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return {
            "success": False,
            "error": f"Login timeout or error: {e}"
        }

    driver.get('https://www.linkedin.com/search/results/people/')

    try:
        click(driver, "//button[contains(@aria-label, 'Show all filters')]")
        click(driver, "//button[contains(@aria-label, '2nd')]")
        click(driver, "//button[contains(@aria-label, '3rd')]")
        click(driver, f"//span[text()='Add a location']")
        
        location_input = driver.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add a location']"))
        )
        location_input.send_keys(location)

        max_retries = 3
        for retry in range(max_retries):
            try:
                location_option = driver.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'basic-typeahead__selectable')]"))
                )
                location_option.click()
                break
            except Exception as e:
                print(f"Retry {retry+1}/{max_retries} selecting location: {e}")
                if retry == max_retries - 1:
                    print("Failed to select location after retries")
                sleep(1)

        title_input = driver.wait.until(
            EC.presence_of_element_located((By.XPATH, "//label[text()='Title']/input[@class='mt1']"))
        )
        title_input.send_keys(title)

        click(driver, "//button[contains(@aria-label, 'Apply current filters')]")

        base_url = driver.current_url
        page_num = 1
        max_pages = 20
        
        while connections_made < max_connections and page_num <= max_pages:
            print(f"Scraping page {page_num}")
            
            max_profile_retries = 3
            profiles = None
            for retry in range(max_profile_retries):
                try:
                    profiles = driver.wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.linked-area"))
                    )
                    break
                except Exception as e:
                    print(f"Retry {retry+1}/{max_profile_retries} loading profiles: {e}")
                    if retry == max_profile_retries - 1:
                        print("Failed to load profiles after retries")
                    sleep(2)
                    driver.refresh()
            
            if not profiles:
                print(f"No profiles found on page {page_num}, moving to next page")
                page_num += 1
                try:
                    driver.get(base_url + f"&page={page_num}")
                except Exception as e:
                    print(f"Error navigating to next page: {e}")
                    break
                continue

            profile_links = []
            for profile in profiles:
                try:
                    profile_link = profile.find_element(By.CSS_SELECTOR, "a[href*='linkedin.com/in/']")
                    href = profile_link.get_attribute('href')
                    if href:
                        profile_links.append(href)
                except Exception as e:
                    print(f"Error getting profile link: {e}")
                    continue

            for href in profile_links:
                if connections_made >= max_connections:
                    break
                
                profiles_processed += 1
                
                if href in connected_urls:
                    print(f"Skipping already connected profile: {href}")
                    continue
                    
                try:
                    driver.get(href)
                    
                    if is_already_connected(driver):
                        print(f"Profile is already connected or pending: {href}")
                        if href not in connected_urls:
                            try:
                                soup = BeautifulSoup(driver.page_source, 'html.parser')
                                name = soup.find('h1')
                                headline = soup.find('div', {'class': 'text-body-medium'})
                                person_name = sanitize_text(name.text if name else "Unknown")
                                person_headline = sanitize_text(headline.text if headline else 'N/A')
                                
                                connected_profiles.append({
                                    "name": person_name,
                                    "headline": person_headline,
                                    "profile_url": href
                                })
                                connected_urls.append(href)
                                save_connected_profiles(connected_profiles)
                            except Exception as e:
                                print(f"Error processing already connected profile: {e}")
                        continue
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    name = soup.find('h1')
                    headline = soup.find('div', {'class': 'text-body-medium'})

                    bio = soup.find('div', {'class': 'display-flex ph5 pv3'})
                    if bio:
                        bio = bio.find('span', {'aria-hidden': 'true'})
                    
                    person_name = sanitize_text(name.text if name else "Unknown")
                    person_headline = sanitize_text(headline.text if headline else 'N/A')
                    person_bio = sanitize_text(bio.text if bio and bio.text != 'See all insights and introduction paths with Sales Navigator.' else 'N/A')
                    
                    print(f"Name: {person_name}")
                    print(f"Headline: {person_headline}")
                    
                    try:
                        click(driver, "//button[contains(@aria-label, ' to connect')] | //div[contains(@aria-label, ' to connect')]", use_js=True)

                        add_note_button = driver.find_elements(By.XPATH, "//button[@aria-label='Add a note']")
                        connection_sent = False

                        if not add_note_button:
                            click(driver, "//button[@aria-label='Send without a note']")
                            connection_sent = True
                        else:
                            click(driver, "//button[@aria-label='Add a note']")
                            no_invites = driver.find_elements(By.ID, "modal-upsell-header")

                            if no_invites:
                                click(driver, "//button[@aria-label='Dismiss']")
                                click(driver, "//button[contains(@aria-label, ' to connect')] | //div[contains(@aria-label, ' to connect')]", use_js=True)
                                click(driver, "//button[@aria-label='Send without a note']")
                                connection_sent = True
                            else:
                                prompt = f"""
                                    Generate a very brief, friendly LinkedIn connection note for:
                                    Name: {person_name}
                                    Role: {person_headline}
                                    Bio: {person_bio}
                                    Make it personal all in one sentence.
                                    This will be sent directly to the person, so don't include anything other than the note itself.
                                    For example, don't put [Your name] or anything that expects manual input.
                                    Don't write this in an email format, just a simple message.
                                    Do not wrap the message in quotation marks.
                                """

                                if custom_prompt:
                                    prompt += f"\n\nUser instructions (override the above instructions if necessary):\n{custom_prompt}"
                                custom_message = call_ai(prompt)["content"]
                                note_area = driver.find_element(By.ID, "custom-message")
                                note_area.send_keys(custom_message)
                                click(driver, "//button[@aria-label='Send invitation']")
                                connection_sent = True
                        
                        if connection_sent:
                            connections_made += 1
                            connection_details.append({
                                "name": person_name,
                                "headline": person_headline,
                                "profile_url": href
                            })
                            connected_profiles.append({
                                "name": person_name,
                                "headline": person_headline,
                                "profile_url": href
                            })
                            connected_urls.append(href)
                            print(f"Connection request sent! Total connections: {connections_made}")
                            save_connected_profiles(connected_profiles)
                    except Exception as e:
                        print(f"Error sending connection request: {e}")
                        
                except Exception as e:
                    print(f"Error processing profile {href}: {e}")
                
                sleep(2)

            if connections_made < max_connections:
                page_num += 1
                try:
                    driver.get(base_url + f"&page={page_num}")
                except Exception as e:
                    print(f"Error navigating to next page: {e}")
                    break

    except Exception as e:
        print(f"Error during connection process: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass
        
    return {
        "success": True,
        "message": f"Successfully connected with {connections_made} new profiles (processed {profiles_processed} total profiles)",
        "connections": connection_details
    }

async def function(args):
    try:
        if not args.get("title"):
            return json.dumps({
                "success": False,
                "error": "Job title is required"
            })
            
        if not args.get("location"):
            return json.dumps({
                "success": False,
                "error": "Location is required"
            })
        
        max_connections = int(args.get("max_connections", 20))
        custom_prompt = args.get("custom_prompt", "")
        
        result = connect_with_people(
            args["title"],
            args["location"],
            max_connections=max_connections,
            custom_prompt=custom_prompt
        )
        
        return json.dumps(result, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

object = {
    "name": "linkedin_connecter",
    "description": "Connect with professionals on LinkedIn based on title and location.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Job title to search for (e.g., 'Software Engineer', 'Data Scientist')"
            },
            "location": {
                "type": "string",
                "description": "Location to search in (e.g., 'Greater Toronto Area, Canada', 'San Francisco Bay Area')"
            },
            "max_connections": {
                "type": "integer",
                "description": "Maximum number of connection requests to send (default: 20)",
                "default": 20
            },
            "custom_prompt": {
                "type": "string",
                "description": "Custom instructions for generating connection messages",
                "default": ""
            }
        },
        "required": ["title", "location"]
    }
}
