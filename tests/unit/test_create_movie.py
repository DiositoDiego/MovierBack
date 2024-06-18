from unittest.mock import patch, Mock
import unittest
import json
import pymysql

from movies.create_movie import (app)

mock_body = {
    "body": json.dumps({
        "title": "Test1",
        "description": "Test1",
        "genre": "Comedia",
        "image": "dsad",
        "status": 1
    })
}


class TestApp(unittest.TestCase):

    @patch.dict("os.environ", {"REGION_NAME": "us-east-2", "DATA_BASE": "movier-test"})
    @patch("movies.create_movie.app.movie_exists")
    @patch("movies.create_movie.app.insert_into_movies")
    @patch("pymysql.connect")
    def test_lambda_handler(self, mock_connect, mock_insert_into_movies, mock_movie_exists):
        mock_connect.return_value = Mock()
        mock_movie_exists.return_value = False
        mock_insert_into_movies.return_value = None

        result = app.lambda_handler(mock_body, None)

        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "Película insertada correctamente")

        mock_movie_exists.assert_called_once_with("Test1")
        mock_insert_into_movies.assert_called_once_with("Test1", "Test1", "Comedia", "dsad", 1)


if __name__ == "__main__":
    unittest.main()
