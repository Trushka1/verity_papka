import tempfile
import unittest
from pathlib import Path

from data_layer import Dish, Order
from json_repository import JsonRepository
from repository_layer import MemoryRepository
from service_layer import RestaurantService


class RestaurantServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = RestaurantService(
            MemoryRepository(),
            MemoryRepository(),
        )

    def test_order_keeps_price_from_time_of_addition(self):
        dish = self.service.add_menu_dish("Суп", 250)
        order = self.service.open_order(3)

        self.service.add_dish_to_order(order.id, dish.id, 2)
        self.service.change_dish_price(dish.id, 300)

        updated_order = self.service.get_order(order.id)
        self.assertEqual(
            self.service.calculate_order_total(updated_order),
            500,
        )

    def test_empty_order_cannot_be_closed(self):
        order = self.service.open_order(3)

        with self.assertRaises(ValueError):
            self.service.close_order(order.id)

    def test_closed_order_cannot_be_changed(self):
        dish = self.service.add_menu_dish("Суп", 250)
        order = self.service.open_order(3)
        self.service.add_dish_to_order(order.id, dish.id, 1)
        self.service.close_order(order.id)

        with self.assertRaises(ValueError):
            self.service.add_dish_to_order(order.id, dish.id, 1)

    def test_json_data_is_restored_after_repository_restart(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_directory = Path(temporary_directory)

            dish_repository = JsonRepository(
                data_directory / "dishes.json",
                Dish,
            )
            order_repository = JsonRepository(
                data_directory / "orders.json",
                Order,
            )
            service = RestaurantService(dish_repository, order_repository)

            dish = service.add_menu_dish("Суп", 250)
            order = service.open_order(3)
            service.add_dish_to_order(order.id, dish.id, 2)

            # создаём хранилища заново, как после перезапуска программы
            dish_repository = JsonRepository(
                data_directory / "dishes.json",
                Dish,
            )
            order_repository = JsonRepository(
                data_directory / "orders.json",
                Order,
            )
            restored_service = RestaurantService(
                dish_repository,
                order_repository,
            )

            restored_order = restored_service.get_order(order.id)
            self.assertEqual(
                restored_service.calculate_order_total(restored_order),
                500,
            )
            self.assertEqual(restored_service.list_menu_dishes()[0].name, "Суп")


if __name__ == "__main__":
    unittest.main()