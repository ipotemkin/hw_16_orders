from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String, db.CheckConstraint("role in ('customer', 'executor')"))
    phone = db.Column(db.String)
    # orders = db.relationship('Order', backref='user', lazy='dynamic')  # orders - user
    offers = db.relationship('Offer', backref='user', lazy='dynamic')  # offers - user


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))  # offers - order
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # offers - user


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # orders - user 1
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # orders - user 2
    offers = db.relationship('Offer', backref='order', lazy='dynamic')  # offers - order

