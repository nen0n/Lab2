import json
import uuid
import datetime
from datetime import datetime

class Order():
    def __init__(self):
        self.id = str(uuid.uuid1())
        self.pizzas = []

    def AddSelfMadePizza(self, *additional_ingridients):
        if not additional_ingridients:
            raise ValueError("No ingredients in pizza")
        pizza = SelfMadePizza(additional_ingridients)
        self.pizzas.append(pizza)

    def AddPizzaOfTheDay(self, *additional_ingridients):
        pizza = PizzaOfTheDay(additional_ingridients)
        self.pizzas.append(pizza)

    def GetOrder(self):
        with open("Order.json", encoding="utf-8") as f:
            order = json.load(f)
            if not order:
                order = {}
            if str(self.id) not in order:
                order[self.id] = {}
            i = 1
            for pizza in self.pizzas:
                order[self.id][i] = {}
                order[self.id][i]["Name"] = pizza.name
                order[self.id][i]["Ingredients"] = pizza.ingredients
                order[self.id][i]["Price"] = pizza.price
                i += 1
        with open("Order.json", "w", encoding="utf-8") as f:
            json.dump(order, f)


    def __str__(self):
        return f'\nId of Order:{self.id}\nPizzas:\n{"".join(list(map(str, self.pizzas)))}'


class Pizza():
    def __init__(self, *additional_ingridients):
        self.AdditionalIngredients = []
        for ingredient in additional_ingridients:
            self.AdditionalIngredients.append(ingredient)

class SelfMadePizza(Pizza):
    def __init__(self, *additional_ingridients):
        super().__init__(*additional_ingridients)
        self.name = "SelfMade"
        self.price = 0
        self.ingredients = []
        if self.AdditionalIngredients[0]:
            with open("ListOfIngridients.json", encoding="utf-8") as f:
                ingr = json.load(f)
                for current_ingredient in self.AdditionalIngredients[0]:
                    self.ingredients.append(current_ingredient)
                    self.price += ingr[current_ingredient]

    def __str__(self):
        return f'\nPizzas name: {self.name}\nIngredients: {" ".join(self.ingredients)}\nCost: {self.price}\n\n'


class PizzaOfTheDay(Pizza):
    def __init__(self, *additional_ingridients):
        super().__init__(*additional_ingridients)
        DayOfWeek = datetime.now().strftime('%A')
        with open("TypesOfPizza.json", encoding="utf-8") as f:
            data = json.load(f)[DayOfWeek]
        self.price = data["price"]
        self.ingredients = data["ingredients"]
        self.name = data["name"]
        if self.AdditionalIngredients[0]:
            with open("ListOfIngridients.json", encoding="utf-8") as f:
                ingr = json.load(f)
                for current_ingredient in self.AdditionalIngredients[0]:
                    self.ingredients.append(current_ingredient)
                    self.price += ingr[str(current_ingredient)]

    def __str__(self):
        return f'\nPizzas name: {self.name}\nIngredients: {" ".join(self.ingredients)}\nCost: {self.price}'

Person = Order()
Person.AddPizzaOfTheDay("Ham", "Ham")
Person.AddSelfMadePizza("Ham", "Ham")
print(Person)
Person.GetOrder()
