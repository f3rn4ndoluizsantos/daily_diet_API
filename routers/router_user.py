from flask import request
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from models.user import User
from flask import Blueprint, jsonify
from database import db
import bcrypt

# Create a Blueprint
router_user = Blueprint("router_user", __name__)

# login_manager = LoginManager()
# login_manager.init_app(router_user)
# login_manager.login_view = "login"


# @login_manager.user_loader
# def load_user(user_id):
#     return db.session.get(User, int(user_id))


@router_user.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # user = User.query.filter_by(username=username).all() # return list of user
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(str.encode(password), str.encode(user.password)):
                login_user(user)
                return jsonify({"message": "Authenticated successfully"}), 200
            else:
                return jsonify({"message": "Wrong username or password"}), 401
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "username and password are required"}), 400


@router_user.route("/logout", methods=["GET"])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "User logged out successfully"}), 401

    return jsonify({"message": "User not logged in"}), 401


@router_user.route("/add", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username and email and password:
        hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 201

    return jsonify({"message": "username, email and password are required"}), 400


@router_user.route("/all", methods=["GET"])
@login_required
def get_users():
    print("")
    if current_user.role == "admin":
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    else:
        return jsonify({"message": "Unauthorized"}), 403


@router_user.route("/one/<int:id_user>", methods=["GET"])
@login_required
def get_user(id_user):
    user = db.session.get(User, id_user)
    print(user)

    if user:
        return jsonify(user.to_dict()), 200

    return jsonify({"message": "User not found"}), 404


@router_user.route("/upd/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    # user = User.query.get(id_user)
    user = db.session.get(User, id_user)

    if id_user != current_user.id and current_user.role == "user":
        print("entrou aqui", current_user)
        return jsonify({"message": "Unauthorized"}), 403

    if user:
        # user.username = data.get("username") pode ocorrer um problema pois está logado, com o username
        user.email = data.get("email")
        user.password = bcrypt.hashpw(
            str.encode(data.get("password")), bcrypt.gensalt()
        )
        user.role = data.get("role")
        db.session.commit()
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"message": "User not found"}), 404


@router_user.route("/delete/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    if user and user.id != current_user.id:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404
