import datetime
from collections import OrderedDict
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    '''Create' the database and the table if they don't exist'''
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def menu_loop():
    '''Show the menu'''
    choice = None

    while choice != 'q':
        clear()
        print('Enter "Q" to quit')
        for key, value in menu.items():
            print(f'{key}) {value.__doc__}')
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()



def add_entry():
    '''Add an entry'''
    data_1 = []
    print('Enter your entry, enter "done" when finished')

    while True:
        data = input()
        if data.lower() != 'done':
            data_1.append(data)
        else:
            break
    data = '\n'.join(data_1)
    if input('Save entry? [Y/n] ').lower() != 'n':
        Entry.create(content=data)
        print('Saved successfuly')


def view_entry(search_query=None):
    '''View previous entries'''
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        clear()
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M:%p')
        print(timestamp)
        print('=' * len(timestamp))
        print(entry.content)
        print('\n\n'+'='*len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Nq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    '''Search entries for a string'''
    view_entry(input('Search query: '))


def delete_entry(entry):
    '''Delete an entry'''
    if input('Are you sure? [y/N] ').lower() == 'y':
        entry.delete_instance()
        print('Entry deleted')

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entry),
    ('s', search_entries),
])

if __name__ == '__main__':
    initialize()
    menu_loop()