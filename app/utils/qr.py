import qrcode

def generate_qr(link, filename):
    img = qrcode.make(link)
    img.save(filename)