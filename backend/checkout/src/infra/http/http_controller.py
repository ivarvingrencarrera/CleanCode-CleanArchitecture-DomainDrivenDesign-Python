from checkout.src.application.usecase.checkout import Checkout
from checkout.src.application.usecase.get_products import GetProducts
from checkout.src.infra.http.http_server import HttpServer


class HttpController:
    def __init__(self, http_server: HttpServer, checkout: Checkout, get_product: GetProducts) -> None:
        self.http_server = http_server
        self.checkout = checkout
        self.get_products = get_product

        self.http_server.on('post', '/checkout', lambda _, body: self.checkout.execute(body))

        self.http_server.on('get', '/products', lambda _: self.get_products.execute())
