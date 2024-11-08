import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qr_file_reader
# from qr_camera_reader import QRCameraReader  # Import mô-đun quét mã QR
from create_qrcode import generate_qr_code  # Import mô-đun tạo mã QR
import os
import subprocess


class QRCodeReaderApp:
    def __init__(self, root):
        self.root = root
        root.title("QR Code Reader")
        # self.qr_camera_reader = QRCameraReader()

        self.layout = tk.Frame(root)

        self.data_input = tk.Entry(self.layout)
        self.data_input.grid(row=0, column=0, padx=5, pady=5)

        self.generate_button = tk.Button(self.layout, text="Generate QR Code", command=self.generate_qr)
        self.generate_button.grid(row=0, column=1, padx=5, pady=5)

        self.camera_button = tk.Button(self.layout, text="Read QR from Camera", command=self.read_qr_from_camera_gui)
        self.camera_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.file_button = tk.Button(self.layout, text="Read QR from File", command=self.read_qr_from_file_gui)
        self.file_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.Diem_Danh_button = tk.Button(self.layout, text="Timekeeping using excel file", command=self.Diem_Danh_code)
        self.Diem_Danh_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.qr_label = tk.Label(self.layout) # Thêm qr_label là một thuộc tính
        self.qr_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.result_entry = tk.Entry(self.layout, width=50)  # Thêm result_entry là một thuộc tính
        self.result_entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.layout.pack()

    def Diem_Danh_code(self):
        # Thay đổi đường dẫn đến main.py tại đây
        main_path = "Diem_danh/main.py"

        # Mở file main.py bằng cách gọi subprocess
        subprocess.Popen(["python", main_path])

    def generate_qr(self):
        data = self.data_input.get()
        if data:
            file_path = "qrcode.png"  # Tên file cho mã QR được lưu
            generate_qr_code(data, file_path)
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            self.qr_label.config(image=photo)
            self.qr_label.image = photo

            # Hiển thị hộp thoại xác nhận lưu file
            reply = messagebox.askquestion("Save QR Code", "Do you want to save the QR Code?")
            if reply == 'yes':
                file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", ".png"), ("All Files", ".*")])
                if file_name:
                    os.replace(file_path, file_name)
                    messagebox.showinfo("Saved", "QR Code saved successfully!")
                else:
                    os.remove(file_path)
            else:
                os.remove(file_path)  # Xóa file nếu người dùng chọn "No"

    def read_qr_from_camera_gui(self):
        self.result_entry.delete(0, tk.END)  # Xóa nội dung cũ trước khi hiển thị mới
        self.result_entry.config(state='normal')  # Cho phép chỉnh sửa

        self.result_entry.insert(0, "Scanning QR code from camera...")

        def qr_callback(qr_data):
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, qr_data)
            self.result_entry.config(state='readonly')  # Không cho phép chỉnh sửa

        self.qr_camera_reader.start_camera()
        self.qr_camera_reader.qr_callback = qr_callback

    def read_qr_from_file_gui(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), ("All files", ".")])
        if file_path:
            self.result_entry.delete(0, tk.END)  # Xóa nội dung cũ trước khi hiển thị mới
            self.result_entry.config(state='normal')  # Cho phép chỉnh sửa

            self.result_entry.insert(0, f"Scanning QR code from file: {file_path}")
            qr_data = qr_file_reader.read_qr_from_file(file_path)  # Assume qr_file_reader module has this function

            if qr_data:
                self.result_entry.delete(0, tk.END)
                self.result_entry.insert(0, qr_data)
            else:
                self.result_entry.delete(0, tk.END)
                self.result_entry.insert(0, "No QR code found in the image.")
            
            self.result_entry.config(state='readonly')  # Không cho phép chỉnh sửa
            
if __name__=="__main__":
    m = tk.Tk()
    window = QRCodeReaderApp(m)
    m.mainloop()