import os
from dotenv import load_dotenv

from azure.communication.email import EmailClient
from flask import Flask, request, jsonify, Response

from model.Notification import Notification, Templates


load_dotenv()
app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email() -> Response:
	data = request.json

	try:
		notification = Notification(data)
		if notification.get_status_code() // 100 != 2:
			return jsonify(notification.get_response())

		connection_string = os.environ.get("CONNECTION_STRING")
		client = EmailClient.from_connection_string(connection_string)
		message = {
			"senderAddress": os.environ.get("SENDER_ADDRESS"),
			"recipients": {
				"to": [
					{"address": data['to']}
				]
			},
			"content": {
				"subject": notification.get_subject(),
				"html": notification.get_body()
			}
		}

		poller = client.begin_send(message)
		result = poller.result()
		print(result)
	except Exception as ex:
		print("Exception occurred:")
		print(ex)
		return jsonify({
			'message': 'Exception occurred.',
		}), 500
	return jsonify(notification.get_response()), 200

if __name__ == '__main__':
	# Utiliza Waitress como servidor en lugar del servidor de desarrollo de Flask para producción
	"""
	from waitress import serve
	print("Server running!")
	serve(app, host='0.0.0.0', port=5000)
	"""
	app.run(debug=True)
	