from database import db
from models.user import User

# from flask_login import UserMixin


class Snack(db.Model):

    __tablename__ = "sancks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    is_on_diet = db.Column(db.Boolean, default=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def __repr__(self):
        return f"<Snack('name={self.name}', description={self.description}, is_on_diet={self.is_on_diet}, created_at={self.created_at}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_on_diet": self.is_on_diet,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
