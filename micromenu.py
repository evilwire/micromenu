import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from lib.menu_model import Base as MenuBase, Menu


class MicroMenu(object):
    def __init__(self):
        # TODO: hardcoded in value
        self.engine = sqlalchemy.create_engine(
            "sqlite:////tmp/dev.sqlite")

        # create all the models in the Menu model
        # checking first to see if the schema exists
        MenuBase.metadata.create_all(self.engine,
                                     checkfirst=True)

        self.scoped_session = scoped_session(
            sessionmaker(bind=self.engine))

    def create_menu(self, dict_):
        session = self.scoped_session()
        menu = Menu.from_dict(dict_)
        session.add(menu)
        session.commit()
        return menu

    def get_menu(self, menu_id):
        session = self.scoped_session()
        menu = session.query(Menu).filter_by(id=menu_id).first()
        if not menu:
            return None

        return menu.to_dict()

    def update_menu(self, menu_id, data):
        session = self.scoped_session()
        menu = session.query(Menu).filter_by(id=menu_id).first()
        if not menu:
            return False

        if menu.update(data):
            session.add(menu)
            session.commit()
            return True

    def delete_menu(self, menu_id):
        session = self.scoped_session()
        menu = session.query(Menu).filter_by(id=menu_id).first()
        if not menu:
            return False

        session.delete(menu)
        session.commit()

    def list_menus(self, start=0, end=10):
        session = self.scoped_session()
        menus = session.query(Menu).slice(start, end)
        return [menu.to_dict() for menu in menus]

if __name__ == "__main__":
    mumenu = MicroMenu()
    mumenu.create_menu({
        "description": "Hello World!"
    })

    print mumenu.get_menu(1)
    print mumenu.list_menus()