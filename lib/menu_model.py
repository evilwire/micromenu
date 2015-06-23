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
