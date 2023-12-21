import datetime
import time

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Text, DateTime, Boolean, ForeignKey, \
    select
from sqlalchemy.sql.functions import now

metadata = MetaData()

products = Table(
    'products', metadata,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('name', String(200), nullable=False),
    Column('description', String(), nullable=False),
    Column('image_link', String(), nullable=False),
    Column('price', Integer(), nullable=False),
)

orders = Table(
    'orders', metadata,
    Column('id', Integer(), primary_key=True, autoincrement=True),
    Column('date_at', DateTime(), default=now()),
    Column('email', String(), nullable=False),
    Column('address', String(), nullable=False),
    Column('session_id', String(), nullable=False)
)

products_orders = Table(
    'orders_products', metadata,
    Column('product_id', ForeignKey('products.id')),
    Column('order_id', ForeignKey('orders.id')),
    Column('amount', Integer())
)

engine = create_engine("sqlite:///sqlite3.db")
metadata.create_all(engine)


def fill_products():
    products_fixture = {
        "Кружка с надписью «Для папы»": [
            "https://static.tildacdn.com/tild3264-3066-4361-b665-643336333964/2-001-.png",
            340,
            "Эта кружка идеально подходит для подарка вашему отцу. Она имеет уникальный дизайн и надпись «Для папы», которая напомнит ему о вашей любви и уважении."],
        "Набор для уюта «Домашний очаг»": [
            "https://cdn.leroymerlin.ru/lmru/image/upload/v1678745069/b_white,c_pad,d_photoiscoming.png,f_auto,h_600,q_auto,w_600/lmcode/6QZOmhfZZEyaQsIAsCwfgQ/90637146.jpg",
            999,
            "Набор для уюта «Домашний очаг» поможет создать атмосферу комфорта и уюта в вашем доме. В него входят ароматические свечи, мягкий плед и красивая ваза."],
        "Годовой запас носков": [
            "https://ir.ozone.ru/s3/multimedia-i/c1000/6003599694.jpg",
            1500,
            "Годовым запасом носков вы обеспечите себя комфортом на целый год. В комплекте 72 пары носков из мягкого дышащего материала."],
        "Монета «На счастье»": [
            "https://www.bon.kz/wp-content/uploads/2021/06/Tree_of_Luck_amethyst1.jpg",
            200,
            "Монета «На счастье» станет отличным подарком для тех, кто верит в силу талисманов. Она имеет уникальный дизайн и принесет удачу своему обладателю."],
        "Дерево счастья": [
            "https://zeltta.ru/upload/resize_cache/iblock/0e4/750_1000_10ca8ff9f27699851caf9d9378ff6e09d/0e4c20f6ba867b0f828106d4e16ec3bf.jpg",
            700,
            "Описание не добавлено"],
        "Шкатулка «Сокровища»": [
            "https://www.hobbyportal.ru/data/products/cache/2018feb/10/22/163428_50644.jpg",
            290,
            "Шкатулка «Сокровища» - это стильное и практичное изделие. Она выполнена из качественных материалов и имеет уникальный дизайн."],
        "Подушка «Доброй ночи»": [
            "https://www.pinkbus.ru/im/600x600/286872/2/750644/262.jpg",
            760,
            "Подушка «Доброй ночи» поможет вам заснуть быстро и спать крепко. Она имеет удобную форму и мягкий наполнитель."],
        "Зажигалка Zippo": [
            "https://izippo.ru/image/catalog/blog2/zajigalka-zippo-kak-otlichit-original-ot-potdelki-1.jpg",
            3000,
            "Описание не добавлено"],
        "Гамак для квартиры": [
            "https://ae04.alicdn.com/kf/S92bbdf019a234eee81a602f57a010a1bV.jpg",
            2200,
            "Гамак для квартиры - это удобное и стильное решение для создания зоны отдыха в вашем доме. Он выполнен из прочных материалов и имеет уникальный дизайн."],
        "Радио для души": [
            "https://ae01.alicdn.com/kf/Se93d7025a8a84915bfaa21b502c08020w.jpg",
            7700,
            "Радио для души - это не просто устройство для прослушивания музыки, но и стильный элемент декора. Оно имеет красивый дизайн и позволяет слушать любимые песни в высоком качестве."],
        "Набор посуды": [
            "https://ae04.alicdn.com/kf/Sf938e930f60c4e75b9d3c014815acec6y.jpg",
            9000,
            "Набор качественной и стильной посуды, который будет полезен в повседневной жизни и при сервировке стола. Можно выбрать набор с разным количеством предметов и материалом: керамика, стекло, нержавеющая сталь и т.д."
        ],
        "Термокружка": [
            "https://posylka-cdn.s3.eu-central-1.amazonaws.com/products/08202963/1000/08202963_9.jpg",
            1400,
            "Стильная и функциональная термокружка, которая поможет сохранить напиток горячим или холодным на длительное время. Можно выбрать термокружку с разным дизайном и объемом: от 250 мл до 1 литра."
        ],
        "Фотоальбом": [
            "https://shop-cdn1-2.vigbo.tech/shops/93092/products/21718305/images/3-05a901e90dc703ebfc8fec7009e95504.jpg",
            100,
            "Красивый и оригинальный фотоальбом, в котором можно хранить и просматривать фотографии. Можно выбрать фотоальбом с разным дизайном и вместимостью: от 100 до 1000 фотографий"
        ],
        "Бокалы": [
            "https://posylka-cdn.s3.eu-central-1.amazonaws.com/products/08055701/1000/08055701_7.jpg",
            2999,
            "Описание не добавлено"
        ],
        "Набор инструментов": [
            "https://www.kaufbei.tv/out/pictures/master/product/1/4310_schwartzman_sm-108_1.jpg",
            54000,
            "Набор качественных и функциональных инструментов, которые помогут в ремонте и повседневных делах. Можно выбрать набор с разным количеством предметов и инструментами"
        ],
        "Книга": [
            "https://store.artlebedev.ru/products/images/804a54ch.jpg",
            300,
            "Интересная и познавательная книга, которая будет полезна и интересна получателю. Можно выбрать книгу по разным темам: художественная литература, научно-популярные издания, биографии и т.д."
        ],
        "Подарочный набор косметики": [
            "https://posylka-images.s3.eu-central-1.amazonaws.com/08/50/30/69/08503069_1.jpg",
            8950,
            "Набор косметических средств, подобранных в соответствии с предпочтениями и типом кожи получателя. В набор могут входить кремы, лосьоны, гели, маски и другие косметические продукты."
        ],
        "Футболка": [
            "https://store.artlebedev.ru/products/images/euxy7tc7.jpg",
            600,
            "Стильная и удобная футболка с интересным дизайном, которая будет отлично смотреться на получателе. Можно выбрать футболку с разными принтами: с логотипами брендов, с юмористическими надписями, с изображениями животных и т.д."
        ],
        "Шарф": [
            "https://leo-ventoni.ru/upload/iblock/39a/h1eipu4ru4lwxy2dt4lulyrf5vab54fv.jpg",
            600,
            "Теплый и стильный шарф, который будет защищать от холода и ветра. Можно выбрать шарф с разными дизайнами: с узорами, с логотипами брендов, с яркими цветами и т.д."
        ],
        "Кошелёк": [
            "https://shop-cdn1-2.vigbo.tech/shops/46679/products/16892804/images/3-9344812d7cc8f3b37f776352a133d9f5.jpg",
            450,
            "Стильный и функциональный кошелёк, который поможет организовать финансы и будет удобен в использовании. Можно выбрать кошелёк с разным количеством отделений и из разных материалов: кожа, металл, пластик и т.д."
        ],
    }

    conn = engine.connect()
    for name, info in products_fixture.items():
        conn.execute(
            products.insert().values(
                name=name,
                image_link=info[0],
                price=info[1],
                description=info[2]
            )
        )

    conn.commit()


def get_products():
    return engine.connect().execute(products.select()).fetchall()


def get_products_dict():
    return {
        str(row[0]): {
            "name": row[1],
            "description": row[2],
            "image_link": row[3],
            "price": row[4]
        } for row in engine.connect().execute(products.select()).fetchall()
    }


def insert_order(session_id: str, order_info: dict, email, address) -> int:
    conn = engine.connect()
    r = conn.execute(
        orders.insert().values(
            date_at=datetime.datetime.now(),
            email=email,
            address=address,
            session_id=session_id.replace(".", "")
        )
    )

    order_id = r.inserted_primary_key[0]
    for product_id, amount in order_info.items():
        conn.execute(
            products_orders.insert().values(
                product_id=product_id,
                order_id=order_id,
                amount=amount
            )
        )
    conn.commit()
    return order_id


def update_info():
    conn = engine.connect()

    for row_id, description in [
        (5, "Дерево счастья - это красивый и символичный подарок. Его ветви украшены яркими лентами, которые напоминают о важных событиях в жизни."),
        (8, "Зажигалка Zippo - это стильный и функциональный аксессуар. Она выполнена из прочных материалов и имеет уникальный дизайн, который можно персонализировать."),
        (14, "Стильные и качественные бокалы, которые подойдут для сервировки напитков. Можно выбрать бокалы с разным дизайном и материалом: стекло, хрусталь, металл и т.д."),
    ]:
        conn.execute(
            products.update().where(
                products.c.id == row_id
            ).values(
                description=description
            )
        )
    conn.commit()
    return 5, 8, 14
