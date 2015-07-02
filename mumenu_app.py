from gevent import monkey
monkey.patch_all()

import bottle
from lib.server import HTTPRouter
from micromenu import MicroMenu


router = HTTPRouter()
micro_app = MicroMenu()


@router.post("/menus")
def create_menus(request):
    menu = micro_app.create_menu(request)
    return router.json_response({
        "status": "OK",
        "data": menu.to_dict()
    }, resp=bottle.response)


@router.get("/menus")
def index_customers():
    return router.json_response({
        "status": "OK",
        "data": micro_app.list_menus()
    }, resp=bottle.response)


if __name__ == "__main__":
    bottle.run(host="0.0.0.0", port=8090, server="gevent")