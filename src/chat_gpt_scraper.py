from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ChatGPTScraper:
    def __init__(self, driver):
        self.driver = driver

    def navigate_chatgpt(self):
        self.driver.get('https://chat.openai.com/auth/login')
        sleep(120)
        sleep(120)

    def ask_gpt(self, text):
        text_box = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/main/div[3]/form/div/div[2]/textarea')
        text_box.send_keys(text)


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    chatGPTScraper = ChatGPTScraper(driver=driver)
    chatGPTScraper.navigate_chatgpt()
    chatGPTScraper.ask_gpt("I am going to provide passages and you will give me summaries")