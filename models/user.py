from init import db, ma

class User(db.Model):
    __tablename__ = 'users' # creating users tablename

    id = db.Column(db.Integer, primary_key=True) # primary key
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True) # has to be unique
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True) # optional so nullable True
    is_admin = db.Column(db.Boolean, default=False) # default not admin

class UserSchema(ma.Schema): # subclass of ma.Schema so it can be JSON serilisable
    class Meta: # Meta class containing the fields of the table
        fields = ('id', 'name', 'email', 'address', 'password', 'is_admin')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])