import datetime
import unittest
import random
from item import Item
from hub import Hub


def create_item():
    """Return random Item"""

    while True:
        item = Item(
            f'{''.join(random.choices([chr(i) for i in range(97, 123)], k=5))}',
            'description',
            datetime.date.today().strftime('%d.%m.%Y'),
            random.randrange(1000, 10000),
            '')

        yield item


class TestHub(unittest.TestCase):
    def test_hub_singleton(self):
        """Проверка того что hub - синглтон"""
        self.assertTrue(Hub() is Hub())

    def test_len(self):
        """Проверка того что при добавлении предметов меняется значение len()"""
        h = Hub()
        h.clear()
        for i in range(5):
            h.add_item(Item(f'name_{i + 1}', f'description_{i + 1}', f'1{i}.11.2023', 100, 'tag1'))

        self.assertEqual(len(h), 5)

    def test_rm_item(self):
        h = Hub()
        h.clear()

        for i in range(5):
            h.add_item(Item(f'name_{i + 1}', f'description_{i + 1}', f'1{i}.11.2023', 100, 'tag1'))

        last_id = h.find_by_tags('tag1')[0].get_id()

        h.rm_item(last_id)
        self.assertEqual(len(h), 4)

        item = Item(f'name_test', f'description_test', f'13.11.2023', 100, 'tag1')
        h.add_item(item)
        h.rm_item(item)
        self.assertEqual(len(h), 4)

    def test_drop_items(self):
        h = Hub()
        h.clear()

        items = []

        for i in range(5):
            item = Item(f'name_{i + 1}', f'description_{i + 1}', f'1{i}.11.2023', 100, 'tag1')
            h.add_item(item)
            items.append(item)

        h.drop_items(items[:3])

        self.assertEqual(len(h), 2)

    def test_clear(self):
        h = Hub()
        h.clear()

        for i in range(5):
            h.add_item(Item(f'name_{i + 1}', f'description_{i + 1}', f'1{i}.11.2023', 100, 'tag1'))

        self.assertEqual(len(h), 5)

        h.clear()
        self.assertEqual(len(h), 0)

    def test_date(self):
        h = Hub()
        h.clear()

        h.date = '09.12.2023'

        self.assertEqual(h.date, datetime.date(2023, 12, 9))

    def test_find_by_date(self):
        h = Hub()
        h.clear()

        items = []
        for i in range(5):
            item = Item(f'name_{i + 1}', f'description_{i + 1}', f'1{i}.11.2023', 100, 'tag1')
            h.add_item(item)
            items.append(item)

        self.assertEqual(len(h.find_by_date('10.11.2023', '12.11.2023')), 3)
        self.assertEqual(len(h.find_by_date('13.11.2023')), 4)
        with self.assertRaises(AttributeError):
            h.find_by_date('10.11.23')
            h.find_by_date('11.23.23')

    def test_add_item(self):
        h = Hub()
        h.clear()

        with self.assertRaises(AttributeError):
            h.add_item(2)
            h.add_item('Item')

    def test_most_valuables(self):
        h = Hub()
        h.clear()

        for i in range(5):
            item = Item(f'name_{i + 1}', f'description_{i + 1}', f'1{i}.11.2023', (i + 1) * 1000, 'tag1')
            h.add_item(item)

        self.assertEqual(len(h.find_most_valuable()), 1)
        self.assertEqual(len(h.find_most_valuable(2)), 2)
        self.assertEqual(h.find_most_valuable()[0].cost, 5000)

        for i in range(5):
            h.add_item(Item(f'name_{i + 6}', f'description', f'1{i}.11.2023', 7000, 'tag1'))

        self.assertEqual(len(h.find_most_valuable()), 5)


class TestItem(unittest.TestCase):
    def test_item_id(self):
        """Проверка того что у разных Items разные id"""
        for _ in range(10):
            self.assertNotEqual(Item('name', 'description', '06.12.2023', 100, 'tag').get_id(),
                                Item('name', 'description', '06.12.2023', 100, 'tag').get_id())

    def test_len(self):
        """Проверка того что при добавлении тэгов меняется значение len(item)"""
        item = Item('name', 'description', '29.11.2023', 100, 'tag1', 'tag2')
        start_len = len(item)
        item.add_tag('tag3')
        item.add_tag('tag4')

        self.assertNotEqual(len(item), start_len)

    def test_equal_tags(self):
        test_item = Item('item', 'item description', '06.12.2023', 100, '')
        for i in range(10):
            if i % 2:
                test_item.add_tag(f'tag_{i}')
                test_item.add_tag(f'tag_{i}')
            else:
                test_item.add_tag(f'tag_{i}')
        self.assertEqual(len(test_item.get_tags()), len(set(test_item.get_tags())))

    def test_find_by_id(self):
        current_id = Item('item', 'item description', '06.12.2023', 100, '').get_id()
        hub = Hub()
        for _ in range(5):
            hub.add_item(Item('item', 'item description', '06.12.2023', 100, ''))

        self.assertNotEqual(hub.find_by_id(current_id + 1), [-1, None])
        self.assertNotEqual(hub.find_by_id(current_id + 2), [-1, None])
        self.assertNotEqual(hub.find_by_id(current_id + 3), [-1, None])
        self.assertEqual(hub.find_by_id(current_id + 7), [-1, None])
        self.assertEqual(hub.find_by_id(current_id + 8), [-1, None])

    def test_find_by_tags(self):
        hub = Hub()
        hub.add_item(
            Item('item_true', 'item description', '06.12.2023', 100,
                 'test_tag_1', 'test_tag_2', 'test_tag_3', 'test_tag_4', 'test_tag_5', 'test_tag_6'))

        self.assertEqual(
            hub.find_by_tags(['test_tag_1', 'test_tag_2', 'test_tag_3', 'test_tag_4', 'test_tag_5',
                              'test_tag_6'])[0].get_name(), 'item_true')
        self.assertNotEqual(
            hub.find_by_tags(['test_tag_2', 'test_tag_3', 'test_tag_4', 'test_tag_5', 'test_tag_6']),
            'item_true')

    def test_multiply_adding_tags(self):
        item = Item('name', 'description', '06.12.2023', 100, 'test_tag_1')

        item.add_tags([f'test_tag_{i + 1}' for i in range(5)])
        self.assertEqual(len(item.get_tags()), 5)

    def test_multiply_removing_tags(self):
        item = Item('name', 'description', '06.12.2023', 100, 'tag_1')

        item.add_tags([f'tag_{i + 1}' for i in range(5)])
        item.rm_tags(['tag_1', 'tag_2'])
        self.assertEqual(len(item.get_tags()), 3)

        item.rm_tags(['tag_10'])
        self.assertEqual(len(item.get_tags()), 3)

    def test_is_tagged(self):
        item = Item('name', 'description', '06.12.2023', 100, 'tag_1')

        item.add_tags([f'tag_{i + 1}' for i in range(5)])
        self.assertTrue(item.is_tagged('tag_1'))
        self.assertFalse(item.is_tagged('tag_10'))

    def test_copy(self):
        item = Item('name', 'description', '06.12.2023', 100, 'test_tag_1')
        item_copy = item.copy()

        self.assertFalse(item is item_copy)
        self.assertEqual(item.cost, item_copy.cost)
        self.assertEqual(item.get_descr(), item_copy.get_descr())
        self.assertEqual(item.get_name(), item_copy.get_name())
        self.assertNotEqual(item.get_id(), item_copy.get_id())

    def test_comparing(self):
        item_cheap = Item('name', 'description', '06.12.2023', 100, 'test_tag_1')
        item_expensive = Item('name', 'description', '06.12.2023', 5000, 'test_tag_1')
        self.assertTrue(item_cheap < item_expensive)
        self.assertTrue(item_expensive > item_cheap)
        self.assertFalse(item_cheap > item_expensive)
        self.assertFalse(item_expensive < item_cheap)

    def test_cost(self):
        item = Item('name', 'description', '06.12.2023', 5000, 'test_tag_1')
        item.cost = 10000
        self.assertEqual(item.cost, 10000)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
