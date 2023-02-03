from app import db
# Child Model
class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String)
    recipe_url = db.Column(db.String)
    time= db.Column(db.Integer)
    # Should we remove nullable = True because the only time we'll be using these models is for users that 
    # are signed in to save recipes
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", back_populates="recipes")

    def to_dict(self):
        recipe_dict = {}
        recipe_dict["recipe_id"] = self.recipe_id
        recipe_dict["title"] = self.title
        recipe_dict["image"] = self.image
        recipe_dict["recipe_url"] = self.recipe_url     
        recipe_dict["time"] = self.time
        recipe_dict["user_id"] = self.user_id
        return recipe_dict

    @classmethod

    def from_dict(cls, request_body):
        return cls(
            recipe_id=request_body["recipe_id"],
            title=request_body["title"],
            image=request_body["image"],
            recipe_url= request_body["recipe_url"],
            time= request_body["time"],
            user_id= request_body["user_id"]
        )