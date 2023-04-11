#from run import db
from  flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user

app= Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager()

login_manager.login_view = 'user_login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    curr_user= User.query.filter_by(id = user_id).first()
    return curr_user

# @login_manager.user_loader()
# def load_user(user_id):
#     curr_user= User.query.filter_by(id = user_id).first()
#     return curr_user

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(20),unique=True, nullable = False)
    password = db.Column(db.String(20),nullable = False)
    email= db.Column(db.String(120),unique =True, nullable=False)
    phone = db.Column(db.String(10), nullable=False,default='0720000000')
   # consumption = db.Column(db.DECIMAL(10, 2), default=0)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    orders = db.relationship('Orders', backref=db.backref('user',lazy=True))
    def __repr__(self):
        return '<User %r>'%self.username

class Pizza(db.Model):
    __tablename__ = 'pizza'
    id = db.Column(db.Integer, primary_key = True,autoincrement= True)
    name = db.Column(db.String(50),nullable =False)
    price = db.Column(db.DECIMAL(10, 2))
    size = db.Column(db.String(20))
    picture = db.Column(db.String(255),default='/static/images/Margherita.jpeg')
    toppings = db.Column(db.Text)
#   views_count = db.Column(db.Integer, default=0)
    inventory = db.Column(db.Integer, default=100)
    sold = db.Column(db.Integer, default=0)

    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    cart = db.relationship("Cart", backref='pizza')
    orders_detail = db.relationship("OrdersDetail", backref='pizza')

    def __repr__(self):
        return "<Pizza %r>" % self.name

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    user_id = db.Column(db.Integer)
    number = db.Column(db.Integer, default=0)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Cart %r>" % self.id


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    receive_name = db.Column(db.String(255))
    receive_address = db.Column(db.String(255))
    receive_tel = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    order_status=db.Column(db.String(20))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    orders_detail = db.relationship("OrdersDetail", backref='orders')  # 外键关系关联

    def __repr__(self):
        return "<Orders %r>" % self.id


class OrdersDetail(db.Model):
    __tablename__ = 'orders_detail'
    id = db.Column(db.Integer, primary_key=True)
    pizzas_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    number = db.Column(db.Integer, default=0)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(100), unique=True,nullable = False)
    password = db.Column(db.String(100),unique=True,nullable = False)

    def __repr__(self):
        return "<Admin %r>"%self.manager
