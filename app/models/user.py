from app import db
# Parent Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    recipes = db.relationship("Recipe", backref="user", lazy=True)
    
    # def to_dict(self):
    #         return {
    #         }

    # user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)