from datetime import datetime
import json
import os
from os import chdir, getcwd


class User(object):
    def __init__(self, name):
        self.__isadmin = False
        self.name = name
        self.tariff = 1

    def save(self):
        home = getcwd()
        chdir('./users')

        with open(f'{self.id}.json', 'w', encoding='utf-8') as f:
            data = self.__dict__
            data.pop('id')
            json.dump(data, f, ensure_ascii=False, indent=4)

        chdir(home)

