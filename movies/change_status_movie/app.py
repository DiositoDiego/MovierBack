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
        message = toggle_movie_status(movie_id)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(
                {'message': 'Error al actualizar el estado de la película en la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': message})
    }


def toggle_movie_status(movie_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            select_query = """
                SELECT status
                FROM Movies
                WHERE id = %s
            """
            cursor.execute(select_query, (movie_id,))
            result = cursor.fetchone()
            if result is None:
                raise Exception("La película no existe")

            current_status = result[0]
            new_status = 0 if current_status == 1 else 1

            update_query = """
                UPDATE Movies
                SET status = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (new_status, movie_id))
            connection.commit()

            status_message = "habilitada" if new_status == 1 else "deshabilitada"
            return f"Película {status_message} correctamente"
    finally:
        connection.close()
