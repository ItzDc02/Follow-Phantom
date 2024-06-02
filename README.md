
# Follow Phantom
Automate the process of following pages on LinkedIn with ease using Follow Phantom—a PyQt5 and Selenium-based desktop application.

<img src="https://github.com/ItzDc02/Follow-Phantom/blob/master/Images/app_icon.png" alt="Follow Phantom Logo" width="200"/>

## 🚀 Features
- **User-Friendly Interface:** Simple and clear GUI built with PyQt5.
- **Excel Integration:** Upload an Excel file with LinkedIn URLs to automate the following process.
- **Supports 2FA:** Compatible with LinkedIn accounts that have two-factor authentication enabled.
- **Progress Tracking:** Real-time progress bar to monitor the automation process.
- **Detailed Logging:** Logging system to track the step-by-step operations and issues.

## 📋 Prerequisites
Ensure you have the following installed:
- Python 3.6 or higher
- PyQt5
- Selenium
- pandas
- webdriver_manager

You can install the necessary packages using pip:
```bash
pip install PyQt5 selenium pandas webdriver_manager
```

## 🛠 Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/follow-phantom.git
cd follow-phantom
```

## 🖥️ Usage
To run the application, execute the following command in the terminal:
```bash
python follow_phantom.py
```
- Enter your LinkedIn credentials in the GUI.
- Toggle the checkbox if you have 2FA enabled on your LinkedIn account.
- Upload an Excel file containing the URLs of the LinkedIn pages you wish to follow.
- Click 'Start' to begin the automation process.

## 📈 Progress and Logging
- The progress bar in the GUI will show the current progress of the following process.
- Check the log files for detailed information about the operations performed and any errors encountered.

## 🖼️ Screenshots
- **Login Screen and Main Interface with Progress Bar**
<img src="https://github.com/ItzDc02/Follow-Phantom/blob/master/Images/Interface.png" alt="App Interface With 2FA demo" width="500"/>


## 🛡️ Security
Your credentials are only used for logging in and are not stored or transmitted elsewhere.

## 💡 Tips
- Ensure your Excel file is correctly formatted with URLs in the first column.
- Regularly update your browser driver using webdriver_manager to avoid compatibility issues.

## 📝 License
Distributed under the MIT License. See LICENSE for more information.
