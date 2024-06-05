import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"

def lambda_handler(event, context):
    try:
        comments = get_comments_with_status(1)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener los comentarios de la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'Comentarios': comments})
    }


def get_comments_with_status(status):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    comments = []

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT *
                FROM Comments
                WHERE movie_id = %s
                """
            cursor.execute(query, (status,))
            result = cursor.fetchall()
            for row in result:
                comment = {
                    'user_id': row[0],
                    'movie_id': row[1],
                    'comment': row[2],
                    'date': row[3],
                }
                comments.append(comment)
    finally:
        connection.close()

    return comments
