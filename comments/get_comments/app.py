import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"


def lambda_handler(event, context):
    try:
        movie = event['pathParameters'].get('id')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(
                {'message': 'Error al obtener los parámetros del cuerpo de la solicitud', 'error': str(e)})
        }
    if not movie:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el parámetro movie_id'})
        }

    try:
        movie = int(movie)
        if movie <= 0:
            raise ValueError('El parámetro movie_id debe ser un entero positivo')
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }

    try:
        if not movie_exists(movie):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'La película no existe'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al verificar la existencia de la película', 'error': str(e)})
        }

    try:
        movie = int(movie)
        comments = get_comments_with_movie_id(movie)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener los comentarios de la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'Comentarios': comments})
    }

def movie_exists(movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor() as cursor:
            check_query = "SELECT COUNT(*) FROM Movies WHERE id = %s"
            cursor.execute(check_query, (movie_id,))
            result = cursor.fetchone()
            return result[0] > 0
    finally:
        connection.close()


def get_comments_with_movie_id(movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    comments = []

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT *
                FROM Comments
                WHERE movie_id = %s
                """
            cursor.execute(query, (movie_id,))
            result = cursor.fetchall()
            for row in result:
                comment = {
                    'comment_id': row[0],
                    'user_id': row[1],
                    'movie_id': row[2],
                    'comment': row[3],
                    'date': row[4].strftime('%Y-%m-%d %H:%M:%S')
                }
                comments.append(comment)
    finally:
        connection.close()


    return comments
