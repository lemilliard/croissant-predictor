import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

hopla_url = "https://hopla2.fr.capgemini.com"
hopla_calendar_url = "https://hopla2.fr.capgemini.com/Calendar"


class Fetcher:
    def __init__(self):
        self.cookies = []
        self.projects = []
        self.load_cookies_and_projects()
        self.calendar = {}

    def load_cookies_and_projects(self):
        options = webdriver.ChromeOptions()
        options.add_argument("mute-audio")
        options.add_argument("disable-gpu")
        options.add_argument("log-level=3")
        options.add_argument("hide-scrollbars")
        options.add_argument("headless")

        driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
        driver.get(hopla_url)
        self.cookies = driver.get_cookies()

        select_projects = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "main_project"))
        )
        options_projects = WebDriverWait(select_projects, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "option"))
        )
        self.projects = [
            {"id": option.get_attribute("value"), "name": option.get_attribute("text")}
            for option in options_projects
        ]
        driver.close()

    def load_calendar(self, project_id, start_date, nb_months):
        headers = self.get_headers()
        data = {
            "startDate": start_date,
            "collection": "events",
            "projectId": project_id,
            # "projectId": "5c735e75d5de9fb38da25c1a",
            "nbMonths": nb_months,
            "action": "get"
        }
        req = requests.post(hopla_calendar_url, headers=headers, data=data, verify=False)
        if req.status_code != 200:
            raise Exception("Erreur dans la récupération des données")
        return req.json()

    def get_headers(self):
        return {
            "Content-type": "application/x-www-form-urlencoded",
            "Cookie": "; ".join([cookie["name"] + "=" + cookie["value"] for cookie in self.cookies])
        }
