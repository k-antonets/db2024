import sqlite3

class Taxon:
    __con = None
    __cur = None
    __table = "Taxonomy"

    def __init__(self, name='', rank='', description=''):
        self.name, self.rank, self.description = name, rank, description
        self.__parentId = -1
        self.__id = -1
        self.__changed = False
        self.__saved = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__changed = True
        self.__name = name

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, rank):
        self.__changed = True
        self.__rank = rank

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__changed = True
        self.__description = description

    @property
    def id(self):
        return self.__id

    @property
    def hasParent(self):
        return self.__parentId > -1

    @classmethod
    def bindDb(cls, con: sqlite3.Connection):
        cls.__db = con
        cls.__cur = con.cursor()

    @classmethod
    def getById(cls, id: int):
        txn = cls.__cur.execute(f'select tax_name, rank, description, parent_id from {cls.__table} where id = ?;', (id, ))
        txnTuple = txn.fetchone()
        t = cls(*txnTuple[0:3])
        t.__id = id
        t.__parentId = txnTuple[3]
        t.__saved = True
        return t

    def getParent(self):
        if self.hasParent:
            return type(self).getById(self.__parentId)
        else:
            return None

    def save(self):
        if self.__saved and not self.__changed:
            return
        if not self.__saved:
            type(self).__cur.execute(f'insert into {type(self).__table}(tax_name, rank, description, parent_id) values (?, ?, ?, ?);',
                                     (self.name, self.rank, self.description, self.__parentId))
        else:
            type(self).__cur.execute(f'update {type(self).__table} set tax_name = ?, rank = ?, description = ?, parent_id = ? where id = ?;',
                                     (self.name, self.rank, self.description, self.__parentId, self.__id))
        type(self).__con.commit()
        self.__saved = True
        self.__changed = False

    def __str__(self):
        return f"{self.rank} {self.name}"
