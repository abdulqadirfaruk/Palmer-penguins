from pymongo import MongoClient


class Connect(object):
    @staticmethod
    def get_connection():
        return MongoClient('mongodb+srv://app:HcVqRjIRB021C4dx@cluster0.3zldi.mongodb.net/penguins?retryWrites=true&w=majority')
