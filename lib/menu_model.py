import datetime
import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()
Column = sqlalchemy.Column
DateTime = sqlalchemy.DateTime
Integer = sqlalchemy.Integer
String = sqlalchemy.String


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    description = Column(String(250), nullable=True)
    time_created = Column(DateTime)
    time_updated = Column(DateTime)

    @classmethod
    def from_dict(cls, dict_):
        """
        :param dict_:
        :return:
        """
        dict_["time_created"] = datetime.datetime.now()
        dict_["time_updated"] = dict_["time_created"]

        return cls(**dict_)

    def to_dict(self):
        """

        :return:
        """
        return {
            "id": self.id,
            "description": self.description if self.description else "(none)",
            "time_created": "%s" % self.time_created,
            "time_updated": "%s" % self.time_updated
        }

    def update(self, data):
        if "description" in data:
            self.description = data["description"]
            self.time_updated = datetime.datetime.now()


class SubMenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    time_updated = Column(DateTime)
    name = Column(String(length=100))
    description = Column(String(250), nullable=True)
    image = Column(String, nullable=True)


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime)
    time_updated = Column(DateTime)
    name = Column(String(length=100))
    description = Column(String(250), nullable=True)
    price = Column(String)
    process_time = Column(Integer)
    image = Column(String, nullable=True)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///dev.sqlite")
    Base.metadata.create_all(engine, checkfirst=True)

    print Menu.__base__

    menu = Menu.from_dict({
        "description": "hello!"
    })

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(menu)
    session.commit()

    print menu.to_dict()
