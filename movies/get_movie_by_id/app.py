import json
import pymysql
from utils import get_connection

headers_open = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,OPTIONS',
}

def lambda_handler(event, context):
    try:
        movie_id = event['pathParameters'].get('id')
        if not movie_id:
            raise ValueError("No se proporcionó el ID de la película")

        status = 1
        movie = get_movie_by_id(status, movie_id)
        if not movie:
            return {
                'statusCode': 404,
                'headers': headers_open,
                'body': json.dumps({'message': 'Película no encontrada'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers_open,
            'body': json.dumps({'message': 'Error al obtener la película de la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'headers': headers_open,
        'body': json.dumps({'Pelicula': movie})
    }

def get_movie_by_id(status, movie_id):
    connection = get_connection()
    movie = None

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, title, description, genre, image, status
                FROM Movies
                WHERE status = %s AND id = %s
                """
            cursor.execute(query, (status, movie_id))
            result = cursor.fetchone()
            if result:
                movie = {
                    'id': result[0],
                    'title': result[1],
                    'description': result[2],
                    'genre': result[3],
                    'image': result[4],
                    'status': result[5]
                }
    finally:
        connection.close()

    return movie
