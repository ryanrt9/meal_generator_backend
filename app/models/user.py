from app import db
# Parent Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username 
    email = db.Column(db.String)
    recipes = db.relationship("Recipe", back_populates="user")
    # leave off for now- what this means if the page is refreshed user has to input ingredients in again
    # if we add, we'll need to write additional code to save each ingredient with the ability for the user to add more in the future.
    # ingredients =db.Column(db.Array(db.String))# Column("data",ARRAY(String))

    # def to_dict(self):
    #         return {
    #         }

    # user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
