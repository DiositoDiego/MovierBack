import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body.get('user_id')
        movie_id = body.get('movie_id')

        if not user_id or not movie_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Faltan user_id o movie_id en el cuerpo de la solicitud'})
            }

        if not user_exists(user_id):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'El usuario no existe'})
            }

        if not movie_exists(movie_id):
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'La película no existe'})
            }

        mark_movie_as_watched(user_id, movie_id)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al marcar la película como vista en la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Película marcada como vista con éxito'})
    }

def user_exists(user_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor() as cursor:
            query = "SELECT 1 FROM Users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return True
            return False
    finally:
        connection.close()

def movie_exists(movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor() as cursor:
            query = "SELECT 1 FROM Movies WHERE id = %s"
            cursor.execute(query, (movie_id,))
            result = cursor.fetchone()
            if result:
                return True
            return False
    finally:
        connection.close()

def mark_movie_as_watched(user_id, movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO WatchedMovies (user_id, movie_id, status)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """
            cursor.execute(query, (user_id, movie_id))
            connection.commit()
    finally:
        connection.close()
