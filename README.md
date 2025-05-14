# 📡 Stock Alert System Using Serverless Architecture

Questo progetto mostra come costruire un semplice sistema cloud-native per monitorare le quantità di referenze in un inventario e ricevere **notifiche via SMS** in tempo reale 
quando i valori scendono sotto soglia, utilizzando esclusivamente **servizi AWS gestiti**.

---

## ☁️ Architettura
![Architettura]([https://raw.githubusercontent.com/alessaless/Stock-Alert-System-Using-Serverless-Architecture/master/architecture/architecture.png](https://github.com/alessaless/Stock-Alert-System-Using-Serverless-Architecture/blob/master/architecture/architecture.png?raw=true))


---

## 🔧 Servizi AWS utilizzati

| Servizio         | Funzione                                                                 |
|------------------|--------------------------------------------------------------------------|
| **AWS Lambda**   | Funzione serverless che analizza le referenze ordinate                   |
| **Amazon DynamoDB** | Database NoSQL contenente id referenza, quantità e soglia                 |
| **Amazon SNS**   | Servizio di notifica utilizzato per inviare SMS in caso di scorte basse  |
| **Amazon API Gateway** | Espone la funzione Lambda come endpoint HTTP per l'invocazione diretta     |
| **IAM**          | Gestione dei permessi per Lambda (accesso a DynamoDB e SNS)              |

---

## ⚙️ Come funziona

1. Una **chiamata HTTP POST** invoca la funzione Lambda tramite API Gateway, con una lista di referenze ordinate.
2. La Lambda interroga **DynamoDB** per ciascuna referenza.
3. Se la `quantita` di una referenza è **inferiore alla `soglia`**, viene pubblicato un messaggio su **Amazon SNS**.
4. SNS invia un **SMS al numero configurato** tramite variabili d’ambiente.

---

## 🔐 Permessi necessari
La funzione Lambda deve avere allegata una IAM role con queste policy:

- `AmazonDynamoDBReadOnlyAccess`
- `AmazonSNSFullAccess`

Inoltre è necessario settare la variabile d'ambiente `DESTINATARIO_SMS` della lambda direttamente sulla console AWS in Console Lambda > Configuration > Environment variables

---

## 🧪 Esempio di payload

```json
{
  "referenze": [
    { "id": "REF001", "quantita": 2 },
    { "id": "REF002", "quantita": 1 }
  ]
}
