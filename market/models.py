from market import db , bcrypt, login_manager
from market import  bcrypt

from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Just model of the user scheme
    """
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=16), nullable=False)
    budget = db.Column(db.Integer(), nullable=False,default=1000)
    items = db.relationship('Item', backref='owner_user', lazy=True)


    @property
    def prettier_budget(self):
        if len(str(self.budget)) >=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'
    @property
    def password(self):
        return self.password


    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        if self.budget >= item_obj.price:
            return True
        else :
            return False


    def __repr__(self):
        return f'Item {self.user_name}, id: {self.id}'

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
   
    def buy(self, current_user):
        self.owner = current_user.id
        current_user.budget -= self.price
        db.session.commit()
    def sell(self, current_user):
        current_user.budget += self.price
        self.owner = None
        db.session.commit()
    def __repr__(self):
        return f'Item {self.name}, id: {self.id}'

# db.create_all()