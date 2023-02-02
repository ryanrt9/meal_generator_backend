from app import db
# Child Model
class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    recipe_url = db.Column(db.String)
    # the reason why we have nullable=True here is because not all users are signed in
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)

    # def to_dict(self):
    #     recipe_dict = {}
    #     recipe_dict["recipe_id"] = self.id
    #     recipe_dict["image"]
    #     recipe_dict["recipe_url"]       

    #     if self.user_id == None:
    #         recipe_dict["user_id"] = None
    #     else:
    #         recipe_dict["user_id"] = self.user_id