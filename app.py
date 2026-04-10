from flask import Flask
from flask_jwt_extended import JWTManager
from database.db import init_db

from Routes.auth import auth_bp
from Routes.items import items_bp
from Routes.transactions import transactions_bp




app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"

@app.route("/")
def home():
    return {
        "message": "TIX Inventory API is running "
    }, 200


jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(transactions_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)