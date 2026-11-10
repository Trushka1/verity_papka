class Dish:
    # id назначается при сохранении блюда в репозитории
    def __init__(self, name, price):
        self.id = None
        self.name = name
        self.price = price


class OrderItem:
    # позиция запоминает название и цену на момент добавления в заказ
    def __init__(self, dish_name, price, quantity):
        self.dish_name = dish_name
        self.price = price
        self.quantity = quantity


class Order:
    # у каждого заказа свой список позиций
    def __init__(self, table_number):
        self.id = None
        self.table_number = table_number
        self.items = []
        self.is_closed = False
