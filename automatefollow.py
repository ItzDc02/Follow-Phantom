import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QFileDialog, QMessageBox, QLineEdit, QFormLayout, QProgressBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from webdriver_manager.chrome import ChromeDriverManager

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FollowPhantom(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.file_path = None
        self.two_fa_enabled = False

    def initUI(self):
        self.setWindowTitle('Follow Phantom')
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF; font-size: 14px;")

        layout = QVBoxLayout()

        self.info_label = QLabel('Welcome to Follow Phantom')
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter LinkedIn Username')
        self.username_input.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        form_layout.addRow('Username:', self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter LinkedIn Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        form_layout.addRow('Password:', self.password_input)

        layout.addLayout(form_layout)

        self.two_fa_checkbox = QCheckBox('Do you have 2FA on your LinkedIn?')
        self.two_fa_checkbox.setStyleSheet("color: #FFFFFF;")
        self.two_fa_checkbox.stateChanged.connect(self.toggle_two_fa)
        layout.addWidget(self.two_fa_checkbox)

        self.upload_button = QPushButton('Upload Excel File')
        self.upload_button.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        self.start_button = QPushButton('Start')
        self.start_button.setStyleSheet("background-color: #555555; color: #FFFFFF;")
        self.start_button.clicked.connect(self.start_process)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def toggle_two_fa(self, state):
        self.two_fa_enabled = (state == Qt.Checked)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            self.file_path = file_name
            self.info_label.setText(f"File Uploaded: {os.path.basename(file_name)}")

    def start_process(self):
        if not self.file_path:
            QMessageBox.warning(self, 'No File', 'Please upload an Excel file first.', QMessageBox.Ok)
            return

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Missing Credentials', 'Please enter both username and password.', QMessageBox.Ok)
            return

        self.info_label.setText('Starting process...')
        self.progress_bar.setValue(0)
        QApplication.processEvents()
        self.run_bot(self.file_path, username, password, self.two_fa_enabled)

    def run_bot(self, file_path, username, password, two_fa_enabled):
        EXCEL_PATH = file_path
        COLUMN_NAME = 'Career Page URL'
        df = pd.read_excel(EXCEL_PATH, header=None)
        df.columns = [COLUMN_NAME]
        df = self.check_for_duplicates(df)

        try:
            # Replacing the service setup with webdriver-manager
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        except Exception as e:
            logging.error(f"Error initializing WebDriver: {e}")
            QMessageBox.critical(self, 'Error', 'Failed to initialize WebDriver.', QMessageBox.Ok)
            return

        if not self.linkedin_login(driver, username, password, two_fa_enabled):
            driver.quit()
            return

        total_rows = len(df.index)
        for index, row in df.iterrows():
            self.progress_bar.setValue(int((index + 1) / total_rows * 100))
            QApplication.processEvents()
            if not self.process_page(driver, row[COLUMN_NAME]):
                continue

        driver.quit()
        self.info_label.setText('Process completed successfully!')
        self.progress_bar.setValue(100)

    def check_for_duplicates(self, df):
        if df.duplicated(subset=['Career Page URL']).any():
            logging.info("Duplicate entries found. Removing duplicates...")
            df = df.drop_duplicates(subset=['Career Page URL'])
        return df

    def linkedin_login(self, driver, username, password, two_fa_enabled):
        try:
            driver.get('https://www.linkedin.com/login')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
            driver.find_element(By.ID, 'username').send_keys(username)
            driver.find_element(By.ID, 'password').send_keys(password)
            driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
            
            if two_fa_enabled:
                QMessageBox.information(self, '2FA Required', 'Please complete the 2FA on your device and click OK once done.', QMessageBox.Ok)
                WebDriverWait(driver, 60).until(EC.url_contains('feed'))  # Adjust time as needed
            else:
                WebDriverWait(driver, 10).until(EC.url_contains('feed'))
            
            return True
        except Exception as e:
            logging.error(f"Login failed: {e}")
            QMessageBox.critical(self, 'Login Failed', 'Could not log in to LinkedIn.', QMessageBox.Ok)
            return False

    def process_page(self, driver, career_page_url):
        try:
            driver.get(career_page_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            follow_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@aria-label, "Follow")]'))
            )
            if "Following" not in follow_button.text:
                follow_button.click()
                time.sleep(2)
                logging.info(f"Followed the page: {career_page_url}")
            else:
                logging.info(f"Already following the page: {career_page_url}")
            return True
        except Exception as e:
            logging.error(f"Could not follow the page: {career_page_url}. Error: {e}")
            return False

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('app_icon.png'))
    window = FollowPhantom()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
