import stripe
from django.conf import settings

# Инициализируем клиента Stripe секретным ключом
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Шаг 1: Создание продукта в Stripe."""
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(amount, product_id):
    """Шаг 2: Создание цены в Stripe (сумма переводится в копейки)."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),  # Переводим рубли в копейки
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id):
    """Шаг 3: Создание сессии оплаты для получения ссылки."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url


def retrieve_stripe_session(session_id):
    """Дополнительное задание: Получение данных о сессии Stripe по её ID."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session.payment_status
