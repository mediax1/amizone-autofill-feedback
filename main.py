import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random,os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

from rich.console import Console
from rich.text import Text


console = Console()

def print_header():
        
    header_text = [
r'''
██████╗ ██╗   ██╗███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
██╔══██╗╚██╗ ██╔╝████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██║  ██║ ╚████╔╝ ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║  ██║  ╚██╔╝  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██████╔╝   ██║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═════╝    ╚═╝   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
''']

    os.system('cls' if os.name == 'nt' else 'clear')
    
    color = "grey46"
    for line in header_text:
        console.print(Text(line, style=color), justify="center")
        time.sleep(0.1)
    
    console.print(Text("Feedback Automation Tool By @mediax1 | Faizan", style="italic bold cyan"), justify="center")
    console.print(Text("Join discord.gg/dynexus For More Stuff Like This", style="italic bold cyan"), justify="center")
    console.print("")

def main():
    import getpass
    
    username = input(f"{Fore.CYAN}Enter your username: {Fore.RESET}")
    password = getpass.getpass(f"{Fore.CYAN}Enter your password: {Fore.RESET}")
    

    os.system('cls' if os.name == 'nt' else 'clear')
    

    print_header()
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://s.amizone.net/")
    
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "_UserName"))
    )
    username_field.clear()
    username_field.send_keys(username)
    
    password_field = driver.find_element(By.NAME, "_Password")
    password_field.clear()
    password_field.send_keys(password)
    
    login_button = driver.find_element(By.CLASS_NAME, "login100-form-btn")
    login_button.click()
    
    WebDriverWait(driver, 20).until(
        EC.url_changes("https://s.amizone.net/")
    )
    
    print(f"{Fore.GREEN}[+] Logged in successfully")
    handle_popups(driver)
    
    navigate_to_faculty_page(driver)
    time.sleep(5)
    
    subjects = scan_subjects(driver)
    process_subjects(driver, subjects)
    
    while True:
        time.sleep(10)

def handle_popups(driver):
    popup_close_selectors = [
        "//button[contains(@class, 'close')]",
        "//button[contains(@class, 'btn-close')]",
        "//div[contains(@class, 'modal')]//button[contains(@class, 'close')]",
        "//div[contains(@class, 'popup')]//button",
        "//a[contains(@class, 'close')]",
        "//span[contains(@class, 'close')]",
        "//div[contains(@id, 'modal')]//button",
        "//div[contains(@class, 'ui-dialog')]//button",
        "//div[contains(@role, 'dialog')]//button",
        "//button[contains(text(), 'Close')]",
        "//button[contains(text(), 'OK')]",
        "//button[contains(text(), 'Continue')]",
        "//button[contains(text(), 'Got it')]",
        "//button[contains(text(), 'Dismiss')]",
        "//button[contains(text(), 'I understand')]"
    ]
    
    for _ in range(5):
        found_popup = False
        
        for selector in popup_close_selectors:
            try:
                close_buttons = driver.find_elements(By.XPATH, selector)
                
                if close_buttons:
                    for button in close_buttons:
                        if button.is_displayed():
                            button.click()
                            found_popup = True
                            time.sleep(1)
            except Exception:
                continue
        
        try:
            alert = driver.switch_to.alert
            alert.accept()
            found_popup = True
        except:
            pass
            
        if not found_popup:
            break
        
        time.sleep(1)

def navigate_to_faculty_page(driver):
    print(f"{Fore.CYAN}[*] Navigating to Faculty page")
    try:
        try:
            my_faculty_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='menu-text' and text()='My Faculty']"))
            )
            my_faculty_link.click()
            return True
        except:
            current_url = driver.current_url
            base_url = current_url.split('/')[0] + '//' + current_url.split('/')[2]
            faculty_url = base_url + "/FacultyFeeback"
            driver.get(faculty_url)
            return True
    except Exception:
        return try_alternative_faculty_links(driver)

def try_alternative_faculty_links(driver):
    faculty_selectors = [
        "//a[contains(@href, 'faculty')]",
        "//a[contains(text(), 'Faculty')]",
        "//a[contains(text(), 'My Faculty')]",
        "//li[contains(@class, 'menu')]//a[contains(@href, 'faculty')]",
        "//div[contains(@class, 'menu')]//a[contains(text(), 'Faculty')]",
        "//ul[contains(@class, 'nav')]//a[contains(@href, 'faculty')]",
        "//span[contains(text(), 'Faculty')]/..",
        "//i[contains(@class, 'fa-user')]/following-sibling::span[contains(text(), 'Faculty')]/.."
    ]
    
    for selector in faculty_selectors:
        try:
            element = driver.find_element(By.XPATH, selector)
            if element.is_displayed():
                element.click()
                return True
        except:
            continue
    
    return False

def scan_subjects(driver):
    subject_selectors = [
        "//table//tr[contains(@class, 'data-row')]",
        "//div[contains(@class, 'course')]",
        "//div[contains(@class, 'subject')]",
        "//li[contains(@class, 'subject')]",
        "//div[contains(@class, 'faculty-course')]",
        "//div[contains(@class, 'course-card')]",
        "//table//tbody//tr[position() > 1]"
    ]
    
    found_subjects = []
    
    for selector in subject_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                print(f"{Fore.CYAN}[*] Found {Fore.YELLOW}{len(elements)}{Fore.CYAN} subjects")
                for idx, element in enumerate(elements, 1):
                    subject_text = element.text.strip()
                    if subject_text:
                        found_subjects.append(element)
        except:
            continue
    
    return found_subjects

def process_subjects(driver, subjects):
    if not subjects:
        print(f"{Fore.RED}[-] No subjects found to process")
        return
    
    total_subjects = len(subjects)
    print(f"{Fore.GREEN}[+] Starting to process {Fore.YELLOW}{total_subjects}{Fore.GREEN} subjects")
    
    # Track processed subjects by their text to avoid duplicate processing
    processed_subjects = set()
    current_index = 0
    
    while current_index < total_subjects:
        try:
            print(f"\n{Fore.CYAN}[*] Processing subject {Fore.YELLOW}{current_index+1}/{total_subjects}")
            
            fresh_subjects = scan_subjects(driver)
            
            if current_index < len(fresh_subjects):
                subject = fresh_subjects[current_index]
                subject_text = subject.text.strip()
                
                # Check if we've already processed this subject
                if subject_text in processed_subjects:
                    print(f"{Fore.YELLOW}[!] Subject already processed: {Fore.YELLOW}{subject_text}")
                    current_index += 1
                    continue
                
                print(f"{Fore.CYAN}[*] Subject: {Fore.YELLOW}{subject_text}")
                
                if click_subject(driver, subject):
                    time.sleep(3)
                    
                    feedback_clicked = click_feedback_button(driver, subject_text)
                    
                    if not feedback_clicked:
                        print(f"{Fore.BLUE}[i] No feedback needed - moving to next subject")
                    else:
                        print(f"{Fore.GREEN}[+] Successfully processed feedback")
                        processed_subjects.add(subject_text)
                    
                    time.sleep(3)  
                    current_index += 1
                else:
                    navigate_to_faculty_page(driver)
                    time.sleep(3)
            else:
                navigate_to_faculty_page(driver)
                time.sleep(3)
        
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {str(e)}")
            navigate_to_faculty_page(driver)
            time.sleep(3)
            current_index += 1
    
    print(f"\n{Fore.GREEN}[+] Completed processing all subjects!")

def click_subject(driver, subject):
    try:
        subject.click()
        return True
    except:
        try:
            links = subject.find_elements(By.TAG_NAME, "a")
            if links:
                for link in links:
                    if link.is_displayed():
                        link.click()
                        return True
        except:
            pass
                
        try:
            buttons = subject.find_elements(By.TAG_NAME, "button")
            if buttons:
                for button in buttons:
                    if button.is_displayed():
                        button.click()
                        return True
        except:
            pass
                
        driver.execute_script("arguments[0].click();", subject)
        return True
            
    return False

def click_feedback_button(driver, subject_text):
    time.sleep(3)
    
    # Look for checkmark related to THIS subject specifically
    try:
        # First find the subject container - it might be a row or a specific div containing the subject
        subject_containers = driver.find_elements(By.XPATH, 
            f"//tr[contains(., '{subject_text}')] | //div[contains(., '{subject_text}')]")
        
        for container in subject_containers:
            try:
                # Check for checkmark image within this container
                checkmark = container.find_element(By.XPATH, ".//img[contains(@src, 'right.gif') or contains(@src, 'check')]")
                if checkmark.is_displayed():
                    print(f"{Fore.YELLOW}[!] Feedback already submitted for this subject (checkmark found)")
                    return False
            except NoSuchElementException:
                # No checkmark found in this container, which is good
                pass
    except:
        # If we can't find the container, continue with regular flow
        pass
    
    # Check for text indications that feedback is already given
    feedback_completed_texts = [
        "Feedback Submitted", 
        "Already Submitted",
        "Completed",
        "Thank you for your feedback"
    ]
    
    page_text = driver.page_source.lower()
    for text in feedback_completed_texts:
        if text.lower() in page_text:
            print(f"{Fore.YELLOW}[!] Feedback appears to be already submitted (found text: {text})")
            return False
    
    # Now check for the feedback button with more robust method
    try:
        feedback_button = driver.find_element(By.XPATH, 
            "//a[contains(@class, 'btn') and contains(., 'Feedback') and .//i[contains(@class, 'fa-comment')] and not(contains(., 'Post Message'))]")
        
        if feedback_button.is_displayed():
            feedback_button.click()
            time.sleep(3)
            return select_all_strongly_agree(driver)
        else:
            return False
    except NoSuchElementException:
        pass
    
    # Try all possible feedback-related buttons with improved identification
    button_selectors = [
        "//a[contains(@class, 'btn') and (contains(., 'Feedback') or contains(., 'Rate'))]",
        "//button[contains(., 'Feedback') or contains(., 'Rate')]",
        "//a[contains(@href, 'feedback') or contains(@href, 'rate')]",
        "//input[contains(@value, 'Feedback') or contains(@value, 'Rate')]"
    ]
    
    for selector in button_selectors:
        try:
            buttons = driver.find_elements(By.XPATH, selector)
            for button in buttons:
                if button.is_displayed():
                    button.click()
                    time.sleep(3)
                    return select_all_strongly_agree(driver)
        except:
            continue
        
    print(f"{Fore.YELLOW}[!] Could not find feedback button for subject: {subject_text}")
    return False

def select_all_strongly_agree(driver):
    processed_elements = set()
    total_selected = 0
    
    strongly_agree_selectors = [
        "//label[contains(.//span[contains(@class, 'lbl')], 'Strongly Agree')]/input[@type='radio']",
        "//label[contains(., 'Strongly Agree')]/input[@type='radio']",
        "//input[@type='radio']/following-sibling::span[contains(text(), 'Strongly Agree')]/..",
        "//input[@type='radio'][../span[contains(text(), 'Strongly Agree')]]",
        "//label[.//span[text()=' Strongly Agree']]/input",
        "//span[text()=' Strongly Agree']/preceding-sibling::input[@type='radio']"
    ]
    
    for selector in strongly_agree_selectors:
        radio_buttons = driver.find_elements(By.XPATH, selector)
        if radio_buttons:
            for radio in radio_buttons:
                element_id = radio.get_attribute("id") or radio.get_attribute("name")
                if not element_id:
                    element_id = driver.execute_script("""
                        function getXPath(element) {
                            if (element.id !== '') return 'id("' + element.id + '")';
                            if (element === document.body) return element.tagName;
                            
                            var ix = 0;
                            var siblings = element.parentNode.childNodes;
                            for (var i = 0; i < siblings.length; i++) {
                                var sibling = siblings[i];
                                if (sibling === element) return getXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                                if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
                            }
                        }
                        return getXPath(arguments[0]);
                    """, radio)
                
                if element_id in processed_elements:
                    continue
                
                processed_elements.add(element_id)
                
                try:
                    if not radio.is_selected():
                        try:
                            radio.click()
                            total_selected += 1
                        except:
                            driver.execute_script("arguments[0].click();", radio)
                            total_selected += 1
                except:
                    continue
    
    if total_selected == 0:
        all_radios = driver.find_elements(By.XPATH, "//input[@type='radio']")
        
        radio_groups = {}
        for radio in all_radios:
            try:
                name = radio.get_attribute("name")
                if name:
                    if name not in radio_groups:
                        radio_groups[name] = []
                    radio_groups[name].append(radio)
            except:
                continue
        
        for name, radios in radio_groups.items():
            if radios:
                try:
                    radios.sort(key=lambda x: int(x.get_attribute("value") or 0), reverse=True)
                    if not radios[0].is_selected():
                        element_id = radios[0].get_attribute("id") or name
                        
                        if element_id not in processed_elements:
                            processed_elements.add(element_id)
                            try:
                                radios[0].click()
                                total_selected += 1
                            except:
                                driver.execute_script("arguments[0].click();", radios[0])
                                total_selected += 1
                except:
                    continue
    
    select_all_yes_options(driver)
    add_teacher_comment(driver)
    return submit_feedback(driver)

def select_all_yes_options(driver):
    processed_elements = set()
    
    yes_selectors = [
        "//label[contains(.//span[contains(@class, 'lbl')], 'Yes')]/input[@type='radio']",
        "//label[contains(., 'Yes')]/input[@type='radio']",
        "//input[@type='radio']/following-sibling::span[contains(text(), 'Yes')]/..",
        "//input[@type='radio'][../span[contains(text(), 'Yes')]]",
        "//label[.//span[text()='Yes']]/input",
        "//span[text()='Yes']/preceding-sibling::input[@type='radio']",
        "//input[@id='rdbQuestion1' and @value='1']",
        "//input[@id='rdbQuestion2' and @value='1']",
        "//input[@id='rdbQuestion3' and @value='1']"
    ]
    
    for selector in yes_selectors:
        radio_buttons = driver.find_elements(By.XPATH, selector)
        if radio_buttons:
            for radio in radio_buttons:
                element_id = radio.get_attribute("id") or radio.get_attribute("name")
                if not element_id:
                    element_id = driver.execute_script("""
                        function getXPath(element) {
                            if (element.id !== '') return 'id("' + element.id + '")';
                            if (element === document.body) return element.tagName;
                            
                            var ix = 0;
                            var siblings = element.parentNode.childNodes;
                            for (var i = 0; i < siblings.length; i++) {
                                var sibling = siblings[i];
                                if (sibling === element) return getXPath(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                                if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
                            }
                        }
                        return getXPath(arguments[0]);
                    """, radio)
                
                if element_id in processed_elements:
                    continue
                
                processed_elements.add(element_id)
                
                try:
                    if not radio.is_selected():
                        try:
                            radio.click()
                        except:
                            driver.execute_script("arguments[0].click();", radio)
                except:
                    continue
    
    specific_selectors = [
        "//input[@name='FeedbackRating_Q1Rating' and @value='1']",
        "//input[@name='FeedbackRating_Q2Rating' and @value='1']",
        "//input[@name='FeedbackRating_Q3Rating' and @value='1']"
    ]
    
    for selector in specific_selectors:
        try:
            yes_buttons = driver.find_elements(By.XPATH, selector)
            for button in yes_buttons:
                element_id = button.get_attribute("id") or button.get_attribute("name")
                
                if element_id not in processed_elements:
                    processed_elements.add(element_id)
                    
                    if not button.is_selected():
                        try:
                            button.click()
                        except:
                            driver.execute_script("arguments[0].click();", button)
        except:
            continue
    
    return True

def add_teacher_comment(driver):
    comments = [
        "An excellent teacher who makes complex concepts easy to understand. The lectures are engaging and well-structured.",
        "One of the best faculty members I've had. Always prepared for class and explains concepts clearly.",
        "The teacher is knowledgeable, approachable, and genuinely cares about student learning. Classes are interactive and enjoyable.",
        "Exceptional teaching skills with real-world examples that help connect theory to practice. Always available for doubts and questions.",
        "The faculty is very professional and delivers lectures with clarity. Course materials are well-organized and helpful."
    ]
    
    comment = random.choice(comments)
    
    textarea_selectors = [
        "//textarea[@id='FeedbackRating_Comments']",
        "//textarea[contains(@class, 'f-Comments')]",
        "//textarea[@name='FeedbackRating_Comments']",
        "//textarea[@placeholder='Comments can not be greater than 1000 characters']",
        "//textarea"
    ]
    
    for selector in textarea_selectors:
        try:
            textareas = driver.find_elements(By.XPATH, selector)
            if textareas:
                for textarea in textareas:
                    if textarea.is_displayed():
                        textarea.clear()
                        textarea.send_keys(comment)
                        return True
        except:
            continue
    
    return False

def submit_feedback(driver):
    submit_selectors = [
        "//input[@id='btnSubmit']",
        "//input[@type='submit' and @value='Submit']",
        "//input[@type='submit']",
        "//button[@type='submit']",
        "//button[contains(text(), 'Submit')]",
        "//input[contains(@class, 'btn-primary') and @type='submit']"
    ]
    
    for selector in submit_selectors:
        try:
            submit_buttons = driver.find_elements(By.XPATH, selector)
            if submit_buttons:
                for button in submit_buttons:
                    if button.is_displayed():
                        try:
                            button.click()
                            return True
                        except:
                            driver.execute_script("arguments[0].click();", button)
                            return True
        except:
            continue
    
    return False

if __name__ == "__main__":
    main()