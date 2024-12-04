from models import Category, Product, ProductGroup, PricingRule
from utils import get_products_by_category, calculate_group_price

# Категории
electronics = Category.create(name='Electronics')
phones = Category.create(name='Phones', parent=electronics)

# Товары
iphone = Product.create(name='iPhone', price=999.99, type='SIMPLE', category=phones)
samsung = Product.create(name='Samsung Galaxy', price=799.99, type='SIMPLE', category=phones)

# Группа товаров
phone_bundle = Product.create(name='Phone Bundle', type='GROUP', category=electronics)
ProductGroup.create(group=phone_bundle, product=iphone)
ProductGroup.create(group=phone_bundle, product=samsung)

# Правила
PricingRule.create(group=phone_bundle, discount=10, free_every_n=2)

# Получить все товары в категории Electronics
products = get_products_by_category(electronics.id)
for product in products:
    print(product.name, product.price)

# Рассчитать цену группы
bundle_price = calculate_group_price(phone_bundle.id)
print(f"Цена набора: {bundle_price}")
