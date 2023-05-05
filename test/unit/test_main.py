import pytest
from fastapi.testclient import TestClient

from src.main import app

STATUS_CODE_OK = 200


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_checkout_with_invalid_cpf(client: TestClient) -> None:
    input_ = {'cpf': '406.302.170-27'}
    response = client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    assert output['message'] == 'Invalid cpf'


def test_empty_checkout(client: TestClient) -> None:
    input_ = {'cpf': '353.775.320-90'}
    response = client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    assert output['total'] == 0


def test_checkout_with_3_products(client: TestClient) -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [
            {'id_product': 1, 'quantity': 1},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3},
        ],
    }
    response = client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    total = 6090
    assert output['total'] == total


def test_checkout_with_3_products_with_coupon(client: TestClient) -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [
            {'id_product': 1, 'quantity': 1},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3},
        ],
        'coupon': 'VALE20',
    }
    response = client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    total = 4872
    assert output['total'] == total
