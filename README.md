# Amizone Feedback Autofill

A Selenium script that fills in faculty feedback forms on the Amizone portal (s.amizone.net) for Amity University students.

## Features

- Opens Chrome with `undetected-chromedriver`
- Waits for you to log in and solve the CAPTCHA yourself
- Dismisses popups and alerts after login
- Opens **My Faculty** from the sidebar automatically
- Watches for the Feedback button when you click a faculty row
- Selects "Strongly Agree" / "Yes" options and reports any question groups it could not answer
- Adds a random positive comment and submits the form

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
4. Click a faculty row. When the Feedback button appears, the script fills and submits the form.
5. Click the next faculty row and repeat.
6. Press `Ctrl+C` to stop the watcher, then press Enter to close the browser.

## Troubleshooting

- **`python` not found on macOS:** use `python3` outside the venv. Inside the activated venv, `python` works.
- **Chrome version mismatch:** update Chrome to the latest version and run again.
- **Login not detected:** the script looks for `/Home` or `dashboard` in the URL. Make sure you reach the dashboard before the timeout.
- **My Faculty not clicked:** click it manually. The watcher still works. If it keeps failing, update `MY_FACULTY_XPATHS`.
- **Unanswered question groups warning:** those questions have labels the script does not recognise. Answer them manually before submitting.
- **Form not submitted:** check that every question is answered and that a Submit button is visible.

## Disclaimer

This project is for personal and educational use. It automates actions on your own account. Review your answers and follow your university's policies. You are responsible for how you use it.

## License

MIT. See [LICENSE](LICENSE).

## Author

Faizan ([@mediax1](https://github.com/mediax1))
