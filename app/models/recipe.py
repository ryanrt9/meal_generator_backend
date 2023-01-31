from app import db
# Child Model
class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    ingredients =db.Column(db.ARRAY(db.String))
    image = db.Column(db.String)
    recipe_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # user= db.relationship("User", back_populates="recipes")