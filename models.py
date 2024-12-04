from peewee import *


# База данных
db = SqliteDatabase('online_shop.db')


class BaseModel(Model):
    class Meta:
        database = db


# Модель категории
class Category(BaseModel):
    id = AutoField()
    name = CharField()
    parent = ForeignKeyField('self', null=True, backref='subcategories')
    

# Модель товара
class Product(BaseModel):
    id = AutoField()
    name = CharField()
    price = FloatField(null=True)
    type = CharField(choices=[('SIMPLE', 'Simple'), ('GROUP', 'Group')])
    category = ForeignKeyField(Category, backref='products')
    

# Модель группы товаров
class ProductGroup(BaseModel):
    group = ForeignKeyField(Product, backref='group_items')
    product = ForeignKeyField(Product, backref='groups')


# Модель правил ценообразования
class PricingRule(BaseModel):
    group = ForeignKeyField(Product, backref='pricing_rules')
    discount = FloatField(null=True)  # Скидка в %
    free_every_n = IntegerField(null=True)  # Каждый N-й товар бесплатно


if not db.table_exists(Product):
    db.create_tables(BaseModel.__subclasses__())
