import unittest
from unittest.mock import patch, MagicMock
import json
from comments.get_comments.app import lambda_handler, movie_exists, get_comments_with_movie_id
from comments.get_comments.utils import get_secret, get_connection


class TestLambdaFunctions(unittest.TestCase):

    def setUp(self):
        self.event = {
            'pathParameters': {
                'id': '1'
            }
        }
        self.context = {}

    @patch('comments.get_comments.app.get_connection')
    @patch('comments.get_comments.app.movie_exists')
    @patch('comments.get_comments.app.get_comments_with_movie_id')
    def test_lambda_handler_success(self, mock_get_comments, mock_movie_exists, mock_get_connection):
        # Mock responses
        mock_movie_exists.return_value = True
        mock_get_comments.return_value = [
            {'comment_id': 1, 'user_id': 1, 'movie_id': 1, 'comment': 'Great movie!', 'date': '2024-08-19 00:00:00',
             'username': 'user1'}]

        response = lambda_handler(self.event, self.context)
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('Comentarios', body)

    @patch('comments.get_comments.app.get_connection')
    @patch('comments.get_comments.app.movie_exists')
    def test_lambda_handler_movie_id_error(self, mock_movie_exists, mock_get_connection):
        # Invalid movie ID in the event
        self.event['pathParameters']['id'] = 'invalid'

        response = lambda_handler(self.event, self.context)
        self.assertEqual(response['statusCode'], 400)
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Error al obtener los parámetros del cuerpo de la solicitud')

    @patch('comments.get_comments.app.get_connection')
    @patch('comments.get_comments.app.movie_exists')
    def test_lambda_handler_movie_not_exists(self, mock_movie_exists, mock_get_connection):
        # Movie does not exist
        mock_movie_exists.return_value = False

        response = lambda_handler(self.event, self.context)
        self.assertEqual(response['statusCode'], 400)
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'La película no existe')

    @patch('comments.get_comments.app.get_connection')
    @patch('comments.get_comments.app.movie_exists')
    @patch('comments.get_comments.app.get_comments_with_movie_id')
    def test_lambda_handler_database_error(self, mock_get_comments, mock_movie_exists, mock_get_connection):
        # Simulate database error
        mock_get_comments.side_effect = Exception('Database error')
        mock_movie_exists.return_value = True

        response = lambda_handler(self.event, self.context)
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertEqual(body['message'], 'Error al obtener los comentarios de la base de datos')

    @patch('comments.get_comments.utils.get_secret')
    @patch('comments.get_comments.utils.get_connection')
    def test_get_connection_success(self, mock_get_connection, mock_get_secret):
        # Mock secret retrieval and connection
        mock_get_secret.return_value = {
            'host': 'localhost',
            'username': 'user',
            'password': 'pass',
            'dbInstanceIdentifier': 'dbname',
            'port': 3306
        }
        mock_get_connection.return_value = MagicMock()

        # Directly test get_connection behavior
        connection = get_connection()
        self.assertIsInstance(connection, MagicMock)

    @patch('comments.get_comments.utils.get_secret')
    def test_get_secret_success(self, mock_get_secret):
        # Mock secret retrieval
        mock_get_secret.return_value = {
            'host': 'localhost',
            'username': 'user',
            'password': 'pass',
            'dbInstanceIdentifier': 'dbname',
            'port': 3306
        }

        secret = get_secret()
        self.assertEqual(secret['host'], 'localhost')


if __name__ == '__main__':
    unittest.main()
