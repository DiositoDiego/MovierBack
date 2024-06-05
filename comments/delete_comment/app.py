import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"


def lambda_handler(event, context):
    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        movie = body.get('comment_id')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(
                {'message': 'Error al obtener los parámetros del cuerpo de la solicitud', 'error': str(e)})
        }
    if not movie:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el parámetro comment_id'})
        }

    try:
        if movie <= 0:
            raise ValueError('El parámetro comment_id debe ser un entero positivo')
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }

    try:
        comment = int(movie)
        comments = get_comment_with_id(comment)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener los comentarios de la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'Comentarios': comments})
    }


def get_comment_with_id(comment_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    comments = []

    try:
        with connection.cursor() as cursor:
            query = """
                DELETE FROM Comments
                WHERE id = %s
                """
            cursor.execute(query, (comment_id,))
            connection.commit()
    finally:
        connection.close()

    return comments
