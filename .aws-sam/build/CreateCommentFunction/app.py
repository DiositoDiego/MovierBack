import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"



def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user = body.get('user_id')
        movie = body.get('movie_id')
        comment = body.get('comment')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error al obtener los parámetros del cuerpo de la solicitud', 'error': str(e)})
        }

    if user is None or movie is None or comment is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Faltan parámetros'})
        }

    try:
        insert_into_comments(user, movie, comment)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al insertar el comentario en la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Película insertada correctamente'})
    }

def insert_into_comments(user, movie, comment):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            insert_query = """
                INSERT INTO Comments (user_id, movie_id, comment, date) VALUES (%s, %s, %s, %s, current_timestamp())
                """
            cursor.execute(insert_query, (user, movie, comment))
            connection.commit()
    finally:
        connection.close()