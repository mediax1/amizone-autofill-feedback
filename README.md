# Dynexus Feedback Automation Tool

<div align="center">
  
  ![Dynexus Logo](https://i.postimg.cc/yxvFyJBx/icon-9.png)

**Automate Your Faculty Feedback Process**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289DA.svg)](https://discord.gg/dynexus)

</div>

## 📋 Overview

The Dynexus Feedback Automation Tool is a powerful Selenium-based Python script designed to automate the tedious process of submitting faculty feedback forms specifically for **Amity University** students. Built to work exclusively with the Amity University feedback portal (s.amizone.net), it navigates through the feedback system, intelligently identifies subjects requiring feedback, and automatically fills out forms with positive ratings and thoughtful comments.

### 🎬 Preview

[![Dynexus Feedback Automation Tool Demo](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/your-video-id)

_Click the badge above to watch the demo video_

## ✨ Features

- **Automatic Login** - Securely log in to your academic portal
- **Smart Navigation** - Intelligently find and access the faculty feedback section
- **Duplicate Detection** - Prevent processing the same subject multiple times
- **Popup Handling** - Automatically close annoying popups and alerts
- **Positive Feedback** - Select "Strongly Agree" options for all rating questions
- **Meaningful Comments** - Add thoughtful, randomly selected comments about teaching quality
- **Robust Error Handling** - Gracefully recover from unexpected situations
- **Progress Tracking** - Colorful console output showing real-time progress

## ⚠️ Important Note

This tool is specifically designed for **Amity University** students and works exclusively with the Amizone portal (s.amizone.net). It will not work with other university portals or feedback systems.

## 📥 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/mediax1/amizone-autofill-feedback.git
   cd dynexus-feedback-tool
   ```

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download webdriver**
   - Download Chrome WebDriver from [here](https://sites.google.com/chromium.org/driver/)
   - Ensure the WebDriver version matches your Chrome browser version
   - Add the WebDriver to your system PATH or place it in the script directory

## 🚀 Usage

Run the script:

```bash
python dynexus_feedback.py
```

Follow the prompts to enter your Amizone login credentials. The tool will then:

1. Log in to your Amity University portal (Amizone)
2. Navigate to the faculty feedback section
3. Process each subject one by one
4. Select positive ratings and add meaningful comments
5. Submit each form and track progress

Note: You must have an active Amity University account with valid credentials to use this tool.

## 💻 How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Login       │───▶│  Find Subjects  │───▶│ Process Subject │
└─────────────────┘    └─────────────────┘    └────────┬────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Submit Feedback │◀───│  Add Comments   │◀───│  Select Ratings │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

The script uses intelligent selection algorithms to find and interact with form elements, ensuring reliable operation even with slightly different form layouts.

## ⚙️ Configuration

No additional configuration is required. The script is designed to handle different feedback formats automatically.

## 📝 Requirements

- Python 3.7 or higher
- Chrome browser
- Libraries: selenium, rich, colorama

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

If you're familiar with other university feedback systems and would like to adapt this tool for your university, feel free to fork the repository and customize it accordingly.

## 🔐 Security

This tool requires your login credentials to access the feedback system. All credentials are handled securely:

- Passwords are not displayed when typed
- No credentials are stored or transmitted beyond the login process
- All automation happens locally on your machine

## 🌟 Join Our Community

Join our Discord server for support, updates, and more tools like this one:
[discord.gg/dynexus](https://discord.gg/dynexus)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**@mediax1 | Faizan**

---

<div align="center">
  <img src="https://i.postimg.cc/yxvFyJBx/icon-9.png" width="200">
  
  <p>Made with ❤️ by the Dynexus Community</p>
</div>
