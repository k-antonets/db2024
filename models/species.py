import sqlite3
from .taxon import Taxon

class Species(Taxon):
    def __init__(self, speciesName='', genusName='', description=''):
        super().__init__(speciesName, 'species', description)
        self.__genus = Taxon(genusName, 'genus', '')

    @property
    def fullName(self):
        return f'{self.__genus.name} {self.name}'

    @property
    def speciesName(self):
        return self.name

    @speciesName.setter
    def speciesName(self, name):
        self.name = name

    @property
    def genusName(self):
        return self.__genus.name

    @genusName.setter
    def genusName(self, name):
        self.__genus.name = name

    @property
    def genus(self):
        return self.__genus


    @classmethod
    def getById(cls, _db, id: int):
        t = super(Species, cls).getById(_db, id)
        t.__setGenus(_db)
        return t

    def __setGenus(self, _db):
        if self._parentId > -1 and self.__genus.id < 0:
            self.__genus = Taxon.getById(_db, self._parentId)

    def __str__(self):
        return self.fullName

    def save(self, _db):
        self.__genus.save(_db)
        self._parentId = self.__genus.id
        super().save(_db)

    @classmethod
    def getList(cls, _db):
        lst = cls.getListByRank(_db, 'species')
        return lst
