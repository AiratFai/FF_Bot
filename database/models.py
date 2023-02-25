from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class ExpenseCategories(Base):
    __tablename__ = 'expense_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(30), nullable=False)
    children = relationship('MainTable', backref='parent1')

    def __repr__(self):
        return self.category_name


class IncomeCategories(Base):
    __tablename__ = 'income_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(30), nullable=False)
    children = relationship('MainTable', backref='parent2')

    def __repr__(self):
        return self.category_name


class MainTable(Base):
    __tablename__ = 'main_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    expense_cat_id = Column(Integer, ForeignKey('expense_categories.id'), nullable=True, default=None)
    income_cat_id = Column(Integer, ForeignKey('income_categories.id'), nullable=True, default=None)
    name = Column(String(60), nullable=False)
    date = Column(DateTime, default=datetime.now)
    income = Column(Integer, default=0)
    expense = Column(Integer, default=0)
    balance = Column(Integer, default=0)

    def __repr__(self):
        return self.name


