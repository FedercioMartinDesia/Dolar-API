import requests
from datetime import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def obtener_cotizacion_dolar_blue():
    # URL del endpoint para obtener la cotización del Dólar Blue
    url = 'https://dolarapi.com/v1/dolares/blue'

    try:

        response = requests.get(url)


        if response.status_code == 200:
            datos = response.json()


            compra = datos.get('compra')
            venta = datos.get('venta')


            fecha = datetime.now().strftime("%Y-%m-%d")

            return fecha, compra, venta
        else:
            print(f"Error: {response.status_code}")
            print("Error al leer la API")
            return None

    except Exception as e:
        print("Hubo un error")
        print(e)
        return None

def enviar_correo():
    resultado = obtener_cotizacion_dolar_blue()

    if resultado:
        fecha, compra, venta = resultado

        text_body = f"""
        Buen día,

        Esta es la cotización del dólar blue al {fecha}:

        Compra: ${compra}
        Venta: ${venta}

        Saludos
        """

        html_body = f"""
        <html>
        <body>
            <p>Buen día, esta es la cotización del dólar blue al {fecha}:</p>
            <ul>
                <li>Compra: ${compra}</li>
                <li>Venta: ${venta}</li>
            </ul>
            <p>Saludos,</p>
            <p>Federico</p>
        </body>
        </html>
        """

        sender_email = "mail emisor"
        receiver_email = "mail receptor"
        password = "contraseña"


        mi_mail = MIMEMultipart("alternative")
        mi_mail["From"] = sender_email
        mi_mail["To"] = receiver_email
        mi_mail["Subject"] = "Cotización del Dólar Blue"


        mi_mail.attach(MIMEText(text_body, "plain"))
        mi_mail.attach(MIMEText(html_body, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, mi_mail.as_string())

        print("El correo electrónico fue enviado correctamente.")

    else:
        print("No se pudo obtener la cotización del dólar blue.")

enviar_correo()
