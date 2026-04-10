from flask import Blueprint, request
from database.db import get_db_connection
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from utils.decorators import role_required
from datetime import datetime, timedelta

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions_bp.route("/borrow", methods=["POST"])
def borrow_item():
    verify_jwt_in_request()
    user = get_jwt_identity()

    data = request.get_json()
    item_id = data.get("item_id")

    conn = get_db_connection()

    item = conn.execute(
        "SELECT * FROM items WHERE id = ?",
        (item_id,)
    ).fetchone()

    if not item or item["stock"] <= 0:
        return {"error": "Item unavailable"}, 400

    conn.execute("UPDATE items SET stock = stock - 1 WHERE id = ?", (item_id,))

    due_date = datetime.utcnow() + timedelta(days=item["borrow_duration"])

    conn.execute(
        """INSERT INTO transactions (user_id, item_id, type, date, due_date)
           VALUES (?, ?, 'BORROW', ?, ?)""",
        (user["id"], item_id, datetime.utcnow(), due_date)
    )

    conn.commit()
    conn.close()

    return {"message": "Borrowed"}, 200


@transactions_bp.route("/return", methods=["POST"])
def return_item():
    verify_jwt_in_request()
    user = get_jwt_identity()

    data = request.get_json()
    tx_id = data.get("transaction_id")

    conn = get_db_connection()

    tx = conn.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (tx_id,)
    ).fetchone()

    if not tx or tx["user_id"] != user["id"]:
        return {"error": "Unauthorized"}, 403

    if tx["returned_at"]:
        return {"error": "Already returned"}, 400

    conn.execute("UPDATE items SET stock = stock + 1 WHERE id = ?", (tx["item_id"],))

    conn.execute(
        "UPDATE transactions SET returned_at = ? WHERE id = ?",
        (datetime.utcnow(), tx_id)
    )

    conn.commit()
    conn.close()

    return {"message": "Returned"}, 200


@transactions_bp.route("/my", methods=["GET"])
def my_transactions():
    verify_jwt_in_request()
    user = get_jwt_identity()

    conn = get_db_connection()

    txs = conn.execute(
        """SELECT t.*, i.name as item_name
           FROM transactions t
           JOIN items i ON t.item_id = i.id
           WHERE t.user_id = ?""",
        (user["id"],)
    ).fetchall()

    conn.close()

    return [dict(tx) for tx in txs], 200


@transactions_bp.route("/", methods=["GET"])
@role_required("CM")
def all_transactions():
    conn = get_db_connection()

    txs = conn.execute(
        """SELECT t.*, u.name as user_name, i.name as item_name
           FROM transactions t
           JOIN users u ON t.user_id = u.id
           JOIN items i ON t.item_id = i.id"""
    ).fetchall()

    conn.close()

    return [dict(tx) for tx in txs], 200