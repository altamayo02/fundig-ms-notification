from enum import Enum

# Template bodies are defined in _set_body(fields),
# making use of the incoming fields
class Templates(Enum):
	TWOFACTOR = ["pin"]
	PWRESET = ["url"]
	
class Notification:
	REQUIRED_FIELDS = ["to"]

	def __init__(self, fields: list) -> None:
		self.template = None
		self.subject = ""
		self.body = ""

		self.status_code = 200
		self.response = {
			'message': "E-mail sent successfully."
		}

		# TODO - Structure of templateless JSON (client must give a body)
		try:
			self.template = Templates[fields["template"]]
		except:
			self.response = {
				'message': "Invalid notification template.",
				'available_templates': [template.name for template in Templates]
			}
			self.status_code = 400
			return
		
		if not all(field in fields for field in Notification.REQUIRED_FIELDS + self.template.value):
			self.response = {
				'message': "Missing required fields.",
				'required_fields': Notification.REQUIRED_FIELDS + self.template.value,
				'received_fields': fields
			}
			self.status_code = 400
			return
		
		self._set_body(fields)
		if fields["subject"]: self.subject = fields["subject"]
	
	def get_template(self) -> Templates:
		return self.template

	def get_subject(self) -> str:
		return self.subject
	
	def get_body(self) -> str:
		return self.body
	
	def get_status_code(self) -> int:
		return self.status_code

	def get_response(self) -> dict[str, any]:
		return self.response
	
	def _set_body(self, fields) -> None:
		if self.template == Templates.TWOFACTOR:
			self.body = f"""
				<html>
					<p>Su código de verificación es: {fields["pin"]}</p>
				</html>
			"""
			self.subject = "Nuevo intento de inicio de sesión"
		elif self.template == Templates.PWRESET:
			self.body = f"""
				<html>
					<p>Haga clic en el siguiente link para reestablecer su contraseña:</p>
					<p>{fields["url"]}</p>
				</html>
			"""
			self.subject = "Reestablecimiento de contraseña"