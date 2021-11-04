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

    # DEBUG
    # cursor = db.session.execute(f"SELECT * from {User.__tablename__} limit 5").cursor
    # mytable = prettytable.from_db_cursor(cursor)
    # mytable.max_width = 30
    # print(mytable)
    #
    # cursor = db.session.execute(f"SELECT * from {Order.__tablename__} limit 5").cursor
    # mytable = prettytable.from_db_cursor(cursor)
    # mytable.max_width = 30
    # print(mytable)
    #
    # cursor = db.session.execute(f"SELECT * from {Offer.__tablename__} limit 5").cursor
    # mytable = prettytable.from_db_cursor(cursor)
    # mytable.max_width = 30
    # print(mytable)

    app.run()
