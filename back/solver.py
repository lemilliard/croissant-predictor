import json
import datetime
import os
import time
import pythoncom

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
                try:
                    person.potential = potential["potential"][person.name]
                except:
                    person.potential = 0
        return persons

    @staticmethod
    def calculate_potentials(persons, friday, most_potential_persons):
        for person in persons:
            if person in most_potential_persons:
                person.potential = 0
            else:
                person.potential += 1

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
                        if person.filter_name in filter:
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

        calendar = self.fetcher.load_calendar(project_id, self.get_first_day_of_current_month(), months + 1)

        persons = self.update_persons(calendar, potential)

        friday = self.get_next_friday()

        self.pop_potential(friday, potential["date"], persons)

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
            if len(most_potentials_persons) > 0:
                print(most_potentials_persons[0].name)
            friday += datetime.timedelta(7)
        friday -= datetime.timedelta(7)
        Solver.save_calculate_potential(persons, friday)
        saved, added = self.save_croissanists(croissanists)
        self.delete_meeting(persons, saved)
        self.generate_meeting(added)
        
        return croissanists

    def get_persons(self, project_id, months):
        calendar = self.fetcher.load_calendar(project_id, self.get_first_day_of_current_month(), months)
        persons = [{"name": str(person["first_name"]).capitalize() + " " + str(person["last_name"]).upper()} for person
                   in calendar["users"]]
        return persons

    def pop_potential(self, current_friday, saved_friday, persons):
        saved_friday = datetime.datetime.strptime(saved_friday, "%Y-%m-%d").date()
        while current_friday <= saved_friday:
            max_persons = []
            max_potential = 0
            for person in persons:
                if person.potential > 0 and person.potential < 99:
                    if person.potential > max_potential:
                        max_potential = person.potential
                    person.potential -= 1
                elif person.potential == 0:
                    person.potential = 99
                else:
                    max_persons.append(person)
            for person in max_persons:
                person.potential = max_potential
            saved_friday -= datetime.timedelta(7)
      
    def delete_meeting(self, persons, saved):
        import win32com.client
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        ns = outlook.GetNamespace("MAPI")
        names = []
        for person in persons:
            names.append(person.name)
            
        for p in saved:
            if p['name'] in names:
                print(p['name'])
                names.remove(p['name'])
            
        print('names', names)
        
        for name in names:
            meetings = ns.GetDefaultFolder(9).Items
            meetings = meetings.Restrict("[Subject] = 'Croissant " + name + "'")
            
            for meeting in meetings:
                meeting.Delete()
                time.sleep(0.1)
        pythoncom.CoUninitialize()

    def generate_meeting(self, added):
        import win32com.client
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch("Outlook.Application")
        print('added', added)
        
        for croissanist in added:
            appt = outlook.CreateItem(1)

            date_croissant = datetime.datetime.strptime(croissanist['friday'], "%Y-%m-%d").date()
            date_croissant -= datetime.timedelta(1)
            appt.Start = date_croissant.strftime("%Y-%m-%d") + " 10:00"  # yyyy-MM-dd hh:mm
            appt.Subject = "Croissant " + croissanist['name']
            appt.Duration = 30
            appt.Location = "Location Name"
            appt.MeetingStatus = 1

            # appt.Recipients.Add(croissanist['email])
            appt.Recipients.Add("kevin.bouzan@capgemini.com")

            appt.Save()
            appt.Send()
            time.sleep(0.1)
        pythoncom.CoUninitialize()

    def save_croissanists(self, croissanists):
        updated = []
        saved = []
        added = []
        try:
            with open('croissanists.json', 'r') as f:
                last_persons = json.load(f)
        except:
            last_persons = None
            print('Exception when opening file')
            
        if last_persons is not None:
            for croissanist in croissanists:
                try:
                    if last_persons[croissanist['name']] != croissanist['friday']:
                        last_persons[croissanist['name']] = croissanist['friday']
                        updated.append(croissanist)
                    else:
                        saved.append(croissanist)
                except:
                    print('Exception because there are not the searching name')
                    added.append(croissanist)
                  
            saved += added
            saved_dict = dict([(p['name'], p['friday']) for p in saved+updated])
        else:
            added = croissanists
            saved = added
            saved_dict = dict([(p['name'], p['friday']) for p in saved])
            
        with open('croissanists.json', 'w') as f:
            json.dump(saved_dict, f)
        
        return saved, added + updated
        