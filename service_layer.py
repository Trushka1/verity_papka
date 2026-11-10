from data_layer import Dish, Order, OrderItem
from repository_layer import Repository


class RestaurantService:
    def __init__(self, dish_repository: Repository,
                 order_repository: Repository):
        self.dish_repository = dish_repository
        self.order_repository = order_repository

    def add_menu_dish(self, name, price):
        name = name.strip()
        if not name:
            raise ValueError("название блюда не может быть пустым")
        if price < 1:
            raise ValueError("цена должна быть больше нуля")
        return self.dish_repository.add(Dish(name, price))

    def list_menu_dishes(self):
        return self.dish_repository.get_all()

    def change_dish_price(self, dish_id, price):
        if price < 1:
            raise ValueError("цена должна быть больше нуля")
        dish = self.dish_repository.get(dish_id)
        dish.price = price
        return self.dish_repository.update(dish)

    def remove_menu_dish(self, dish_id):
        self.dish_repository.delete(dish_id)

    def open_order(self, table_number):
        if table_number < 1:
            raise ValueError("номер столика должен быть больше нуля")
        return self.order_repository.add(Order(table_number))

    def get_order(self, order_id):
        return self.order_repository.get(order_id)

    # добавление блюда и закрытие требуют открытого заказа
    def _get_open_order(self, order_id):
        order = self.get_order(order_id)
        if order.is_closed:
            raise ValueError("заказ уже закрыт")
        return order

    def add_dish_to_order(self, order_id, dish_id, quantity):
        if quantity < 1:
            raise ValueError("количество должно быть больше нуля")
        order = self._get_open_order(order_id)
        dish = self.dish_repository.get(dish_id)
        # копируем цену из меню, чтобы её изменение не затронуло заказ
        order.items.append(OrderItem(dish.name, dish.price, quantity))
        return self.order_repository.update(order)

    def calculate_order_total(self, order):
        total_price = 0
        for order_item in order.items:
            total_price += order_item.price * order_item.quantity
        return total_price

    def close_order(self, order_id):
        order = self._get_open_order(order_id)
        # закрываем заказ, только если в нём есть хотя бы одна позиция
        if not order.items:
            raise ValueError("сначала добавьте блюдо в заказ")
        order.is_closed = True
        return self.order_repository.update(order)

