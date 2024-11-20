import cv2  # Import thư viện OpenCV để xử lý ảnh và video
from decode import decode_img  # Import hàm decode_img từ module decode
import tkinter as tk  # Import thư viện tkinter để tạo giao diện người dùng
from tkinter import filedialog  # Import hàm filedialog từ thư viện tkinter

def select_file():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc của tkinter
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])  # Hiển thị cửa sổ chọn file
    return file_path

def check_Attendance(excel_file):
    cap = cv2.VideoCapture(0)  # Mở kết nối với camera, số 0 là ID của camera mặc định
    cap.set(3, 640)  # Thiết lập chiều rộng frame
    cap.set(4, 480)  # Thiết lập chiều cao frame

    marked = False  # Biến cờ để theo dõi đã đánh dấu 'X' hay chưa

    while cap.isOpened() and not marked:
        success, img = cap.read()  # Đọc frame từ camera
        if success:
            decode_img(img, excel_file)  # Gọi hàm decode_img từ module decode để xử lý ảnh
            cv2.imshow("decode", img)  # Hiển thị frame đã xử lý
            if cv2.waitKey(25) & 0xFF == 27:  # Chờ phím nhấn, nếu nhấn 'ESC' thì thoát
                break
        else:
            break

    cap.release()  # Giải phóng camera
    cv2.destroyAllWindows()  # Đóng tất cả cửa sổ hiển thị

if __name__ == '__main__':
    attendance_file = select_file()  # Sử dụng hàm select_file để chọn file điểm danh
    if attendance_file:  # Kiểm tra xem người dùng đã chọn file hay chưa
        check_Attendance(attendance_file)  # Nếu có file, thì gọi hàm check_Attendance để điểm danh
    else:
        print("Không chọn file.")  # Thông báo nếu không có file được chọn
