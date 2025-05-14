import boto3
import os

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    import json
    body = event.get('body')

    if isinstance(body, str):
        body = json.loads(body)

    referenze_da_ordinare = body.get('referenze', [])

    table = dynamodb.Table('Referenze')

    for ref in referenze_da_ordinare:
        ref_id = ref.get("id")
        q_ordinata = ref.get("quantita", 1)

        if not ref_id or not isinstance(q_ordinata, int):
            print(f"Input non valido: {ref}")
            continue

        try:
            response = table.update_item(
                Key={'id': ref_id},
                UpdateExpression="SET quantita = quantita - :dec",
                ExpressionAttributeValues={':dec': q_ordinata},
                ReturnValues="UPDATED_NEW"
            )

            nuova_quantita = int(response['Attributes']['quantita'])

            soglia_resp = table.get_item(Key={'id': ref_id})
            soglia = int(soglia_resp['Item'].get('soglia', 0))

            if nuova_quantita < soglia:
                message = f"⚠️ Referenza {ref_id} ha quantità {nuova_quantita} sotto la soglia {soglia}"
                sns.publish(
                    PhoneNumber=os.environ['DESTINATARIO_SMS'],
                    Message=message
                )
                print(f"SMS inviato per {ref_id}")
            else:
                print(f"{ref_id}: quantità aggiornata a {nuova_quantita} (soglia: {soglia})")

        except Exception as e:
            print(f"Errore durante l’elaborazione di {ref_id}: {str(e)}")

    return {
        "statusCode": 200,
        "body": "Ordine processato con quantità specifiche"
    }
