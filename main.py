import json
import datetime
import requests

from selenium import webdriver

hopla_url = 'https://hopla2.fr.capgemini.com'
hopla_calendar_url = 'https://hopla2.fr.capgemini.com/Calendar'
JSESSIONID_cookie = None
JSESSIONID_cookie_name = 'JSESSIONID'
brandNewDayProd_cookie = None
brandNewDayProd_cookie_name = 'brandNewDayProd'


class Person:
    def __init__(self, name):
        self.name = name
        self.holiday = []
        self.potential = 0

    def add_holiday(self, holiday):
        datetime_object = datetime.datetime.strptime(holiday, '%Y-%m-%d')
        self.holiday.append(holiday)

    def is_in_holiday(self, date):
        if date in self.holiday:
            return True
        else:
            return False


class Solver:
    @staticmethod
    def fetch_cookie():
        global JSESSIONID_cookie
        global brandNewDayProd_cookie
        options = webdriver.ChromeOptions()
        options.add_argument("mute-audio")
        options.add_argument('disable-gpu')
        options.add_argument('log-level=3')
        options.add_argument('hide-scrollbars')
        options.add_argument("headless")

        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
        driver.get(hopla_url)
        JSESSIONID_cookie = driver.get_cookie(JSESSIONID_cookie_name)
        brandNewDayProd_cookie = driver.get_cookie(brandNewDayProd_cookie_name)
        driver.close()

    @staticmethod
    def get_json_schedule():
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': JSESSIONID_cookie_name + '=' + JSESSIONID_cookie[
                'value'] + ';' + brandNewDayProd_cookie_name + '=' + brandNewDayProd_cookie['value']
        }
        data = {
            'startDate': '2019-03-01',
            'collection': 'events',
            'projectId': '5c735e75d5de9fb38da25c1a',
            'nbMonths': '3',
            'action': 'get'
        }
        req = requests.post(hopla_calendar_url, headers=headers, data=data, verify=False)
        with open('bam.json', 'wb') as f:
            f.write(req.content)

    @staticmethod
    def determine_croissaniste(group, datetime_object):
        most_petential_person = None
        max_potential = 0
        for person in group:
            if not person.is_in_holiday(datetime_object) and person.potential >= max_potential:
                max_potential = person.potential
                most_petential_person = person

        for person in group:
            if person != most_petential_person:
                person.potential += 1
            else:
                person.potential = 0

    @staticmethod
    def print_array_info(array):
        for person in array:
            print(person.name, person.potential)

    @staticmethod
    def print_all_holiday(array):
        for person in array:
            print(person.name, person.holiday)

    @staticmethod
    def load_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    @classmethod
    def solve_problem(cls):
        cls.fetch_cookie()
        print(JSESSIONID_cookie)
        print(brandNewDayProd_cookie)
        cls.get_json_schedule()


#
# group = [Person('bob'), Person('alice'), Person('test')]
# datetime_object = datetime.datetime.strptime('2019-03-29', '%Y-%m-%d')
# json_schedule = load_json('planning.json')
#
# for i in range(len(group)):
#     for j in range(31):
#         day = None
#         try:
#             if 'type' in json_schedule['users'][i]['days'][j].keys():
#                 day = json_schedule['users'][i]['days'][j]
#         except:
#             day = json_schedule['users'][i]['days'][j][0]
#         if day != None and day['type'] not in ['day_off', 'RAS']:
#             group[i].add_holiday(day['date'])
#
# for i in range(5):
#     print('before')
#     print_array_info(group)
#     determine_croissaniste(group, datetime_object.strftime('%Y-%m-%d'))
#     print('after')
#     print_array_info(group)
#     datetime_object = datetime_object + datetime.timedelta(days=7)

Solver.solve_problem()
