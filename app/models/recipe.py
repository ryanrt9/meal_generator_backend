from app import db
# Child Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredients =db.Column(db.Array(db.String))
    instruction = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user= db.relationship("User", back_populates="recipes")

