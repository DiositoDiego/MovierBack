import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"

def lambda_handler(event, context):
    try:
        movie_id = event['pathParameters'].get('id')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error al obtener el ID de la película', 'error': str(e)})
        }

    if movie_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el ID de la película'})
        }

    try:
        request_body = json.loads(event['body'])
        title = request_body.get('title')
        description = request_body.get('description')
        genre = request_body.get('genre')
        image = request_body.get('image')
        status = request_body.get('status')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error al obtener los datos de la película del cuerpo de la solicitud', 'error': str(e)})
        }

    if not any([title, description, genre, image, status]):
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Faltan campos a actualizar'})
        }

    try:
        update_movie(movie_id, title, description, genre, image, status)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al actualizar la película en la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Película actualizada correctamente'})
    }

def update_movie(movie_id, title, description, genre, image, status):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            update_query = """
                UPDATE Movies
                SET title = %s, description = %s, genre = %s, image = %s, status = %s
                WHERE id = %s
                """
            cursor.execute(update_query, (title, description, genre, image, status, movie_id))
            connection.commit()
    finally:
        connection.close()
