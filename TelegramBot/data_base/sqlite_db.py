import json

from aiogram import types
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE = "sqlite:///../menu.db"

Base = declarative_base()


# Default data base part
class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class IceCoffee(Base):
    __tablename__ = 'ice coffee'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class Other(Base):
    __tablename__ = 'other'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class Sweets(Base):
    __tablename__ = 'sweets'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return f'ID: {self.id}\nFull name:{self.name}\nPrice: {self.price}\n'


class SuccessfulPurchase(Base):
    __tablename__ = 'successful_purchases'
    id = Column(Integer, primary_key=True)
    user_profile_url = Column(String(128), nullable=False)
    user_name = Column(String(50), nullable=False)
    order = Column(String(128), nullable=False)
    total_amount = Column(Integer, nullable=False)
    date = Column(String(30), nullable=False)


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    last_login = Column(String, nullable=False)
    super_admin = Column(Boolean, default=False)


class DataBase:
    table_classes = (Coffee, IceCoffee, Other, Sweets)
    table_names = ('coffee', 'ice coffee', 'other', 'sweets')

    def __init__(self):
        engine = create_engine(DATABASE, echo=False)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    def sql_start(self):
        if self.session:
            print('DB Connected True')

    def sql_end(self):
        if self.session:
            self.session.commit()
            self.session.close()
            print('DB Connected False')

    def find_table_class(self, table_name):
        for table_class in self.table_classes:
            if table_class.__tablename__ == table_name:
                return table_class
        return None

    # ------------------------------ Web App Common User part ----------------------------------------------------------

    def get_data_for_menu(self, table_name):
        table = self.find_table_class(table_name)
        result = self.session.query(table).order_by('price').all()
        return result

    # ------------------------------ Static methods -------------------------------------------------------------------

    @staticmethod
    def web_data_formater(web_data):
        data = json.loads(web_data)
        return sorted(data)

    @staticmethod
    def items_count_remover(item, items):
        while item in items:
            items.remove(item)
        return items

    # ------------------------------ Telegram bot part ------------------------------
    def get_data_from_web_data(self, web_data):
        result = []
        web_data = self.web_data_formater(web_data)
        for item in web_data:
            table_name = item.split("_")
            table_class = self.find_table_class(table_name[0])
            data = self.session.query(table_class).filter_by(id=item).with_entities(table_class.name,
                                                                                    table_class.price).all()
            result.extend(data)
        return result

    def set_prices_for_payment(self, web_data):
        price = []
        products = ''
        data = self.get_data_from_web_data(web_data)
        unique_items = list(set(data))  # Створюємо список унікальних елементів
        for item in unique_items:
            count = data.count(item)
            product = f'{item[0]} x {count}\n'
            price.append(
                types.LabeledPrice(label=product, amount=item[1] * count * 100)
            )
            products += product

        return price, products

    def succesful_sales(self, user_profile_url, user_name, order, total_amount, date):
        self.session.add(SuccessfulPurchase(user_profile_url=user_profile_url,
                                            user_name=user_name,
                                            order=order,
                                            total_amount=total_amount,
                                            date=date))
        self.session.commit()
        print("Data about sale has been added")


db = DataBase()
