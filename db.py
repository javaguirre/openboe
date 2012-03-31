from pymongo import Connection

class Db(object):

    def __init__(self, db_name='openboe'):
        conn = Connection()
        self.db = conn[db_name]

    def get_cols(self, col):
        return self.db[col].find()

    def has(self, col, query_dict):
        return list(self.db[col].find(query_dict))

    def insert(self, col, element):
        self.db[col].insert(element)
