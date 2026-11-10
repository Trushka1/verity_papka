from abc import ABC, abstractmethod


# общий набор операций для любого способа хранения данных
class Repository(ABC):
    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass


# каждый экземпляр хранит данные в своём словаре
class MemoryRepository(Repository):
    def __init__(self):
        self._entities_by_id = {}
        self._next_id = 1

    def add(self, entity):
        if entity.id is not None:
            raise ValueError("объект уже сохранён")
        # выдаём новый ID и сохраняем объект под этим номером
        entity.id = self._next_id
        self._entities_by_id[entity.id] = entity
        self._next_id += 1
        return entity

    def get(self, entity_id):
        if entity_id not in self._entities_by_id:
            raise ValueError(f"объект с ID {entity_id} не найден")
        return self._entities_by_id[entity_id]

    def get_all(self):
        return list(self._entities_by_id.values())

    def update(self, entity):
        # проверяем, что объект уже есть в хранилище
        self.get(entity.id)
        self._entities_by_id[entity.id] = entity
        return entity

    def delete(self, entity_id):
        self.get(entity_id)
        del self._entities_by_id[entity_id]
