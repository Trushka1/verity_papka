from repository_layer import MemoryRepository
from service_layer import RestaurantService


MENU = """
1. добавить блюдо в меню_ありがと
2. показать меню ресторана_😺
3. изменить цену блюда_💕
4. удалить блюдо из меню_😒
5. открыть заказ_(●'◡'●)
6. добавить блюдо в заказ_✌️
7. показать заказ_😶‍🌫️
8. закрыть заказ_😛
0. выйти-_- 67
"""

def read_positive_integer(prompt):
    # input возвращает строку, поэтому сначала надо переводести её в число
    try:
        number = int(input(prompt))
    except ValueError:
        raise ValueError("введите целое число") from None
    if number < 1:
        raise ValueError("число должно быть больше нуля")
    return number


def print_order_details(service, order):
    status = "закрыт" if order.is_closed else "открыт"
    print(f"заказ №{order.id}, столик №{order.table_number}, {status}")
    if not order.items:
        print("в заказе пока нет блюд")
    for order_item in order.items:
        print(f"{order_item.dish_name} — {order_item.quantity} шт. "
              f"по {order_item.price} руб.")
    print(f"итого: {service.calculate_order_total(order)} руб.")


def main():
    # блюда и заказы хранятся в разных словарях____67
    dish_repository = MemoryRepository()
    order_repository = MemoryRepository()
    service = RestaurantService(dish_repository, order_repository)

    while True:
        try:
            print(MENU)
            menu_choice = input("выберите действие: ").strip()

            if menu_choice == "0":
                break
            elif menu_choice == "1":
                name = input("название блюда: ")
                price = read_positive_integer("цена в рублях: ")
                dish = service.add_menu_dish(name, price)
                print(f"блюдо добавлено, ID: {dish.id}")
            elif menu_choice == "2":
                dishes = service.list_menu_dishes()
                if not dishes:
                    print("в меню пока нет блюд")
                for dish in dishes:
                    print(f"{dish.id}. {dish.name} — {dish.price} руб.")
            elif menu_choice == "3":
                dish_id = read_positive_integer("ID блюда: ")
                price = read_positive_integer("новая цена в рублях: ")
                service.change_dish_price(dish_id, price)
                print("цена изменена")
            elif menu_choice == "4":
                dish_id = read_positive_integer("ID блюда: ")
                service.remove_menu_dish(dish_id)
                print("блюдо удалено из меню")
            elif menu_choice == "5":
                table_number = read_positive_integer("номер столика: ")
                order = service.open_order(table_number)
                print(f"заказ открыт, ID: {order.id}")
            elif menu_choice == "6":
                order_id = read_positive_integer("ID заказа: ")
                dish_id = read_positive_integer("ID блюда: ")
                quantity = read_positive_integer("количество порций: ")
                service.add_dish_to_order(order_id, dish_id, quantity)
                print("блюдо добавлено в заказ")
            elif menu_choice == "7":
                order_id = read_positive_integer("ID заказа: ")
                print_order_details(service, service.get_order(order_id))
            elif menu_choice == "8":
                order_id = read_positive_integer("ID заказа: ")
                order = service.close_order(order_id)
                print_order_details(service, order)
            else:
                print("такого пункта меню нет")
        # после ошибки меню снова появляется на следующем шаге цикла.
        except ValueError as error:
            print(f"ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print()
            break

    print("программа завершена")


if __name__ == "__main__":
    main()
