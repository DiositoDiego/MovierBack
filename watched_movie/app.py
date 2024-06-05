import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body.get('user_id')
    movie_id = body.get('movie_id')

    if not user_id or not movie_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Faltan user_id o movie_id en el cuerpo de la solicitud'})
        }

    try:
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

def mark_movie_as_watched(user_id, movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO WatchedMovies (user_id, movie_id, status)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """
            cursor.execute(query, (user_id, movie_id, 1))
            connection.commit()
    finally:
        connection.close()
