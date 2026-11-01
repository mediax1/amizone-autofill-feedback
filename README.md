# Amizone Feedback Autofill

A Selenium script that fills in faculty feedback forms on the Amizone portal (s.amizone.net) for Amity University students.

## Features

- Opens Chrome with `undetected-chromedriver`
- Waits for you to log in and solve the CAPTCHA yourself
- Dismisses popups and alerts after login
- Opens **My Faculty** from the sidebar automatically
- Scans every subject and faculty entry on the My Faculty page, expands each dropdown and submits feedback where a Feedback button is shown
- Skips entries that already have feedback submitted
- Closes popups intelligently: it waits only as long as needed, catches late popups, and never touches the feedback form itself
- Ignores Yes/No radios inside promotional popups so they are never answered by mistake
- Selects "Strongly Agree" / "Yes" options and reports any question groups it could not answer
- Adds a random positive comment and submits the form
- Falls back to a manual watcher that fills any Feedback button you open yourself

## Requirements

- Python 3.9 or newer
- Google Chrome
- Packages: `selenium`, `undetected-chromedriver`

## Setup and Run

`undetected-chromedriver` downloads a matching driver for your installed Chrome, so no manual driver setup is needed. Install Python 3.9+ and Google Chrome first.

### Windows (PowerShell)

```powershell
git clone https://github.com/mediax1/amizone-autofill-feedback.git
cd amizone-autofill-feedback
python -m venv venv
venv\Scripts\Activate.ps1
pip install selenium undetected-chromedriver
python main.py
```

If PowerShell blocks the activate script, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

In Command Prompt, use `venv\Scripts\activate.bat` instead.

### macOS (Terminal)

```bash
git clone https://github.com/mediax1/amizone-autofill-feedback.git
cd amizone-autofill-feedback
python3 -m venv venv
source venv/bin/activate
pip install selenium undetected-chromedriver
python main.py
```

Install Python with `brew install python` if `python3` is missing. Chrome must be in `/Applications`.

On later runs, skip the clone and install steps. Just `cd` into the folder, activate the venv, and run `python main.py`.

## Usage

1. Chrome opens the Amizone login page.
2. Log in and solve the CAPTCHA. The script waits up to 180 seconds.
3. Once the dashboard loads, popups are closed and **My Faculty** opens.
4. The script goes through every faculty entry, expands it, and fills and submits feedback where a Feedback button appears. Progress is logged as `[n/total] Subject | Faculty`.
5. When the scan finishes, the manual watcher starts. Click a faculty row yourself to fill any entry that was missed.
6. Press `Ctrl+C` to stop the watcher, then press Enter to close the browser.

## Troubleshooting

- **`python` not found on macOS:** use `python3` outside the venv. Inside the activated venv, `python` works.
- **Chrome version mismatch:** update Chrome to the latest version and run again.
- **Login not detected:** the script looks for `/Home` or `dashboard` in the URL. Make sure you reach the dashboard before the timeout.
- **My Faculty not clicked:** click it manually. The watcher still works. If it keeps failing, update `MY_FACULTY_XPATHS`.
- **"No faculty list found" or "No Feedback button" for every entry:** the page markup differs from what the script expects. Update `TIMELINE_ITEMS_XPATH` or `FEEDBACK_IN_ITEM_XPATH`.
- **A popup stays open:** update `VISIBLE_POPUPS_JS`, `DISMISS_TEXTS` or `POPUP_BUTTONS_XPATH` to match it.
- **Unanswered question groups warning:** those questions have labels the script does not recognise. Answer them manually before submitting.
- **Form not submitted:** check that every question is answered and that a Submit button is visible.

## Disclaimer

This project is for personal and educational use. It automates actions on your own account. Review your answers and follow your university's policies. You are responsible for how you use it.

## License

MIT. See [LICENSE](LICENSE).

## Author

Faizan ([@mediax1](https://github.com/mediax1))
