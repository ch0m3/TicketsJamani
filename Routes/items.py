from flask import Blueprint, request
from database.db import get_db_connection
from utils.decorators import role_required

items_bp = Blueprint("items", __name__, url_prefix="/items")


@items_bp.route("/", methods=["GET"])
def get_items():
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items").fetchall()
    conn.close()

    return [dict(item) for item in items], 200


@items_bp.route("/", methods=["POST"])
@role_required("CM")
def create_item():
    data = request.get_json()

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO items (name, price, stock, borrow_duration) VALUES (?, ?, ?, ?)",
        (data["name"], data["price"], data["stock"], data["borrow_duration"])
    )
    conn.commit()
    conn.close()

    return {"message": "Item created"}, 201


@items_bp.route("/<int:id>", methods=["PATCH"])
@role_required("CM")
def update_item(id):
    data = request.get_json()

    conn = get_db_connection()
    conn.execute(
        """UPDATE items 
           SET name = ?, price = ?, stock = ?, borrow_duration = ?
           WHERE id = ?""",
        (data["name"], data["price"], data["stock"], data["borrow_duration"], id)
    )
    conn.commit()
    conn.close()

    return {"message": "Item updated"}, 200


@items_bp.route("/<int:id>", methods=["DELETE"])
@role_required("CM")
def delete_item(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Item deleted"}, 200