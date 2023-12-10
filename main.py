from hub import Hub
from item import Item
from test import create_item
import random

hub = Hub()
hub.clear()

for i in range(30):
    hub.add_item(Item(
        f'{''.join(random.choices([chr(i) for i in range(97, 123)], k=5))}',
        'description',
        f'{str(i + 1).zfill(2)}.12.2023',
        i + 1 * 5,
        'tag'))

a = []
for item in hub:
    if item.get_name().lower().startswith('a'):
        a.append(item)
        hub.rm_item(item)

outdated = []
for item in hub:
    if item.get_date() < hub.date:
        outdated.append(item)
        hub.rm_item(item)

most_valuable = hub.find_most_valuable(10)
for item in most_valuable:
    hub.rm_item(item)

others = hub.get_items()

print(a)
print('*' * 20)
print(outdated)
print('*' * 20)
print(most_valuable)
print('*' * 20)
print(others)

a = next(create_item())
h = Hub()
h.save_as_json()
a.save_as_json()


print(hash(a))
