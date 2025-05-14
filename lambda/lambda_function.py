import boto3
import os

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    body = event.get('body')
    
    if isinstance(body, str):
        import json
        body = json.loads(body)
    
    referenze_da_controllare = body.get('referenze', [])

    table = dynamodb.Table('Magazzino')
    
    for ref_id in referenze_da_controllare:
        response = table.get_item(Key={'id': ref_id})
        item = response.get('Item')

        if item:
            quantita = int(item.get('quantita', 0))
            soglia = int(item.get('soglia', 0))

            if quantita < soglia:
                message = f"⚠️ Referenza {ref_id} ha quantità {quantita} sotto la soglia {soglia}"
                sns.publish(
                    PhoneNumber=os.environ['DESTINATARIO_SMS'],
                    Message=message
                )

    return {
        "statusCode": 200,
        "body": "Controllo completato"
    }
