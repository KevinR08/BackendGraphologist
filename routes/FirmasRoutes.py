from flask import Blueprint, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from concurrent.futures import ThreadPoolExecutor, as_completed
import json


app = Blueprint('firmas_blueprint', __name__)


credenciales = {
    "type": "service_account",
    "project_id": "graphology-416322",
    "private_key_id": "bb3039acb02ce3e329e41f5b5e0261c5bc755af0",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCHEwvjzGmI1LWw\nJXq5hJfMTlQjuoJTPr9Six/EWzOcSkevWEvpYTj2MD5N+RyQo8EkdyREzM7Z20ZP\nr+S5mUKqgyDkXeVpsP1Laz63ZEPjS7bS/lZikVaQe/Y3MnLaEEeeebEmHHMQiETz\nkA10j1YQagE3nKjV9+9lq6KB0nreawkN+0yNqRTNY3fXC4OzvCPWiWntxpP6g/gO\nEUYw+y0MR+D+72iZZHFQBCaOKOFbcNLY4lvPO/oGFLI70eskGCoHmVcrm6eJk6m+\nVkEUmsaKUT7TTouzL10+n1RI7bTLtqaTYgQGOd+CxUdBW0y3NrEY187H/esu9cws\ntd2NrIjFAgMBAAECggEAIXw2hpyybe4jc307GRoWgprJb4kJTWdBCU69i5E7cGuW\nrVCjkwHb2+Y2T+CpdO7vjuFtT5QBVI8wNUmK13r3xKsYwJxJZuPuSx/VTqPv0319\n330XP7y9e7iLX4Alaks+YfpTkPndCZRqmYHU4Bg3kv6geh+fWFnsUmVT9kCOXqxI\nfuPKF0gAbKRAopexb3bCL+YffwIRmpW/AUsDO7Ky4JMp+Gbacr/TbHQ15reO3NRe\neN+boQkooB5QLpYYm2D17t654OZYwM7O+VPcOcCshgjU7wA9ca/TLZ9p2hEtKQ/X\nnqk88lUYF8jptyo7OqjHtmFsiueR2zpHi5ZtGn3f6QKBgQC86kK6C4lvMvAehsBg\nm3ScXfIQiy5pnnUW6jWDEDwhE48ZLbKp0vVrT2Dfd6GixMNrJYoSfJS8yw4B170w\nRDB88bqIZ+sMefltRsFVZLMvCANdCOZWvqX8guNU+7Joo2uoVJhCpv4M6AA4yGc/\neyHHkOCf4a5ILdGcjd3iuDgRXQKBgQC3Ckff5tA1bE2ta0eym2r75qYhgTucbQ/y\nEQBARkjSIZZAlvmBLOu2tnq0qMwV5t911rHGOO3sKxO7KJMA5izaMEXKn02sSOvp\nfxq3Z1RapfPo+HlN1zJhtQhB8jsHrHlzJXkI1TOlXj47Vdn8wzGgn/kfXa8v3wuF\notapPc5WiQKBgBBaUuZZ406t4R0zWunB6ykx9Kc79QuNfOM76N/sgtf2Infyfbm3\nmijs2Rze9S3qzGO0/yu0fweMqCy+qRDJhkz6e8QdArq0wEOWUVv7+IrErc3a3F17\n6VBfYCBWHU5zfvk2QWvbmrgxSPuhVVaoaPcmcltEpNp4pOFhYmiiu6+9AoGAfuH7\njPQ9ZKsc9ZgmbWNbOB9dDmC9Z+QaZ5ztZaDTHgb2VvPRJYB0LYY1bUKNpqkSQmd/\neH9CPrJlzRmFPdxRPzazSpA/kaxDDOt1I6nXSbc8a0TDIfiJDj4l6UD3NoyS7AUP\n79WLJZk83njW0Wal4kjCssGIjVC6dfq5fzw+6rECgYEAtQDuXmWBb+OYq7Onj1I2\nIHUKuAv5o7tofJdVQP/xEYzwKlE0qS/DvBrRrkmBHkZLX9u8gyT692tJTrHQkgw5\n50I4q96FEr3B0qNMXUuluZLS195eMNKiu3lTv4v3YzWLVpDHIghf4MxeETPyzYZ3\nxdjKvggWqHttXncX5T04a10=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-8squh@graphology-416322.iam.gserviceaccount.com",
    "client_id": "106805576176548646621",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-8squh%40graphology-416322.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(credenciales)
firebase_admin.initialize_app(cred)
db = firestore.client()

def holaa():
    return "holaA";

def obtener_usuarios():
    try:
        usuarios_ref = db.collection('users')
        documentos = usuarios_ref.stream()

        registros = {}

        for doc in documentos:
            uid = doc.id
            datos = doc.to_dict()
            print(datos)
            registros[uid] = datos

        return registros

    except Exception as e:
        return None

@app.route('/datos', methods=['GET'])
def datos_usuario():
    try:
        uid = request.args.get('uid')

        usuarios = obtener_usuarios()
        
        if usuarios is None:
            return jsonify({'ERROR': 'FALLA AL LEER LOS DATOS DEL USUARIO'}), 500

        if uid is None or uid not in usuarios:
            return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 500
        
        user = usuarios[uid]

        personalidades = {
            p["predicted_class"].upper(): f"{p['probability'] * 100:.2f}%"
            for p in json.loads(user["personality"])['probabilities']
        }
        
        sexualidades = {
            key.upper(): f"{value * 100:.2f}%"
            for key, value in json.loads(user["sexuality"])['probabilities'].items()
        }

        user['personalidades'] = personalidades
        user['sexualidades'] = sexualidades
        return jsonify({str(uid) : user}), 200

    except Exception as e:
        return jsonify({'ERROR': 'FALLA AL ENVIAR LA SOLICITUD'}), 500


@app.route('/predict', methods=['POST'])
def predecir_compatibilidad():
    try:
        datos = request.get_json()
        uid = datos.get('uid')

        usuarios = obtener_usuarios()
        
        if usuarios is None:
            return jsonify({'ERROR': 'FALLA AL DETERMINAR SU MATCH'}), 500

        if uid is None or uid not in usuarios:
            return jsonify({'ERROR': 'USUARIO INEXISTENTE'}), 500

        usuario_actual = usuarios[uid]
        personalidad_match = usuario_actual['predictPersonality'].upper()
        sexualidad_match = usuario_actual['predictSexuality'].upper()
        signo_match = usuario_actual['sign'].upper()
        genero_actual = usuario_actual['genderUser'].lower()

        del usuarios[uid]

        user_match_uid = None
        reference_match_value = 0
        max_match_value = 0
        for u in usuarios:
            if all(clave in usuarios[u] for clave in ['predictPersonality', 'predictSexuality', 'sign', 'genderUser']):
                genero_posible_match = usuarios[u]['genderUser'].lower()

                # Verificar que sean géneros opuestos (por ejemplo, hombre-mujer)
                if (genero_actual == 'hombre' and genero_posible_match == 'mujer') or (genero_actual == 'mujer' and genero_posible_match == 'hombre'):
                    
                    # Calcular la compatibilidad
                    if usuarios[u]['predictPersonality'].upper() == personalidad_match:
                        reference_match_value += 8
                    if usuarios[u]['predictSexuality'].upper() == sexualidad_match:
                        reference_match_value += 1
                    if usuarios[u]['sign'].upper() == signo_match:
                        reference_match_value += 1

                    if max_match_value < reference_match_value:
                        user_match_uid = str(u)
                        max_match_value = reference_match_value
            
            reference_match_value = 0

        if user_match_uid is None:
            return jsonify({'match': 'AUN NO CONTAMOS CON EL REGISTRO DE UNA PAREJA ADECUADA PARA TI'}), 200

        user_match = usuarios[str(user_match_uid)]
        personalidades = {
            p["predicted_class"].upper(): f"{p['probability'] * 100:.2f}%"
            for p in json.loads(user_match["personality"])['probabilities']
        }
        
        sexualidades = {
            key.upper(): f"{value * 100:.2f}%"
            for key, value in json.loads(user_match["sexuality"])['probabilities'].items()
        }

        user_match['compatibilidad'] = f'{max_match_value * 10}%'
        return jsonify({'user_match' : user_match}), 200

    except Exception as e:
        return jsonify({'ERROR': 'FALLA AL ENVIAR LA SOLICITUD'}), 500
