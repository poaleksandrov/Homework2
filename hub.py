import datetime
import re
from item import Item
import json


class Hub:
    _items = []
    _hub = None

    def __new__(cls, *args, **kwargs):
        if cls._hub is None:
            cls._hub = object.__new__(cls)

        return cls._hub

    def __init__(self, date=datetime.datetime.now().date()):
        self._date = date

    def __getitem__(self, item):
        return self._items[item]

    def __repr__(self):
        return ', '.join([i.get_name() for i in self._items])

    def __str__(self):
        return f'Хаб содержит {len(self._items)} позиции: {", ".join(sorted([i.get_name() for i in self._items]))}'

    def __len__(self):
        return len(self._items)

    def add_item(self, item):
        """Adds Item in Hub"""
        if isinstance(item, Item) or issubclass(type(item), Item):
            self._items.append(item)
        else:
            raise AttributeError('Item must be class Item or its subclass')

    def get_items(self):
        """Returns list of existed Items in Hub """
        return self._items

    def find_by_id(self, item_id):
        """Returns list of Item indexes and names"""
        for index, item in enumerate(self._items):
            if item.get_id() == item_id:
                return [index, item.get_name()]
        return [-1, None]

    def find_by_tags(self, tags):
        """Returns list of Items which contains all tags in getting argument"""
        items = []
        for item in self._items:
            if len(item.get_tags()) > len(tags):
                continue

            for tag in item.get_tags():
                if tag not in tags:
                    break
            else:
                items.append(item)

        return items

    def rm_item(self, i):
        """Removes Item from Hub"""
        for item in enumerate(self._items):
            if item[1].get_id() == i or item[1] is i:
                del self._items[item[0]]
                break

    def drop_items(self, items):
        """Removes all Items which includes in argument"""
        for item in items:
            if item in self._items:
                self._hub.rm_item(item)

    def clear(self):
        """Drops all Items from Hub"""
        self._items = []

    @property
    def date(self):
        """Returns Hub date"""
        return self._date

    @date.setter
    def date(self, new_date):
        """Sets Hub date"""
        if re.fullmatch('[0-9]{2}.[0-9]{2}.[0-9]{4}', new_date):
            day, month, year = map(int, new_date.split('.'))
            self._date = datetime.date(year, month, day)
        else:
            raise AttributeError('Date must be in format "DD.MM.YYYY"')

    def find_by_date(self, *dates):
        """If there is only one argument then method returns Items where dispatch time is less than argument.
        If there are two arguments the method returns Items where dispatch time is between first and second arguments"""
        if len(dates) not in (1, 2):
            raise AttributeError('Method gets 1 or 2 arguments: max date or min and max dates')

        datetimes = []
        items = []

        for i in dates:
            if re.fullmatch('[0-9]{2}.[0-9]{2}.[0-9]{4}', i):
                day, month, year = map(int, i.split('.'))
                datetimes.append(datetime.date(year, month, day))
            else:
                raise AttributeError('Date must be in format "DD.MM.YYYY"')

        if len(datetimes) == 1:
            for item in self._items:
                if item.get_date() <= datetimes[0]:
                    items.append(item)
        else:
            for item in self._items:
                if min(datetimes) <= item.get_date() <= max(datetimes):
                    items.append(item)

        return items

    def find_most_valuable(self, amount=1):
        """Returns the most valuable items in Hub.
        If there are more items satisfying the condition then all of them will be returned.
        For example, amount = 1; there are 3 items in Hub with the highest price (5000). 3 items will be returned"""
        if len(self._items) == 0:
            raise ValueError("Hub doesn't contain any Items")

        if len(self._items) <= amount:
            return sorted(self._items, key=lambda x: x.cost)

        most_valuable = []
        prices = sorted(list(set([i.cost for i in self._items])), reverse=True)[:amount]
        for item in self._items:
            if item.cost in prices:
                most_valuable.append(item)

        return sorted(most_valuable, key=lambda x: x.cost)

    def save_as_json(self):
        """Creates JSON file with Hub's data"""
        to_json = {
            "date": self.date.strftime('%d.%m.%Y'),
            "items": [
                {
                    "name": item.get_name(),
                    "id": item.get_id(),
                    "description": item.get_descr(),
                    "cost": item.cost,
                    "dispatch_time": item.get_date(),
                    "tags": [
                        tag for tag in item.get_tags()
                    ]} for item in self.get_items()
            ]
        }

        with open(f'hubs/hub_{self.date}.json', 'w') as f:
            f.write(json.dumps(to_json))

    @staticmethod
    def read_from_json(file):
        """Creates Hub from JSON file"""
        with open(file, 'r') as f:
            json_string = json.loads(f.read())
        h = Hub(json_string['date'])
        for item in json_string['items']:
            h.add_item(Item(
                item['name'],
                item['description'],
                item['dispatch_time'],
                item['cost'],
                *item['tags']
            ))
        return h
