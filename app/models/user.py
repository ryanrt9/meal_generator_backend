from app import db
# Parent Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    # change to back populate
    # recipes = db.relationship("Recipe", backref="user", lazy=True)
    recipes = db.relationship("Recipe", back_populates="user")
    # confirm that recipes in this user model is going to hold everything that is in the Recipe model
    
    def to_dict(self):
        return {
            "user_id":self.user_id,
            "email":self.email,
            "password":self.password
        }

    # user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)