import sqlite3

class Taxon:
    _table = "Taxonomy"

    def __init__(self, name='', rank='', description=''):
        self.name, self.rank, self.description = name, rank, description
        self._parentId = -1
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
        return self._parentId > -1

    @classmethod
    def getById(cls, _db: sqlite3.Connection, id: int):
        _cur = _db.cursor()
        txn = _cur.execute(f'select tax_name, rank, description, parent_id from {cls._table} where id = ?;', (id, ))
        txnTuple = txn.fetchone()
        t = cls(*txnTuple[0:3])
        t.__id = id
        t._parentId = txnTuple[3]
        t.__saved = True
        return t

    def getParent(self, db):
        if self.hasParent:
            return type(self).getById(db, self._parentId)
        else:
            return None

    def save(self, _db):
        if self.__saved and not self.__changed:
            return
        _cur = _db.cursor()
        if not self.__saved:
            _cur.execute(f'insert into {type(self)._table}(tax_name, rank, description, parent_id) values (?, ?, ?, ?);',
                                    (self.name, self.rank, self.description, self._parentId))
        else:
            _cur.execute(f'update {type(self)._table} set tax_name = ?, rank = ?, description = ?, parent_id = ? where id = ?;',
                                    (self.name, self.rank, self.description, self._parentId, self.__id))
        _db.commit()
        self.__saved = True
        self.__changed = False

    @classmethod
    def getListByRank(cls, _db, rank):
        cur = _db.cursor()
        txn = cur.execute(f'select id from {cls._table} where rank = ?;', (rank,))
        ts = txn.fetchall()
        return [cls.getById(_db, id[0]) for id in ts]

    def __str__(self):
        return f"{self.rank} {self.name}"
