import time

from flask import Flask, render_template, request, make_response

from database.model import fill_products, get_products, get_products_dict, insert_order, update_info

app = Flask(__name__, static_url_path='/static')

sessions = {}
products_cache = get_products_dict()
# fill_products()


@app.route('/')
def index():
    products = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "image_link": row[3],
            "price": row[4]
        } for row in get_products()
    ]

    session_id = request.cookies.get("session-id", None)
    cart = []
    if (session_id is not None) and (session_id in sessions):
        for product_id, quantity in sessions[session_id].items():
            if (product_id not in products_cache) or (quantity <= 0):
                continue

            cart.append({
                "name": products_cache[product_id]["name"],
                "price": products_cache[product_id]["price"],
                "quantity": quantity,
                "id": product_id
            })

    return render_template("bucket.html", products=products, cart=cart)


@app.route("/cart-add/<product_id>", methods=['GET'])
def add_to_cart(product_id):
    if str(product_id) not in products_cache:
        return

    session_id = request.cookies.get("session-id", None)
    if session_id is None:
        session_id = str(time.time())

    if session_id not in sessions:
        sessions[session_id] = {}

    sessions[session_id][product_id] = sessions[session_id].get(product_id, 0) + 1

    resp = make_response("200")
    resp.set_cookie("session-id", session_id)
    return resp


@app.route("/cart-del/<product_id>", methods=['GET'])
def del_to_cart(product_id):
    if str(product_id) not in products_cache:
        return

    session_id = request.cookies.get("session-id", None)
    if session_id is None:
        session_id = str(time.time())

    if session_id not in sessions:
        sessions[session_id] = {}

    sessions[session_id][product_id] = sessions[session_id].get(product_id, 0) - 1
    if sessions[session_id][product_id] < 0:
        sessions[session_id][product_id] = 0

    resp = make_response("200")
    resp.set_cookie("session-id", session_id)
    return resp


@app.route("/order-buy", methods=['GET'])
def order_buy():
    session_id = request.cookies.get("session-id", None)
    if (session_id is None) or (session_id not in sessions) or (not sessions[session_id]):
        return "empty"

    in_cart = []
    summa = 0
    for product_id, quantity in sessions[session_id].items():
        if (product_id not in products_cache) or (quantity <= 0):
            continue
        in_cart.append(f"{products_cache[product_id]['name']} x {quantity}")
        summa += products_cache[product_id]["price"] * quantity

    in_cart.append(f"Итого: {summa}Р")
    return "; ".join(in_cart)


@app.route("/order-commit", methods=['GET'])
def order_commit():
    session_id = request.cookies.get("session-id", None)
    if (session_id is None) or (session_id not in sessions) or (not sessions[session_id]):
        return "Не хватает данных для оформления заказа"

    email = request.args.get("email")
    address = request.args.get("address")

    if (not email) or (not address):
        return "Не хватает данных для оформления заказа"

    order_id = insert_order(session_id, sessions[session_id], email, address)

    in_cart = []
    summa = 0
    for product_id, quantity in sessions[session_id].items():
        if (product_id not in products_cache) or (quantity <= 0):
            continue
        in_cart.append(f"{products_cache[product_id]['name']} x {quantity}")
        summa += products_cache[product_id]["price"] * quantity

    sessions[session_id] = {}
    return render_template(
        "message.html",
        data={
            "order_id": order_id,
            "summa": summa,
            "products": in_cart
        }
    )


@app.route("/update-row", methods=['GET'])
def update_row_handler():
    update_info()

if __name__ == '__main__':
    app.run()
