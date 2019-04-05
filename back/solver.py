import json
import datetime

from back.person import Person
from back.fetcher import Fetcher


class Solver:
    def __init__(self):
        self.fetcher = Fetcher()

    @staticmethod
    def update_persons(calendar, potential):
        persons = [Person(person) for person in calendar["users"]]
        if potential is not None and potential["potential"] is not None:
            for person in persons:
                person.potential = potential["potential"][person.name]
        return persons

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
        Solver.save_calculate_potential(persons, friday)

    @staticmethod
    def save_calculate_potential(persons, friday):
        potential = {
            "date": friday.strftime("%Y-%m-%d"),
            "potential": dict([(p.name, p.potential) for p in persons])
        }
        with open('calculate_potential.json', 'w') as f:
            json.dump(potential, f)

    @staticmethod
    def load_potential():
        try:
            with open('calculate_potential.json', 'r') as calc_f:
                calculate_potential = json.load(calc_f)
            try:
                with open('potential.json', 'r') as f:
                    potential = json.load(f)
            except:
                with open('potential.json', 'w') as f:
                    potential = {
                        "date": Solver.get_next_friday().strftime("%Y-%m-%d"),
                        "potential": None
                    }
                    json.dump(potential, f)
            d = datetime.datetime.strptime(potential["date"], "%Y-%m-%d").date()
            if d < datetime.date.today():
                json.dump(calculate_potential, f)
                return calculate_potential
            return potential
        except:
            return None

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
        potential = self.load_potential()

        calendar = self.fetcher.load_calendar(project_id, self.get_first_day_of_current_month(), months)

        persons = self.update_persons(calendar, potential)

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
