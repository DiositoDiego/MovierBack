from unittest.mock import patch, Mock
import unittest
import json

from comments.delete_comment import (app)

mock_body = {
    "body": json.dumps({
        "user_id": 1,
        "comment_id": 1
    })
}


class TestApp(unittest.TestCase):

        @patch.dict("os.environ", {"REGION_NAME": "us-east-2", "DATA_BASE": "movier-test"})
        @patch("comments.delete_comment.app.get_comment_with_id")
        @patch("comments.delete_comment.app.delete_comment")
        @patch("pymysql.connect")
        def test_lambda_handler(self, mock_connect, mock_get_comment_with_id, mock_delete_comment):
            mock_connect.return_value = Mock()
            mock_get_comment_with_id.return_value = True
            mock_delete_comment.return_value = True

            result = app.lambda_handler(mock_body, None)

            self.assertEqual(result['statusCode'], 500)
            body = json.loads(result['body'])
            self.assertIn("message", body)
            self.assertEqual(body["message"], "Comentario eliminado correctamente")

            mock_get_comment_with_id.assert_called_once_with(1)
            mock_delete_comment.assert_called_once_with(1)

        @patch.dict("os.environ", {"REGION_NAME": "us-east-2", "DATA_BASE": "movier-test"})
        def test_lambda_handler_missing_parameters(self):
            mock_body_without_parameters = {"body": json.dumps({})}
            result = app.lambda_handler(mock_body_without_parameters, None)
            self.assertEqual(result['statusCode'], 400)
            body = json.loads(result['body'])
            self.assertIn("message", body)
            self.assertEqual(body["message"], "Falta el parámetro comment_id")

        @patch.dict("os.environ", {"REGION_NAME": "us-east-2", "DATA_BASE": "movier-test"})
        @patch("comments.delete_comment.app.get_comment_with_id")
        @patch("comments.delete_comment.app.delete_comment")
        @patch("pymysql.connect")
        def test_lambda_handler_comment_does_not_exist(self, mock_connect, mock_get_comment_with_id, mock_delete_comment):
            mock_connect.return_value = Mock()
            mock_get_comment_with_id.return_value = False
            mock_delete_comment.return_value = None

            mock_body_wrong_comment_id = {
                "body": json.dumps({
                    "user_id": 1,
                    "comment_id": 150
                })
            }
            result = app.lambda_handler(mock_body_wrong_comment_id, None)
            self.assertEqual(result['statusCode'], 404)
            body = json.loads(result['body'])
            self.assertIn("message", body)
            self.assertEqual(body["message"], "Comentario no encontrado")