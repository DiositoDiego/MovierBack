from unittest.mock import patch, Mock
import unittest
import json

from comments.get_comments import (app)

mock_path = {
    "pathParameters": {
        "id": 1
    }
}


class TestApp(unittest.TestCase):

    @patch.dict("os.environ", {"REGION_NAME": "us-east-2", "DATA_BASE": "movier-test"})
    @patch("comments.get_comments.app.get_comments_with_movie_id")
    @patch("pymysql.connect")
    def test_lambda_handler(self, mock_connect, mock_get_comments_with_movie_id):
        mock_connect.return_value = Mock()
        mock_get_comments_with_movie_id.return_value = [
            {"user_id": 1, "comment": "Me encantó la pelicula de principio a fin"}]

        result = app.lambda_handler(mock_path, None)
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        self.assertIn("data", body)
        self.assertTrue(body["data"])

    @patch.dict("os.environ", {"REGION_NAME": "us-east-2", "DATA_BASE": "movier-test"})
    def test_lambda_handler_missing_parameters(self):
        mock_body = {"body": json.dumps({})}
        result = app.lambda_handler(mock_body, None)
        self.assertEqual(result['statusCode'], 400)
        body = json.loads(result['body'])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "Error al obtener los parámetros del cuerpo de la solicitud")
