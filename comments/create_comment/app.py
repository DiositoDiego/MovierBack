import json
import pymysql

rds_host = "movier.cpiae0u0ckf8.us-east-1.rds.amazonaws.com"
rds_user = "MovierAdmin"
rds_password = "4dmin123"
rds_db = "movier"

headers_open = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,OPTIONS',
    }


def lambda_handler(event, context):
    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        user = body.get('user_id')
        movie = body.get('movie_id')
        comment = body.get('comment')

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers_open,
            'body': json.dumps(
                {'message': 'Error al obtener los parámetros del cuerpo de la solicitud', 'error': str(e)})
        }

    if user is None or movie is None or comment is None:
        return {
            'statusCode': 400,
            'headers': headers_open,
            'body': json.dumps({'message': 'Faltan parámetros'})
        }

    # Validaciones adicionales
    if not isinstance(user, int) or user <= 0:
        return {
            'statusCode': 400,
            'headers': headers_open,
            'body': json.dumps({'message': 'El ID del usuario debe ser un entero positivo'})
        }

    if not isinstance(movie, int) or movie <= 0:
        return {
            'statusCode': 400,
            'headers': headers_open,
            'body': json.dumps({'message': 'El ID de la película debe ser un entero positivo'})
        }

    if not isinstance(comment, str) or not comment.strip():
        return {
            'statusCode': 400,
            'headers': headers_open,
            'body': json.dumps({'message': 'El comentario no puede estar vacío'})
        }

    if len(comment) > 100:
        return {
            'statusCode': 400,
            'headers': headers_open,
            'body': json.dumps({'message': 'El comentario no puede exceder los 1000 caracteres'})
        }

    try:
        if not user_exists(user):
            return {
                'statusCode': 400,
                'headers': headers_open,
                'body': json.dumps({'message': 'El usuario no existe'})
            }
        if not movie_exists(movie):
            return {
                'statusCode': 400,
                'headers': headers_open,
                'body': json.dumps({'message': 'La película no existe'})
            }
        insert_into_comments(user, movie, comment)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers_open,
            'body': json.dumps({'message': 'Error al insertar el comentario en la base de datos', 'error': str(e)})
        }

        # Add CORS headers
    response = {
        'statusCode': 200,
        'headers': headers_open,
        'body': json.dumps({'message': 'Comentario insertado correctamente'}),

    }

    return response


def user_exists(user_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor() as cursor:
            check_query = "SELECT COUNT(*) FROM Users WHERE id = %s"
            cursor.execute(check_query, (user_id,))
            result = cursor.fetchone()
            return result[0] > 0
    finally:
        connection.close()


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


def insert_into_comments(user, movie, comment):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor() as cursor:
            insert_query = """
                INSERT INTO Comments (user_id, movie_id, comment, date) VALUES (%s, %s, %s, current_timestamp())
            """
            cursor.execute(insert_query, (user, movie, comment))
            connection.commit()
    finally:
        connection.close()
