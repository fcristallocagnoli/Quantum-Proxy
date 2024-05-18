import smtplib
import ssl
from email.message import EmailMessage
import textwrap

from dotenv import dotenv_values

env = dotenv_values()

EMAIL_SENDER = env["EMAIL_SENDER"]
APP_PASSWORD = env["APP_PASSWORD"]
PERSONAL_EMAIL = env["PERSONAL_EMAIL"]
PROFESSIONAL_EMAIL = env["PROFESSIONAL_EMAIL"]

CONTACT_EMAILS = [PERSONAL_EMAIL, PROFESSIONAL_EMAIL]


def create_email(
    *,
    sender: str = f"QuantumProxy App <{EMAIL_SENDER}>",
    receivers: set[str] = None,
    subject: str,
    body: str,
    html: str = None,
) -> EmailMessage:
    """
    Crear un mensaje de correo electrónico personalizado.

    Parámetros:
    sender (str, optional): El remitente del correo electrónico en el formato.
    receivers (list): Una lista de direcciones de correo electrónico de los destinatarios.
    subject (str): El asunto del correo electrónico.
    body (str): El cuerpo del correo electrónico.

    Retorna:
    EmailMessage: El mensaje de correo electrónico creado.
    """
    if receivers is None:
        receivers = CONTACT_EMAILS
    else:
        receivers.union(CONTACT_EMAILS)
    # Crear un nuevo mensaje de correo electrónico
    msg = EmailMessage()

    # Establecer el remitente, los destinatarios, el asunto y el cuerpo del correo electrónico
    msg["From"] = sender
    msg["To"] = list(receivers)
    msg["Subject"] = subject

    footer = textwrap.dedent(
        """\n
    ----------------------------------------------
    This is an auto-generated email. Please do not reply to this message.
    For enquiries, please contact us at fcristallocagnoli@gmail.com.
    """
    )
    body += footer
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")

    return msg


def send_email(
    msg: EmailMessage,
    credentials: tuple[str, str] = (EMAIL_SENDER, APP_PASSWORD),
    server: str = "smtp.gmail.com",
    port: int = 465,
):
    """
    Enviar un correo electrónico personalizado.

    Parámetros:
    msg (EmailMessage): El mensaje de correo electrónico a enviar.
    credentials (tuple[str, str], opcional): Las credenciales del remitente en formato (usuario, contraseña).
    server (str, opcional): El servidor SMTP a utilizar. Por defecto es 'smtp.gmail.com'.
    port (int, opcional): El puerto a utilizar para el servidor SMTP. Por defecto es 465.
    """

    # Crear un contexto SSL seguro
    context = ssl.create_default_context()
    # Extraer las credenciales del remitente (correo y contraseña de aplicación)
    sender, password = credentials

    # Enviar el correo electrónico
    with smtplib.SMTP_SSL(server, port, context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)


def error_mail(error: Exception, context: str = None):
    """
    Enviar un correo electrónico de error.

    Parámetros:
    error (Exception): El error que se produjo.
    """
    # Correo electrónico de errores
    if context:
        error = f"{context}\n{error}"
    msg = create_email(
        subject="Error in QuantumProxy App",
        body=f"An error occurred in the QuantumProxy App:\n\n{error}",
    )
    send_email(msg)


# [ ]: Limpiar el código, eliminar pruebas # [ ]
# Pruebas varias
def main():
    # Crear un mensaje de correo electrónico personalizado
    msg = create_email(
        receivers=PROFESSIONAL_EMAIL,
        subject="Test Email",
        body="This is a test email from QuantumProxy App.",
    )

    # Enviar el correo electrónico
    send_email(msg)
    # Mostrar el mensaje de correo electrónico
    print(msg)


if __name__ == "__main__":
    main()
