import json
from pathlib import Path

from data_layer import Dish, Order, OrderItem
from repository_layer import Repository


class JsonRepository(Repository):
    def __init__(self, file_path, entity_type):
        if entity_type not in (Dish, Order):
            raise TypeError("поддерживаются только Dish и Order")

        self._file_path = Path(file_path)
        self._entity_type = entity_type
        self._entities_by_id = {}
        self._next_id = 1
        self._load()

    def _load(self):
        if not self._file_path.exists():
            self._save()
            return

        data = json.loads(self._file_path.read_text(encoding="utf-8"))

        if not isinstance(data, list):
            raise ValueError("корень JSON-файла должен быть списком")

        for item_data in data:
            if self._entity_type is Dish:
                entity = Dish(item_data["name"], item_data["price"])
            else:
                entity = Order(item_data["table_number"])
                entity.items = [
                    OrderItem(
                        item["dish_name"],
                        item["price"],
                        item["quantity"],
                    )
                    for item in item_data["items"]
                ]
                entity.is_closed = item_data["is_closed"]

            entity.id = item_data["id"]
            self._entities_by_id[entity.id] = entity

        if self._entities_by_id:
            self._next_id = max(self._entities_by_id) + 1

    def _entity_to_dict(self, entity):
        if isinstance(entity, Dish):
            return {
                "id": entity.id,
                "name": entity.name,
                "price": entity.price,
            }

        return {
            "id": entity.id,
            "table_number": entity.table_number,
            "is_closed": entity.is_closed,
            "items": [
                {
                    "dish_name": item.dish_name,
                    "price": item.price,
                    "quantity": item.quantity,
                }
                for item in entity.items
            ],
        }

    def _save(self):
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [
            self._entity_to_dict(entity)
            for entity in self._entities_by_id.values()
        ]
        json_text = json.dumps(data, ensure_ascii=False, indent=2)
        self._file_path.write_text(json_text + "\n", encoding="utf-8")

    def add(self, entity):
        if entity.id is not None:
            raise ValueError("объект уже сохранён")

        entity.id = self._next_id
        self._entities_by_id[entity.id] = entity
        self._next_id += 1
        self._save()
        return entity

    def get(self, entity_id):
        if entity_id not in self._entities_by_id:
            raise ValueError(f"объект с ID {entity_id} не найден")
        return self._entities_by_id[entity_id]

    def get_all(self):
        return list(self._entities_by_id.values())

    def update(self, entity):
        self.get(entity.id)
        self._entities_by_id[entity.id] = entity
        self._save()
        return entity

    def delete(self, entity_id):
        self.get(entity_id)
        del self._entities_by_id[entity_id]
        self._save()