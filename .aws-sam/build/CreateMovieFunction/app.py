import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"



def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        title = body.get('title')
        description = body.get('description')
        genre = body.get('genre')
        image = body.get('image')
        status = body.get('status')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error al obtener los parámetros del cuerpo de la solicitud', 'error': str(e)})
        }

    if title is None or description is None or genre is None or image is None or status is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Faltan parámetros'})
        }

    try:
        insert_into_movies(title, description, genre, image, status)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al insertar en la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Película insertada correctamente'})
    }

def insert_into_movies(title, description, genre, image, status):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)

    try:
        with connection.cursor() as cursor:
            insert_query = """
                INSERT INTO Movies (title, description, genre, image, status) VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(insert_query, (title, description, genre, image, status))
            connection.commit()
    finally:
        connection.close()