import qrcode
from PIL import Image

# Pedir al usuario que ingrese un enlace
link = input("Ingresa el enlace para generar el QR: ")

# Crear el código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(link)
qr.make(fit=True)

# Generar la imagen del QR
img = qr.make_image(fill='black', back_color='white')

# Guardar la imagen como archivo
img.save("qr_code.png")

# Abrir la imagen del QR generado
image = Image.open("qr_code.png")
image.show()  # Opcional, para mostrar la imagen del QR
