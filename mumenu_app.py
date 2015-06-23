from gevent import monkey
monkey.patch_all()

import bottle
from lib.server import HTTPRouter
from micromenu import MicroMenu


router = HTTPRouter()
micro_app = MicroMenu()


@router.post("/customers")
def create_customers(request):
    print request
    return router.json_response({"status": "OK"}, resp=bottle.response)


@router.get("/customers")
def index_customers():
    return micro_app.index_customers()


if __name__ == "__main__":
    bottle.run(host="0.0.0.0", port=8090, server="gevent")