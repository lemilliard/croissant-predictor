import json
import datetime

from person import Person
from fetcher import Fetcher


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
    def calculate_potentials(persons, friday, most_potential_persons):
        for person in persons:
            if person in most_potential_persons:
                person.potential = 0
            else:
                person.potential += 1
        #Solver.save_calculate_potential(persons, friday)

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
                with open('potential.json', 'w') as f:
                    json.dump(calculate_potential, f)
                    return calculate_potential
            return potential
        except:
            with open('potential.json', 'w') as f:
                potential = {
                    "date": Solver.get_next_friday().strftime("%Y-%m-%d"),
                    "potential": None
                }
                json.dump(potential, f)
            return None

    @staticmethod
    def get_most_potential_persons(persons, n, filter, friday):
        most_potential_person = None
        most_potential_persons = []
        tmp_persons = persons.copy()
        for i in range(n):
            max_potential = 0
            for person in tmp_persons:
                if person.potential >= max_potential and not person.is_in_holiday(friday):
                    if filter is not None:
                        if person.name in filter:
                            max_potential = person.potential
                            most_potential_person = person
                    else:
                        max_potential = person.potential
                        most_potential_person = person
            if most_potential_person is not None:
                most_potential_persons.append(most_potential_person)
                tmp_persons.remove(most_potential_person)
                most_potential_person = None
        return most_potential_persons

    @staticmethod
    def get_first_day_of_current_month():
        return datetime.date.today().replace(day=1)

    @staticmethod
    def get_next_friday():
        d = datetime.date.today() + datetime.timedelta(1)
        while d.weekday() != 4:
            d += datetime.timedelta(1)
        return d

    def define_croissanists(self, project_id, months, n, filter=None):
        potential = self.load_potential()

        calendar = self.fetcher.load_calendar(project_id, self.get_first_day_of_current_month(), months)

        persons = self.update_persons(calendar, potential)

        friday = self.get_next_friday()

        croissanists = []

        most_potentials_persons = []

        for i in range(months * 4):
            print("----------------------------")
            print(friday)
            print("----------------------------")
            print("\n".join([p.name + " -> " + str(p.potential) for p in persons]))
            most_potentials_persons = self.get_most_potential_persons(persons, n, filter=filter, friday=friday)
            [croissanists.append(person.dict(friday)) for person in most_potentials_persons]
            self.calculate_potentials(persons, friday, most_potentials_persons)
            if i == 0:
              Solver.save_calculate_potential(persons, friday)
            friday += datetime.timedelta(7)

        return croissanists

    def get_persons(self, project_id, months):
        calendar = self.fetcher.load_calendar(project_id, self.get_first_day_of_current_month(), months)
        persons = [{"name": str(person["first_name"]).capitalize() + " " + str(person["last_name"]).upper()} for person in calendar["users"]]
        return persons
