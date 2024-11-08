import pyzbar.pyzbar as pyzbar
import cv2

def read_qr_from_file(file_path):
    img = cv2.imread(file_path)
    qr_data = decode_qr_from_frame(img)
    return qr_data

def decode_qr_from_frame(frame):
    decode = pyzbar.decode(frame)
    for i in decode:
        return i.data.decode('utf-8')
    return None
