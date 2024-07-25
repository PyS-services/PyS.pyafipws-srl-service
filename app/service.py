import os
import py_eureka_client.eureka_client as eureka_client

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from app.logger_setup import logger
from app.factura_electronica import facturar

load_dotenv()

production = True if os.getenv('PRODUCTION') == "TRUE" else False
eureka_port = int(os.getenv('EUREKA_PORT', 8761))

logger.info(f'production={production}/{os.getenv("PRODUCTION")}')

app = Flask(__name__)

eureka_client.init(eureka_server=f'http://eureka-service:{eureka_port}',
                   app_name='pyafipws-service',
                   instance_port=8281)

@app.route('/api/afipws/test', methods=['GET'])
def test():
    logger.info("test")
    return jsonify({"test": "ok"})

@app.route('/api/afipws/facturador', methods=['POST'])
def facturador():
    logger.info("facturando ...")
    try:
        # obtiene los datos JSON del cuerpo de la solicitud
        json_data = request.get_json()

        logger.info(f"json_data={json_data}")

        # Verifica si es un JSON válido
        if json_data is None:
            return jsonify({"error": "No se proporcionó un JSON válido"}), 400

        json_data = facturar(json_data, production=production)

        logger.info(f"json_data (after)={json_data}")

        return jsonify(json_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)