from pymongo import Connection, ASCENDING

class Db(object):
    DATABASE = 'openboe'

    def __init__(self, db_name=DATABASE):
        conn = Connection()
        self.db = conn[db_name]

    def get_col(self, col):
        return self.db[col].find()

    def has(self, col, query_dict, sort_field=None,
            direction=ASCENDING):
        objects = self.db[col].find(query_dict)
        if sort_field is not None:
            objects.sort(sort_field)

        return list(objects)

    def find_one(self, col, query_dict):
        return self.db[col].find_one(query_dict)

    def insert(self, col, element):
        self.db[col].insert(element)
