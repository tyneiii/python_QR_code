import cv2  # Import thư viện OpenCV để xử lý ảnh và video
import threading  # Import thư viện threading để thực hiện đọc dữ liệu từ camera ở nền
import pyzbar.pyzbar as pyzbar  # Import thư viện pyzbar để giải mã mã QR

class QRCameraReader:
    def __init__(self, qr_callback=None):
        # Khởi tạo đối tượng QRCameraReader
        self.camera_running = False  # Biến cờ để kiểm soát việc chạy camera
        self.cap = None  # Đối tượng capture từ camera
        self.qr_callback = qr_callback  # Callback function để xử lý dữ liệu QR

    def start_camera(self):
        # Bắt đầu chạy camera
        self.camera_running = True
        self.cap = cv2.VideoCapture(0)  # Kết nối với camera (số 0 là ID của camera mặc định)
        threading.Thread(target=self.read_qr_from_camera).start()  # Tạo thread để đọc mã QR từ camera

    def stop_camera(self):
        # Dừng camera
        self.camera_running = False
        if self.cap:
            self.cap.release()  # Giải phóng camera
            cv2.destroyAllWindows()  # Đóng tất cả cửa sổ hiển thị

    def read_qr_from_camera(self):
        # Hàm đọc mã QR từ camera
        while self.camera_running:  # Kiểm tra xem camera có đang chạy hay không
            ret, frame = self.cap.read()  # Đọc frame từ camera
            qr_data = self.decode_qr_from_frame(frame)  # Giải mã mã QR từ frame

            if qr_data:  # Nếu có dữ liệu từ mã QR
                self.stop_camera()  # Dừng camera
                if self.qr_callback:  # Nếu có callback function
                    self.qr_callback(qr_data)  # Gọi callback function để xử lý dữ liệu QR
                break

            cv2.imshow("QR Scanner", frame)  # Hiển thị frame camera

            if cv2.waitKey(1) & 0xFF == 27:  # Nếu nhấn 'ESC' thì dừng camera
                self.stop_camera()
                break

    def decode_qr_from_frame(self, frame):
        # Hàm giải mã mã QR từ frame
        decoded_objs = pyzbar.decode(frame, symbols=[pyzbar.ZBarSymbol.QRCODE])  # Giải mã QR từ frame
        for obj in decoded_objs:  # Duyệt qua các đối tượng đã giải mã được
            return obj.data.decode('utf-8')  # Trả về dữ liệu giải mã
        return None  # Nếu không có mã QR nào được tìm thấy, trả về None
