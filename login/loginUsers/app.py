import json
import boto3


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')

    # Extraer nombre de usuario y contraseña del evento
    username = event['username']
    password = event['password']
    client_id = '1dt0d74uhmc4h4uf77u596d5nq'

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId=client_id
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Inicio de sesión exitoso',
                'id_token': response['AuthenticationResult']['IdToken'],
                'access_token': response['AuthenticationResult']['AccessToken'],
                'refresh_token': response['AuthenticationResult']['RefreshToken']
            })
        }

    except client.exceptions.NotAuthorizedException:
        return {
            'statusCode': 401,
            'body': json.dumps({
                'message': 'Usuario o contraseña incorrectos'
            })
        }

    except client.exceptions.UserNotConfirmedException:
        return {
            'statusCode': 403,
            'body': json.dumps({
                'message': 'Usuario no confirmado'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error en el servidor',
                'error': str(e)
            })
        }
