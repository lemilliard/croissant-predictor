import json
import datetime

from person import Person
from fetcher import Fetcher


class Solver:
    def __init__(self):
        self.fetcher = Fetcher()

    @staticmethod
    def get_persons(calendar):
        return [Person(person) for person in calendar["users"]]

    @staticmethod
    def calculate_potentials(persons, friday):
        max_potential = 0
        most_potential_person = None
        for person in persons:
            if not person.is_in_holiday(friday) and person.potential >= max_potential:
                max_potential = person.potential
                most_potential_person = person

        for person in persons:
            if person != most_potential_person:
                person.potential += 1
            else:
                person.potential = 0

    @staticmethod
    def get_most_potential_person(persons):
        max_potential = 0
        most_potential_person = None
        for person in persons:
            if person.potential >= max_potential:
                max_potential = person.potential
                most_potential_person = person
        return most_potential_person

    @staticmethod
    def get_first_day_of_current_month():
        return datetime.date.today().replace(day=1)

    @staticmethod
    def get_next_friday():
        d = datetime.date.today()
        while d.weekday() != 4:
            d += datetime.timedelta(1)
        return d

    def define_croissanists(self, project_id, months):
        calendar = self.fetcher.load_calendar(project_id, self.get_first_day_of_current_month(), months)
        persons = self.get_persons(calendar)

        friday = self.get_next_friday()

        croissanists = []

        for i in range(months * 4):
            self.calculate_potentials(persons, friday)
            print("----------------------------")
            print(friday)
            print("----------------------------")
            print("\n".join([p.name + " -> " + str(p.potential) for p in persons]))
            croissanists.append(self.get_most_potential_person(persons).dict(friday))
            friday += datetime.timedelta(7)

        return croissanists
