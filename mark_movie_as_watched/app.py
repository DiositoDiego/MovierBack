import json
import pymysql

# Configuración de la base de datos
rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"

def lambda_handler(event, context):
    try:
        # Obtener el ID de la película desde los parámetros del cuerpo de la solicitud
        body = json.loads(event['body'])
        movie_id = body.get('id')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error al obtener el ID de la película del cuerpo de la solicitud', 'error': str(e)})
        }

    if movie_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el ID de la película'})
        }

    try:
        # Marcar la película como vista
        mark_movie_as_watched(movie_id)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al marcar la película como vista en la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Película marcada como vista correctamente'})
    }

def mark_movie_as_watched(movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            # Actualizar el estado de la película a "watched" en la base de datos
            update_query = """
                UPDATE Movies
                SET status = 'watched'
                WHERE id = %s
                """
            cursor.execute(update_query, (movie_id,))
            connection.commit()
    finally:
        connection.close()
