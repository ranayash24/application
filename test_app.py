import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Selenium WebDriver
@pytest.fixture(scope="session")
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("http://localhost:8501/")  # Adjust this URL if your Streamlit app runs on a different port
    return driver

# Test the title of the Streamlit application
def test_title():
    assert "Chatbot" in driver.title  

# Test the API key input functionality
def test_api_key_input(driver):
    api_input = driver.find_element(By.NAME, "api")  
    api_input.clear()
    api_input.send_keys("test_api_key")
    assert "test_api_key" == api_input.get_attribute('value')

# Test the chat input and response
def test_chat_interaction(driver):
    user_input = driver.find_element(By.CSS_SELECTOR, "text_input[placeholder='Your AI assistant is here for your help']")  # Use the correct CSS selector for the input
    user_input.send_keys("Hello")
    user_input.send_keys(Keys.ENTER)
    time.sleep(1)  # Add delay to wait for the response
# Test the chat input and response
def test_chat_interaction(driver):
    # Find the text input field. We assume it's the first or only one on the page.
    user_input = driver.find_element(By.CSS_SELECTOR, "input.stTextInput")  # Streamlit text inputs often have this class
    user_input.send_keys("Hello")
    user_input.send_keys(Keys.ENTER)
    time.sleep(1)  # Add delay to wait for the response

    # Streamlit conversations are usually displayed in text blocks, let's try to find these
    # If your conversation output is immediately visible after sending the message, it might be in a block like this
    response_area = driver.find_elements(By.CSS_SELECTOR, ".stAlert")  # Assuming responses are in alert blocks
    assert any("Hello" in el.text for el in response_area)  # Check if 'Hello' is part of the conversation displayed


