from keyboards.builders import MenuItem, MenuBuilder


def main_menu_keyboard():
    items = [
        MenuItem(
            text="🛍️ Каталог",
            callback_data="show_catalog"
        ),
        MenuItem(
            text="🛒 Для замовлення",
            web_app_url="https://barskyi.github.io/for_order.html"
        ),
        MenuItem(
            text="ℹ️ Контакти",
            web_app_url="https://barskyi.github.io/contact_info.html"
        ),
        MenuItem(
            text="❓ FAQ",
            callback_data="faq"
        ),
        MenuItem(
            text="🔗 Поділитися",
            switch_inline_query="Магазин BarBags: стильні сумки та аксесуари! 👜"
        )
    ]
    return MenuBuilder(items).build()


def catalog_keyboard():
    catalog_items = [
        ("💼️ Шкіряні чоловічі сумки", "https://t.me/c/2403545636/10"),
        ("📨 Текстильні сумки", "https://t.me/c/2403545636/29"),
        ("🧳 Дорожні сумки", "https://t.me/c/2403545636/28"),
        ("🎒 Рюкзаки", "https://t.me/c/2403545636/32"),
        ("🏃 Бананки/сумки-слінг", "https://t.me/c/2403545636/33"),
        ("💳 Гаманці", "show_wallets")
    ]

    items = [MenuItem(text=text, url=url if not url == "show_wallets" else None,
                      callback_data=url if url == "show_wallets" else None)
             for text, url in catalog_items]
    items.extend([
        MenuItem(text="➖➖➖➖➖➖➖➖➖➖➖➖", callback_data="separator"),
        MenuItem(text="🔙 Назад", callback_data="main_menu")
    ])

    return MenuBuilder(items).build()


def wallets_keyboard():
    wallet_items = [
        ("👨 Для нього", "https://t.me/c/2403545636/79"),
        ("👩 Для неї", "https://t.me/c/2403545636/34"),
        ("➖➖➖➖➖➖➖➖➖➖➖➖", "separator"),
        ("🔙 Назад", "show_catalog")
    ]

    items = [MenuItem(text=text,
                      url=url if not url in ["separator", "show_catalog"] else None,
                      callback_data=url if url in ["separator", "show_catalog"] else None)
             for text, url in wallet_items]

    return MenuBuilder(items).build()


def faq_keyboard():
    items = [
        MenuItem(text="📦 Доставка", callback_data="delivery_info"),
        MenuItem(text="💰 Оплата", callback_data="payment_info"),
        MenuItem(text="🔄 Повернення", callback_data="return_info"),
        MenuItem(text="🛠️ Гарантія", callback_data="warranty_info"),
        MenuItem(text="➖➖➖➖➖➖➖➖➖➖➖➖", callback_data="separator"),
        MenuItem(text="🔙 Назад", callback_data="main_menu")
    ]
    return MenuBuilder(items).build()
