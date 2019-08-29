import unidecode

pictures_url = "http://10.24.216.11:3000/img/collaborator/100x100/"


class Person:
    def __init__(self, person):
        self.last_name = str(person["last_name"]).upper()
        self.first_name = str(person["first_name"]).capitalize()
        self.filter_name = self.first_name + " " + self.last_name
        self.name = unidecode.unidecode(self.filter_name)
        self.picture = pictures_url + self.last_name + "%20" + self.first_name + ".jpg"
        self.holiday = []
        self.potential = 0
        self.email = self.get_email()
      
        days = person["days"]
        for j in range(len(days)):
            day = None
            try:
                if "type" in days[j].keys():
                    day = days[j]
            except:
                day = days[j][0]
            if day is not None and day["type"] not in ["day_off", "RAS"]:
                self.add_holiday(day["date"])

    def add_holiday(self, holiday):
        self.holiday.append(holiday)

    def is_in_holiday(self, date):
        return str(date) in self.holiday

    def dict(self, friday):
        return {
            "name": self.name,
            "email": self.email,
            "picture": self.picture,
            "friday": str(friday)
        }

    def get_email(self):
        first_name = self.first_name.replace(" ", "-").lower()
        last_name = self.last_name.lower()
        email_addr = first_name + "." + last_name + "@capgemini.com"
        return unidecode.unidecode(email_addr)
