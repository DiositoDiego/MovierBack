import unittest
import json

from login.loginUsers import (app)

mock_body = {
    "body": json.dumps({
        "username": "20213tn096@utez.edu.mx",
        "password": "!Game123Game"
    })
}


class TestApp(unittest.TestCase):
    def test_lambda_handler(self):
        result = app.lambda_handler(mock_body, None)
        print(result)
