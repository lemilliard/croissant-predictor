import json
import datetime
import requests

from selenium import webdriver

hopla_url = "https://hopla2.fr.capgemini.com"
hopla_calendar_url = "https://hopla2.fr.capgemini.com/Calendar"

calendar_file = "calendar.json"


class Person:
    def __init__(self, name):
        self.name = name
        self.holiday = []
        self.potential = 0

    def add_holiday(self, holiday):
        self.holiday.append(holiday)

    def is_in_holiday(self, date):
        return date in self.holiday


class Solver:
    def __init__(self):
        self.cookies = []
        # self.fetch_cookies()

        self.calendar = {}
        # self.fetch_calendar()
        self.load_calendar()

        self.persons = []
        self.load_persons()

    def fetch_cookies(self):
        options = webdriver.ChromeOptions()
        options.add_argument("mute-audio")
        options.add_argument("disable-gpu")
        options.add_argument("log-level=3")
        options.add_argument("hide-scrollbars")
        options.add_argument("headless")

        driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
        driver.get(hopla_url)
        self.cookies = driver.get_cookies()
        driver.close()

    def fetch_calendar(self):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Cookie": "; ".join([cookie["name"] + "=" + cookie["value"] for cookie in self.cookies])
        }
        data = {
            "startDate": "2019-03-01",
            "collection": "events",
            "projectId": "5c735e75d5de9fb38da25c1a",
            "nbMonths": "3",
            "action": "get"
        }
        req = requests.post(hopla_calendar_url, headers=headers, data=data, verify=False)
        if req.status_code != 200:
            raise Exception("Erreur dans la récupération des données")
        with open(calendar_file, "wb") as f:
            f.write(req.content)
        self.calendar = req.json()

    def load_calendar(self):
        with open(calendar_file) as f:
            self.calendar = json.load(f)

    def load_persons(self):
        self.persons = [Person(person["first_name"] + " " + person["last_name"]) for person in self.calendar["users"]]
        self.print_persons()

    def determine_croissanistes(self, datetime_object):
        most_petential_person = None
        max_potential = 0
        for person in self.persons:
            if not person.is_in_holiday(datetime_object) and person.potential >= max_potential:
                max_potential = person.potential
                most_petential_person = person

        for person in self.persons:
            if person != most_petential_person:
                person.potential += 1
            else:
                person.potential = 0

    def print_persons(self):
        for person in self.persons:
            print(person.name, person.potential)

    def print_holidays(self):
        for person in self.persons:
            print(person.name, person.holiday)

    def test(self):
        datetime_object = datetime.datetime.strptime("2019-03-29", "%Y-%m-%d")

        for i in range(len(self.persons)):
            for j in range(31):
                day = None
                try:
                    if "type" in self.calendar["users"][i]["days"][j].keys():
                        day = self.calendar["users"][i]["days"][j]
                except:
                    day = self.calendar["users"][i]["days"][j][0]
                if day is not None and day["type"] not in ["day_off", "RAS"]:
                    self.persons[i].add_holiday(day["date"])

        for i in range(5):
            print("before")
            self.print_persons()
            self.determine_croissanistes(datetime_object.strftime("%Y-%m-%d"))
            print("after")
            self.print_persons()
            datetime_object = datetime_object + datetime.timedelta(days=7)


solver = Solver()
solver.test()
