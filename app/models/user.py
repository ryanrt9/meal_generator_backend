from app import db
# Parent Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    recipes = db.relationship("Recipe", back_populates="user")
    
    def to_dict(self):
        return {
            "user_id":self.user_id,
            "email":self.email,
            "password":self.password
        }