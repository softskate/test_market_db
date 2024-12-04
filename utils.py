from models import Category, Product, ProductGroup, PricingRule


def get_products_by_category(category_id):
    subcategories = (Category
                     .select(Category.id)
                     .where((Category.id == category_id) |
                            (Category.parent == category_id)))
    products = Product.select().where(Product.category.in_(subcategories))
    return products


def calculate_group_price(group_id):
    # Получаем товары, входящие в группу
    group_items = (Product
                   .select()
                   .join(ProductGroup, on=ProductGroup.product)
                   .where(ProductGroup.group == group_id))
    
    pricing_rule = PricingRule.get_or_none(PricingRule.group == group_id)
    
    total_price = sum(item.price for item in group_items)  # Используем item.price
    
    if pricing_rule:
        # Применяем скидку
        if pricing_rule.discount:
            total_price *= (1 - pricing_rule.discount / 100)
        
        # Бесплатные товары
        if pricing_rule.free_every_n:
            sorted_items = sorted(group_items, key=lambda x: x.price)
            free_items = len(sorted_items) // pricing_rule.free_every_n
            total_price -= sum(item.price for item in sorted_items[:free_items])
    
    return total_price
