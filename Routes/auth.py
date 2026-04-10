from flask import Blueprint, request
from Models.user_model import create_user, find_user_by_email, count_cms
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from utils.decorators import role_required
from database.db import get_db_connection


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = generate_password_hash(data["password"])
    role = data.get("role", "USER")

    if find_user_by_email(email):
        return {"error": "Email already exists"}, 400

    if role == "CM" and count_cms() >= 4:
        return {"error": "Max CM reached"}, 400

    create_user(name, email, password, role)

    return {"message": "User created"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = find_user_by_email(data["email"])

    if not user or not check_password_hash(user["password"], data["password"]):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(
        identity=str(user["id"]),  
        additional_claims={
            "role": user["role"]  
        }
    )

    return {"access_token": token}, 200

@auth_bp.route("/users", methods=["GET"])
@role_required("CM")
def get_users():
    conn = get_db_connection()

    users = conn.execute(
        "SELECT id, name, email, role FROM users"
    ).fetchall()

    conn.close()

    return [dict(user) for user in users], 200