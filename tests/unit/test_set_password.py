from login.set_password import (app)
import unittest
import json


mock_body = {
    "body": json.dumps({
        "username": "joviicam9@gmail.com",
        "temporary_password": "5HNUbd|D",
        "new_password": "Joviicam123*"
    })
}


class TestApp(unittest.TestCase):
    def test_lambda_handler(self):
        result = app.lambda_handler(mock_body, None)
        print(result)
