from data import users, orders, offers
from app import app, db
from app.models import User, Order, Offer
import prettytable


if __name__ == '__main__':
    db.create_all()

    for line in users:
        db.session.add(User(**line))
    for line in orders:
        db.session.add(Order(**line))
    for line in offers:
        db.session.add(Offer(**line))
    db.session.commit()

    # print([(key, value, type(value)) for key, value in User.__dict__.items()])
    # print([column for column in User.__table__.columns])
    # print([(column.name, column.type) for column in User.__table__.columns])
    # user = User.query.get(1)
    # print(user.columns())

    cursor = db.session.execute(f"SELECT * from {User.__tablename__}").cursor
    mytable = prettytable.from_db_cursor(cursor)
    mytable.max_width = 30
    print(mytable)

    cursor = db.session.execute(f"SELECT * from {Order.__tablename__}").cursor
    mytable = prettytable.from_db_cursor(cursor)
    mytable.max_width = 30
    print(mytable)

    cursor = db.session.execute(f"SELECT * from {Offer.__tablename__}").cursor
    mytable = prettytable.from_db_cursor(cursor)
    mytable.max_width = 30
    print(mytable)

    app.run()
