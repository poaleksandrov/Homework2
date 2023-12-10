import itertools
import re
import datetime
import json


class Item:
    _ids = itertools.count(1)  # Создаем генератор для генерации уникальных id

    def __init__(self, name, description, dispatch_time, cost=0, *tags):
        self._tags = []
        self._id = next(self._ids)
        self._name = name
        self._description = description
        self._dispatch_time = dispatch_time
        self._cost = cost

        if re.fullmatch('[0-9]{2}.[0-9]{2}.[0-9]{4}', dispatch_time):
            day, month, year = map(int, dispatch_time.split('.'))
            self._dispatch_time = datetime.date(year, month, day)
        else:
            raise AttributeError('Date must be in format "DD.MM.YYYY"')

        for tag in tags:
            self._tags.append(tag)

    def __repr__(self):
        tags_qty = 3 if len(self._tags) >= 3 else len(self._tags)
        return '-'.join([str(self._id), ','.join(self._tags[:tags_qty])])

    def __str__(self):
        return f'Позиции "{self._name}" присвоены следующие теги (характеристики): {", ".join(self._tags)}'

    def __len__(self):
        return len(self._tags)

    def __lt__(self, other):
        if not isinstance(other, Item):
            raise TypeError('Both of elements must be Item')

        return self.cost < other.cost

    def __hash__(self):
        return int(str(self._id) + self._dispatch_time.strftime('%d%m%Y'))

    def add_tag(self, tag):
        """Adds one tag in Item"""
        if tag in self._tags:
            return 'Tag already exists'
        self._tags.append(tag)

    def add_tags(self, tags):
        """Adds few tags in Item"""
        for tag in tags:
            if tag in self._tags:
                continue
            self._tags.append(tag)

    def rm_tag(self, tag):
        """Removes one tag from Item"""
        self._tags.remove(tag)

    def rm_tags(self, tags):
        """Removes few tags from Item"""
        for tag in tags:
            if tag in self._tags:
                self._tags.remove(tag)

    def get_id(self):
        """Returns Item's id"""
        return self._id

    def get_tags(self):
        """Returns list of Item's tags"""
        return self._tags

    def is_tagged(self, tags):
        """Checks if Item contains tag if there is only one tag in argument
        or all tags from argument are contained in Item if there is container of tags in argument"""
        if isinstance(tags, str):
            if tags in self._tags:
                return True
        else:
            if set(tags).issubset(set(self._tags)):
                return True

        return False

    def get_name(self):
        """Returns Item's name"""
        return self._name

    def get_descr(self):
        """Returns Item's description"""
        return self._description

    @property
    def cost(self):
        """Returns Item's cost"""
        return self._cost

    @cost.setter
    def cost(self, value):
        """Sets Item's cost"""
        if value <= 0:
            raise ValueError("Cost must be more than 0")
        self._cost = value

    def copy(self):
        """Returns copy of object with new id"""
        return Item(self._name, self._description, self._dispatch_time.strftime('%d.%m.%Y'), self._cost, *self._tags)

    def get_date(self):
        """Returns Item's date"""
        return self._dispatch_time

    def save_as_json(self):
        """Creates JSON file with Item's data"""
        to_json = {
            "name": self.get_name(),
            "id": self.get_id(),
            "description": self.get_descr(),
            "cost": self.cost,
            "dispatch_time": self.get_date().strftime('%d.%m.%Y'),
            "tags": [
                tag for tag in self.get_tags()
            ]
        }

        with open(f'items/item_{self.get_name()}.json', 'w') as f:
            f.write(json.dumps(to_json))

    @staticmethod
    def create_from_json(file):
        """Creates Item from JSON file"""
        with open(file, 'r') as f:
            json_string = json.loads(f.read())
        return Item(
            json_string['name'],
            json_string['description'],
            json_string['dispatch_time'],
            json_string['cost'],
            *json_string['tags']
        )
