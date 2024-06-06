import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"


def lambda_handler(event, context):
    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        comment_id = body.get('comment_id')
        user_id = body.get('user_id')
        print(comment_id)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(
                {'message': 'Error al obtener los parámetros del cuerpo de la solicitud', 'error': str(e)})
        }

    if not comment_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el parámetro comment_id'})
        }

    if not user_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Falta el parámetro user_id'})
        }

    try:
        comment_id = int(comment_id)
        if comment_id <= 0:
            raise ValueError('El parámetro comment_id debe ser un entero positivo')
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }

    try:
        user_id = int(user_id)
        if user_id <= 0:
            raise ValueError('El parámetro user_id debe ser un entero positivo')
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }

    try:
        comment = get_comment_with_id(comment_id)
        if not comment:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Comentario no encontrado'})
            }

        if comment['user_id'] != user_id:
            return {
                'statusCode': 403,
                'body': json.dumps({'message': 'Usuario no autorizado para eliminar este comentario'})
            }

        delete_comment(comment_id)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al procesar la solicitud', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Comentario eliminado exitosamente'})
    }


def get_comment_with_id(comment_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = "SELECT * FROM Comments WHERE id = %s"
            cursor.execute(query, (comment_id,))
            comment = cursor.fetchone()
    finally:
        connection.close()

    return comment


def delete_comment(comment_id):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Comments WHERE id = %s"
            cursor.execute(query, (comment_id,))
            connection.commit()
    finally:
        connection.close()
