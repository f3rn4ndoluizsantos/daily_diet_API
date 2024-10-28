from flask import Flask
from database import db
from routers.router_user import router_user
from routers.router_snack import router_snack
from extensions import login_manager
from models.user import User

app = Flask(__name__)


app.config["SECRET_KEY"] = "s3cr3t"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-diet"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


login_manager.init_app(app)
# login_manager.init_app(router_user)
# login_manager.init_app(router_snack)
login_manager.login_view = "router_user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(router_user, url_prefix="/users")
app.register_blueprint(router_snack, url_prefix="/snack")


@app.route("/")
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True, port="3003")
