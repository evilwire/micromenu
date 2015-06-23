from gevent import monkey, Timeout

monkey.patch_all()

from bottle import delete, get, post, request, response, route
from json import dumps


class TimeoutError(Exception):
    pass


class HTTPRouter(object):

    @staticmethod
    def add_xorigin(resp):
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        resp.set_header(
            'Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        resp.set_header(
            'Access-Control-Allow-Headers',
            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

    @staticmethod
    def json_response(dict_, resp, status=200):
        resp.content_type = "application/json; charset=utf-8"
        resp.status = status
        return dumps(dict_)


    def build_method(self, timeout, method_):
        """
        Returns a method wrapping a given method to be used as a bottle
        endpoint handler with a built in time-out.
        :param timeout: the number of seconds the code has before the request
            times out
        :type timeout: int
        :param method_: the method to wrap around
        :type method_: FunctionType
        :return: a method wrapping the given method that times out in a given
            amount of time
        """

        def __http_method(*vargs, **kargs):
            HTTPRouter.add_xorigin(response)
            response.content_type = "application/json"
            with Timeout(timeout, TimeoutError):
                try:
                    method_response = method_(*vargs, **kargs)
                    if hasattr(method_response, "set_header"):
                        HTTPRouter.add_xorigin(method_response)

                    response.status = 200
                    return method_response

                except TimeoutError:
                    return HTTPRouter.json_response({
                        "status": "error",
                        "errors": [{
                            "message": ("Your request took too long to "
                                        "process. We are sorry for the " +
                                        "inconvenience."),
                            "code": 408,
                        }],
                        "query": ""
                    }, status=408, resp=response)
        return __http_method

    def route(self, timeout=30, *vargs, **kargs):
        """
        A decorator modifying a given method to set timeout and is granted
        with
        :param timeout:
        :param vargs:
        :param kargs:
        :return:
        """

        def multi(method_):
            return route(*vargs, **kargs)(
                self.build_method(timeout, method_))
        return multi

    def post(self, path, timeout=30):
        """
        :param path:
        :param timeout:
        :return:
        """

        def multi(method_):
            def with_input():
                return method_(request.json)
            return post(path)(self.build_method(timeout, with_input))
        return multi

    def get(self, path, timeout=30):
        """
        :param path:
        :param timeout:
        :return:
        """
        def multi(method_):
            return get(path)(self.build_method(timeout, method_))
        return multi