import json
import pymysql

rds_host = "movier-test.czu8iscuyzfs.us-east-2.rds.amazonaws.com"
rds_user = "admin"
rds_password = "admin123"
rds_db = "movier"


def lambda_handler(event, context):
    try:
        movies = get_movies_with_status(1)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error al obtener las películas de la base de datos', 'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'Peliculas': movies})
    }


def get_movies_with_status(status):
    connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
    movies = []

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id,title, description, genere, image, status
                FROM Movies
                WHERE status = %s
                """
            cursor.execute(query, (status,))
            result = cursor.fetchall()
            for row in result:
                movie = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'genere': row[3],
                    'image': row[4],
                    'status': row[5]
                }
                movies.append(movie)
    finally:
        connection.close()

    return movies
