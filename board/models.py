# coding: utf-8
from board import db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = db.Model
metadata = Base.metadata


class Counter(Base):
    __tablename__ = 'counters'

    id_counters = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(45))
    type = Column(Integer)
    address = Column(String(45), nullable=False)
    flat = Column(Integer)

    def __str__(self):
        return '{name} {type}'.format(name=self.name, type=self.type)


class CountersParametr(Base):
    __tablename__ = 'counters_parametrs'

    id_counters_parametrs = Column(Integer, primary_key=True)
    id_counters = Column(ForeignKey('counters.id_counters'), index=True)
    id_parametrs = Column(ForeignKey('parametrs.id_parametrs'), index=True)

    counter = relationship('Counter', lazy='joined')
    parametr = relationship('Parametr', lazy='joined')

    def __str__(self):
        return '{counter} {parametr}'.format(counter=self.counter.name, parametr=self.parametr.name)


class History(Base):
    __tablename__ = 'history'

    id_history = Column(Integer, primary_key=True)
    id_counters_parametrs = Column(ForeignKey('counters_parametrs.id_counters_parametrs'), index=True)
    time = Column(DateTime)
    values = Column(Numeric)

    counters_parametr = relationship('CountersParametr')

    def __str__(self):
        return '{counter} {parametr} {time} {val}'.format(
            counter=self.counters_parametr.counter.name,
            parametr=self.counters_parametr.parametr.name,
            time=self.time,
            val=self.values
        )



class Parametr(Base):
    __tablename__ = 'parametrs'

    id_parametrs = Column(Integer, primary_key=True)
    name = Column(String(45))
    unit = Column(String(45))

    def __str__(self):
        return self.name


class Val(Base):
    __tablename__ = 'val'

    id_values = Column(Integer, primary_key=True)
    id_counters_parametrs = Column(ForeignKey('counters_parametrs.id_counters_parametrs'), index=True)
    time = Column(DateTime)
    value = Column(Numeric(5, 3))

    counters_parametr = relationship('CountersParametr')

    def __str__(self):
        return '{counter} {parametr} {time} {val}'.format(
            counter=self.counters_parametr.counter.name,
            parametr=self.counters_parametr.parametr.name,
            time=self.time,
            val=self.values
        )
