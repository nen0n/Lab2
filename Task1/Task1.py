import json
import uuid
import datetime
from datetime import datetime


class Event:
    def __init__(self, name):
        self.name = name

    def GenerateTicket(self, customer):
        with open("TickersForEvent.json") as f:
            data = json.load(f)[self.name]
        date = data["Date"]
        delta = datetime(*list(map(int, date.split("-")))) - datetime.now()
        if customer.isstudent:
            amount = data["Tickets"]["StudentTicket"]["Amount"]
            if amount > 0:
                with open("TickersForEvent.json", "r") as f:
                    data = json.load(f)
                data[self.name]["Tickets"]["StudentTicket"]["Amount"] = amount - 1
                with open("TickersForEvent.json", "w") as f:
                    json.dump(data, f, indent=4)
                ticket = StudentTicket(customer, self.name)
                with open("ListOfTickets.json", "r", encoding="utf-8") as out:
                    ticket_data = json.load(out)
                if not ticket_data:
                    ticket_data = {}
                if str(ticket.id) not in ticket_data:
                    ticket_data[str(ticket.id)] = {}
                ticket_data[str(ticket.id)]["Event"] = self.name
                ticket_data[str(ticket.id)]["Name"] = customer.name
                ticket_data[str(ticket.id)]["Surname"] = customer.surname
                ticket_data[str(ticket.id)]["Cost"] = ticket.get_price()
                ticket_data[str(ticket.id)]["Type of ticket"] = "Student"
                ticket_data[str(ticket.id)]["Date"] = date
                with open("ListOfTickets.json", "w") as out:
                    json.dump(ticket_data, out, indent=4)
                return ticket
            else:
                raise ValueError("Run out of tickets")
        elif delta.days >= 60:
            amount = data["Tickets"]["AdvanceTicket"]["Amount"]
            if amount > 0:
                with open("TickersForEvent.json", "r") as f:
                    data = json.load(f)
                data[self.name]["Tickets"]["AdvanceTicket"]["Amount"] = amount - 1
                with open("TickersForEvent.json", "w") as f:
                    json.dump(data, f, indent=4)
                ticket = AdvanceTicket(customer, self.name)
                with open("ListOfTickets.json", "r", encoding="utf-8") as out:
                    ticket_data = json.load(out)
                if not ticket_data:
                    ticket_data = {}
                if str(ticket.id) not in ticket_data:
                    ticket_data[str(ticket.id)] = {}
                ticket_data[str(ticket.id)]["Event"] = self.name
                ticket_data[str(ticket.id)]["Name"] = customer.name
                ticket_data[str(ticket.id)]["Surname"] = customer.surname
                ticket_data[str(ticket.id)]["Cost"] = ticket.get_price()
                ticket_data[str(ticket.id)]["Type of ticket"] = "Advance"
                ticket_data[str(ticket.id)]["Date"] = date
                with open("ListOfTickets.json", "w") as out:
                    json.dump(ticket_data, out, indent=4)
                return ticket
            else:
                raise ValueError("Run out of tickets")
        elif delta.days < 10:
            amount = data["Tickets"]["LateTicket"]["Amount"]
            if amount > 0:
                with open("TickersForEvent.json", "r") as f:
                    data = json.load(f)
                data[self.name]["Tickets"]["AdvanceTicket"]["Amount"] = amount - 1
                with open("TickersForEvent.json", "w") as f:
                    json.dump(data, f, indent=4)
                ticket = LateTicket(customer, self.name)
                with open("ListOfTickets.json", "r", encoding="utf-8") as out:
                    ticket_data = json.load(out)
                if not ticket_data:
                    ticket_data = {}
                if str(ticket.id) not in ticket_data:
                    ticket_data[str(ticket.id)] = {}
                ticket_data[str(ticket.id)]["Event"] = self.name
                ticket_data[str(ticket.id)]["Name"] = customer.name
                ticket_data[str(ticket.id)]["Surname"] = customer.surname
                ticket_data[str(ticket.id)]["Cost"] = ticket.get_price()
                ticket_data[str(ticket.id)]["Type of ticket"] = "Late"
                ticket_data[str(ticket.id)]["Date"] = date
                with open("ListOfTickets.json", "w") as out:
                    json.dump(ticket_data, out, indent=4)
                return ticket
            else:
                raise ValueError("Run out of tickets")
        else:
            amount = data["Tickets"]["RegularTicket"]["Amount"]
            if amount > 0:
                with open("TickersForEvent.json", "r") as f:
                    data = json.load(f)
                data[self.name]["Tickets"]["AdvanceTicket"]["Amount"] = amount - 1
                with open("TickersForEvent.json", "w") as f:
                    json.dump(data, f, indent=4)
                ticket = RegularTicket(customer, self.name)
                with open("ListOfTickets.json", "r", encoding="utf-8") as out:
                    ticket_data = json.load(out)
                if not ticket_data:
                    ticket_data = {}
                if str(ticket.id) not in ticket_data:
                    ticket_data[str(ticket.id)] = {}
                ticket_data[str(ticket.id)]["Event"] = self.name
                ticket_data[str(ticket.id)]["Name"] = customer.name
                ticket_data[str(ticket.id)]["Surname"] = customer.surname
                ticket_data[str(ticket.id)]["Cost"] = ticket.get_price()
                ticket_data[str(ticket.id)]["Type of ticket"] = "Regular"
                ticket_data[str(ticket.id)]["Date"] = date
                with open("ListOfTickets.json", "w") as out:
                    json.dump(ticket_data, out, indent=4)
                return ticket
            else:
                raise ValueError("Run out of tickets")



class Customer:
    def __init__(self, name, surname, isstudent):
        self.name = name
        self.surname = surname
        self.isstudent = isstudent
        self.tickets = []

    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Wrong type for 'name' atribute")
        self.__name = value


    @property
    def surname (self):
        return self.__surname


    @surname.setter
    def surname (self, value):
        if not isinstance(value, str):
            raise TypeError("Wrong type for 'surname' atribute")
        self.__surname = value


    @property
    def isstudent (self):
        return self.__isstudent


    @isstudent.setter
    def isstudent (self, value):
        if not isinstance(value, bool):
            raise TypeError("Wrong type for 'isstudent' atribute")
        self.__isstudent = value


    def BuyTicket(self, event : Event):
        self.tickets.append(event.GenerateTicket(self))

    def ShowTickets(self):
        for ticket in self.tickets:
            print(ticket)


class Ticket:
    def __init__(self, customer: Customer, name_of_event):
        self.name = customer.name
        self.surname = customer.surname
        self.name_of_event = name_of_event
        self.id = str(uuid.uuid1())


class RegularTicket(Ticket):
    def __init__(self, customer: Customer, name_of_event) -> None:
        super().__init__(customer, name_of_event)
        with open("TickersForEvent.json", encoding="utf-8") as f:
            data = json.load(f)[self.name_of_event]
        self.price = data["Tickets"]["Cost"]
        self.discount = data["Tickets"]["RegularTicket"]["Discount"]
        self.date = data["Date"]

    def get_price(self):
        return (1 - self.discount) * self.price


    def __str__(self):
        return f"Ticket: {self.id}\nCustomer: {self.surname} {self.name}" \
               f"\nEvent: {self.name_of_event}\nDate: {self.date}" \
               f"\nType of ticket: Regular\nCost: {self.get_price()}\n"


class AdvanceTicket(Ticket):
    def __init__(self, customer: Customer, name_of_event) -> None:
        super().__init__(customer, name_of_event)
        with open("TickersForEvent.json", encoding="utf-8") as f:
            data = json.load(f)[self.name_of_event]
        self.price = data["Tickets"]["Cost"]
        self.discount = data["Tickets"]["AdvanceTicket"]["Discount"]
        self.date = data["Date"]

    def get_price(self):
        return (1 - self.discount) * self.price


    def __str__(self):
        return f"Ticket: {self.id}\nCustomer: {self.surname} {self.name}" \
               f"\nEvent: {self.name_of_event}\nDate: {self.date}" \
               f"\nType of ticket: Advance\nCost: {self.get_price()}\n"


class LateTicket(Ticket):
    def __init__(self, customer: Customer, name_of_event) -> None:
        super().__init__(customer, name_of_event)
        with open("TickersForEvent.json", encoding="utf-8") as f:
            data = json.load(f)[self.name_of_event]
        self.price = data["Tickets"]["Cost"]
        self.discount = data["Tickets"]["LateTicket"]["Discount"]
        self.date = data["Date"]

    def get_price(self):
        return (1 - self.discount) * self.price


    def __str__(self):
        return f"Ticket: {self.id}\nCustomer: {self.surname} {self.name}" \
               f"\nEvent: {self.name_of_event}\nDate: {self.date}" \
               f"\nType of ticket: Late\nCost: {self.get_price()}\n"


class StudentTicket(Ticket):
    def __init__(self, customer: Customer, name_of_event) -> None:
        super().__init__(customer, name_of_event)
        with open("TickersForEvent.json", encoding="utf-8") as f:
            data = json.load(f)
        self.price = data[self.name_of_event]["Tickets"]["Cost"]
        self.discount = data[self.name_of_event]["Tickets"]["StudentTicket"]["Discount"]
        self.date = data[self.name_of_event]["Date"]

    def get_price(self):
        return (1 - self.discount) * self.price


    def __str__(self):
        return f"Ticket: {self.id}\nCustomer: {self.surname} {self.name}" \
               f"\nEvent: {self.name_of_event}\nDate: {self.date}" \
               f"\nType of ticket: Student\nCost: {self.get_price()}\n"


def GetTicketById(id: str):
    with open("ListOfTickets.json", "r", encoding="utf-8") as f:
        database = json.load(f)
    ticket = database[id]
    print(ticket)


event1 = Event("Hallapalooza")
event2 = Event("BurningMan")

customer1 = Customer("Yevheniy", "Zdesenko", True)
customer2 = Customer("Anton", "Dzulay", False)

customer1.BuyTicket(event1)
customer1.BuyTicket(event2)

customer2.BuyTicket(event1)

customer1.ShowTickets()
customer2.ShowTickets()

GetTicketById("ff7242c6-5ff5-11ed-a12e-f02f7449c3e4")