import time
import random
import logging
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("feedback")

LOGIN_URL = "https://s.amizone.net"
LOGIN_TIMEOUT = 180

COMMENTS = [
    "An excellent teacher who makes complex concepts easy to understand.",
    "Always prepared and explains concepts clearly with great examples.",
    "Very knowledgeable and genuinely cares about student learning.",
    "Exceptional teaching with real-world examples. Always available to clear doubts.",
    "Well-organized course materials. Makes difficult topics approachable.",
]

FAST_SELECT_JS = r"""
const done = arguments[arguments.length - 1];
const delayMs = arguments[0] * 1000;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const norm = s => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
const inSmallDialog = r => {
  const d = r.closest(".modal, [role='dialog'], [role='alertdialog']");
  return d && d.querySelectorAll("input[type='radio']").length < 4;
};
const radios = Array.from(document.querySelectorAll("input[type='radio']")).filter(r => !inSmallDialog(r));

const labelText = r => {
  const l = r.closest('label') || (r.id && document.querySelector(`label[for="${r.id}"]`));
  if (l) return norm(l.textContent);
  return norm(r.parentElement ? r.parentElement.textContent : '');
};

(async () => {
  let clicked = 0;
  for (const r of radios) {
    const t = labelText(r);
    if ((t.includes('strongly agree') || /^yes\b/.test(t)) && !r.checked) {
      r.click();
      r.dispatchEvent(new Event('change', {bubbles: true}));
      clicked++;
      await sleep(delayMs);
    }
  }
  const groups = {};
  radios.forEach(r => { if (r.name) (groups[r.name] ||= []).push(r); });
  const unanswered = [];
  for (const [name, rs] of Object.entries(groups)) {
    if (!rs.some(r => r.checked)) unanswered.push(name);
  }
  done({clicked, unanswered});
})();
"""

VISIBLE_POPUPS_JS = r"""
const vis = e => {
  const r = e.getBoundingClientRect();
  const s = getComputedStyle(e);
  return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
};
const sel = ".modal, [role='dialog'], [role='alertdialog'], .swal2-popup, .bootbox, .ui-dialog";
return Array.from(document.querySelectorAll(sel))
  .filter(vis)
  .filter(e => !e.querySelector("textarea") && e.querySelectorAll("input[type='radio']").length < 4);
"""

DISMISS_TEXTS = ("ok", "got it", "dismiss", "close", "continue", "done", "no thanks")
POPUP_BUTTONS_XPATH = (
    ".//button | .//input[@type='button' or @type='submit'] "
    "| .//a[contains(@class,'btn')] | .//*[@data-dismiss] | .//*[contains(@class,'close')]"
)

SUBMIT_XPATHS = [
    "//input[@id='btnSubmit']",
    "//input[@type='submit' and @value='Submit']",
    "//button[@type='submit']",
    "//button[contains(text(),'Submit')]",
]

COMMENT_XPATHS = [
    "//textarea[@id='FeedbackRating_Comments']",
    "//textarea[@name='FeedbackRating_Comments']",
    "//textarea",
]


uc.Chrome.__del__ = lambda self: None


def make_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,SafetyCheck")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
        },
    )
    return uc.Chrome(options=options)


def _visible_popups(driver):
    try:
        return driver.execute_script(VISIBLE_POPUPS_JS) or []
    except Exception as e:
        log.debug("popup scan failed: %s", e)
        return []


def _pick_dismiss_button(popup):
    fallback = None
    for b in popup.find_elements(By.XPATH, POPUP_BUTTONS_XPATH):
        try:
            if not b.is_displayed():
                continue
            label = (b.text or b.get_attribute("value") or "").strip().lower()
            cls = (b.get_attribute("class") or "").lower()
        except StaleElementReferenceException:
            continue
        if label in DISMISS_TEXTS:
            return b
        if b.get_attribute("data-dismiss") or "close" in cls:
            fallback = fallback or b
    return fallback


def _is_gone(el):
    try:
        return not el.is_displayed()
    except StaleElementReferenceException:
        return True


def handle_popups(driver, timeout=5.0, quiet=0.0):
    deadline = time.time() + timeout
    quiet_since = None
    closed = 0
    while time.time() < deadline:
        try:
            driver.switch_to.alert.accept()
            closed += 1
            continue
        except Exception:
            pass

        popups = _visible_popups(driver)
        if not popups:
            if quiet <= 0:
                break
            quiet_since = quiet_since or time.time()
            if time.time() - quiet_since >= quiet:
                break
            time.sleep(0.1)
            continue

        quiet_since = None
        popup = popups[-1]
        btn = _pick_dismiss_button(popup)
        try:
            if btn is not None:
                click_element(driver, btn)
            else:
                popup.send_keys(Keys.ESCAPE)
            closed += 1
        except Exception as e:
            log.debug("popup dismiss failed: %s", e)
        try:
            WebDriverWait(driver, 2, poll_frequency=0.1).until(
                lambda d: _is_gone(popup)
            )
        except TimeoutException:
            log.debug("popup still visible after dismiss")
            time.sleep(0.2)
    if closed:
        log.info("Closed %d popup(s)", closed)
    return closed


def click_element(driver, el):
    try:
        el.click()
        return True
    except Exception as e:
        log.debug("native click failed: %s", e)
    try:
        driver.execute_script("arguments[0].click();", el)
        return True
    except Exception as e:
        log.warning("js click failed: %s", e)
        return False


def get_feedback_button(driver):
    els = driver.find_elements(
        By.XPATH,
        "//a[contains(@class,'btn') and contains(.,'Feedback') and not(contains(.,'Post Message'))]",
    )
    for el in els:
        try:
            if el.is_displayed():
                return el
        except StaleElementReferenceException:
            continue
    return None


SELECTION_DELAY = 0.5


def fill_options(driver):
    driver.set_script_timeout(120)
    result = driver.execute_async_script(FAST_SELECT_JS, SELECTION_DELAY)
    log.info("Selected %d options", result["clicked"])
    if result["unanswered"]:
        log.warning(
            "Unanswered question groups (no matching label, answer manually): %s",
            ", ".join(result["unanswered"]),
        )
    return not result["unanswered"]


def add_comment(driver):
    for sel in COMMENT_XPATHS:
        for ta in driver.find_elements(By.XPATH, sel):
            try:
                if ta.is_displayed():
                    ta.clear()
                    ta.send_keys(random.choice(COMMENTS))
                    return True
            except StaleElementReferenceException:
                continue
    log.warning("No comment box found")
    return False


def element_gone(el):
    try:
        return not el.is_displayed()
    except StaleElementReferenceException:
        return True


def submit_and_wait(driver):
    for sel in SUBMIT_XPATHS:
        for btn in driver.find_elements(By.XPATH, sel):
            try:
                visible = btn.is_displayed()
            except StaleElementReferenceException:
                continue
            if not visible:
                continue
            if not click_element(driver, btn):
                continue
            try:
                WebDriverWait(driver, 15).until(lambda d: element_gone(btn))
            except TimeoutException:
                log.warning("Submit button still visible after 15s")
                return False
            handle_popups(driver, quiet=0.8)
            return True
    log.warning("No submit button found")
    return False


def wait_for_login(driver):
    driver.get(LOGIN_URL)
    log.info("Log in and solve the CAPTCHA. Waiting up to %ds...", LOGIN_TIMEOUT)
    try:
        WebDriverWait(driver, LOGIN_TIMEOUT).until(
            lambda d: "/Home" in d.current_url or "dashboard" in d.current_url.lower()
        )
    except TimeoutException:
        raise RuntimeError("Login not detected within the timeout")
    log.info("Logged in.")
    handle_popups(driver, quiet=1.5)


MY_FACULTY_XPATHS = [
    "//a[normalize-space(.)='My Faculty']",
    "//a[contains(normalize-space(.),'My Faculty')]",
    "//*[self::span or self::li][normalize-space(.)='My Faculty']",
]


def open_my_faculty(driver):
    for sel in MY_FACULTY_XPATHS:
        try:
            el = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, sel))
            )
        except TimeoutException:
            continue
        if click_element(driver, el):
            log.info("Opened My Faculty.")
            return True
    log.warning("Could not find 'My Faculty' in the menu. Click it manually.")
    return False


def process_feedback(driver, btn):
    handle_popups(driver)
    if not click_element(driver, btn):
        log.warning("Could not click Feedback button")
        return False
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='radio']"))
        )
    except TimeoutException:
        log.warning("Feedback form did not load")
        return False
    handle_popups(driver, quiet=1.0)
    fill_options(driver)
    add_comment(driver)
    return submit_and_wait(driver)


TIMELINE_ITEMS_XPATH = "//ul[contains(@class,'timeline')]/li"
FEEDBACK_IN_ITEM_XPATH = (
    ".//a[contains(@class,'btn') and contains(.,'Feedback') "
    "and not(contains(.,'Post Message'))]"
)


def get_items(driver):
    return driver.find_elements(By.XPATH, TIMELINE_ITEMS_XPATH)


def item_feedback_button(item):
    for el in item.find_elements(By.XPATH, FEEDBACK_IN_ITEM_XPATH):
        try:
            if el.is_displayed():
                return el
        except StaleElementReferenceException:
            continue
    return None


def open_item(driver, item):
    try:
        panel = item.find_element(By.XPATH, ".//div[contains(@class,'text')]")
        if panel.is_displayed():
            return
        header = item.find_element(By.XPATH, ".//div[@class='subject']")
        click_element(driver, header)
        WebDriverWait(driver, 3).until(lambda d: panel.is_displayed())
    except Exception as e:
        log.debug("open_item: %s", e)


def scan_all_subjects(driver):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, TIMELINE_ITEMS_XPATH))
        )
    except TimeoutException:
        log.warning("No faculty list found. Falling back to manual mode.")
        return
    total = len(get_items(driver))
    log.info("Found %d faculty entries. Scanning...", total)

    done = 0
    for i in range(total):
        items = get_items(driver)
        if i >= len(items):
            log.info("Page changed; reopening My Faculty.")
            open_my_faculty(driver)
            time.sleep(2)
            items = get_items(driver)
            if i >= len(items):
                break
        item = items[i]
        try:
            subject = item.find_element(By.XPATH, ".//div[@class='subject']").text.strip()
            faculty = item.find_element(
                By.XPATH, ".//*[contains(@class,'faculty-name')]"
            ).get_attribute("textContent").strip()
        except Exception:
            subject, faculty = "?", "?"
        log.info("[%d/%d] %s | %s", i + 1, total, subject, faculty)

        open_item(driver, item)
        time.sleep(0.4)
        btn = item_feedback_button(item)
        if btn is None:
            log.info("  No Feedback button (already submitted).")
            continue

        if process_feedback(driver, btn):
            done += 1
            log.info("  Submitted.")
            time.sleep(1.5)
        else:
            log.error("  Submission failed.")
    log.info("Auto scan finished. Submitted %d of %d.", done, total)

def watch_and_fill(driver):
    log.info("Watching for Feedback button. Click a faculty row to begin. Ctrl+C to stop.")
    last_el = None

    while True:
        try:
            btn = get_feedback_button(driver)

            if btn is None:
                last_el = None
                time.sleep(0.3)
                continue

            if last_el is not None and btn == last_el:
                time.sleep(0.3)
                continue

            log.info("Feedback button detected. Filling...")
            if process_feedback(driver, btn):
                log.info("Submitted. Click next faculty row when ready.")
                last_el = btn
            else:
                log.error("Submission failed for this faculty")
                last_el = btn

            time.sleep(0.3)

        except KeyboardInterrupt:
            log.info("Stopped.")
            break
        except StaleElementReferenceException:
            last_el = None
            time.sleep(0.3)
        except Exception:
            log.exception("Unexpected error in watch loop")
            time.sleep(1)


def main():
    driver = make_driver()
    try:
        wait_for_login(driver)
        open_my_faculty(driver)
        scan_all_subjects(driver)
        watch_and_fill(driver)
    except RuntimeError as e:
        log.error("%s", e)
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()


if __name__ == "__main__":
    main()