import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
import re
import json

#データファイル,フォルダ
data_json = "image_converter_data.json"

cd = open(data_json, 'r')
converter_data = json.load(cd)
cd.close()

class ui_window(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        #window情報
        self.master.title("Image Converter By Syulis")
        self.master.geometry("650x230")

        #タブ
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        #ファイルタブ
        menu_file = tk.Menu(self.master)
        menu.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Open", command=self.file_open, activebackground="blue")

        #オープンラベル
        self.open_file = converter_data["open_file"]
        self.open_file_var = tk.StringVar()
        self.open_file_var.set(self.open_file)
        open_file_label = tk.Label(textvariable=self.open_file_var)
        open_file_label.place(x=5, y=5)

        #リネーム窓
        self.rename_box = tk.Entry(width=20, font=("Meiryo", "10"))
        self.rename_box.place(x=10, y=30)
        self.rename_box.delete(0, tk.END)
        self.rename_box.insert(tk.END, "Rename")

        #変換ラジオボタン
        self.radiobutton_var = tk.IntVar()
        self.radiobutton_var.set(0)

        png = tk.Radiobutton(value=0, variable=self.radiobutton_var, text="png")
        png.place(x=200, y=30)

        PNG = tk.Radiobutton(value=1, variable=self.radiobutton_var, text="PNG")
        PNG.place(x=285, y=30)

        jpg = tk.Radiobutton(value=2, variable=self.radiobutton_var, text="jpg")
        jpg.place(x=200, y=70)

        JPG = tk.Radiobutton(value=3, variable=self.radiobutton_var, text="JPG")
        JPG.place(x=285, y=70)

        jpeg = tk.Radiobutton(value=4, variable=self.radiobutton_var, text="jpeg")
        jpeg.place(x=200, y=110)

        JPEG = tk.Radiobutton(value=5, variable=self.radiobutton_var, text="JPEG")
        JPEG.place(x=285, y=110)

        bmp = tk.Radiobutton(value=6, variable=self.radiobutton_var, text="bmp")
        bmp.place(x=200, y=150)

        BMP = tk.Radiobutton(value=7, variable=self.radiobutton_var, text="BMP")
        BMP.place(x=285, y=150)

        gif = tk.Radiobutton(value=8, variable=self.radiobutton_var, text="gif")
        gif.place(x=200, y=190)

        GIF = tk.Radiobutton(value=9, variable=self.radiobutton_var, text="GIF")
        GIF.place(x=285, y=190)

        #元データ削除
        delete_old_data_label = tk.Label(text="元データを削除")
        delete_old_data_label.place(x=10, y=110)
        self.delete_old_data_var = tk.IntVar()
        self.delete_old_data_var.set(0)

        delete_old_data_t = tk.Radiobutton(value=1, variable=self.delete_old_data_var, text="する")
        delete_old_data_t.place(x=90, y=100)

        delete_old_data_f = tk.Radiobutton(value=0, variable=self.delete_old_data_var, text="しない")
        delete_old_data_f.place(x=90, y=120)

        #実行ボタン
        execution_button = tk.Button(text="Execution")
        execution_button.place(x=362.5, y=30)
        execution_button.bind('<1>', self.execution)

        #ログ箱
        self.log_box = tk.Entry(width=16, font=("Meiryo", "10"))
        self.log_box.place(x=505, y=30)
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "Log")

        #終了ボタン
        end_button = tk.Button(text="End")
        end_button.place(x=450, y=30)
        end_button.bind('<1>', self.end)

        #バージョン等
        version_label = tk.Label(text="Image Converter By Syulis Ver.1.0")
        version_label.place(x=460, y=210)

        self.file_open()

    #ファイルオープン
    def file_open(self):
        try:
            fld = filedialog.askopenfilenames(initialdir=converter_data["open_file"])
            converter_data["open_file"] = fld[0]
            converter_data["dir"] = os.path.dirname(converter_data["open_file"])
            self.open_file = converter_data["open_file"]
            self.open_file_var.set(self.open_file)
            self.rename_box.delete(0, tk.END)
            self.rename_box.insert(tk.END, os.path.splitext(os.path.basename(self.open_file))[0])
            self.put_log("green", "Loaded")
        except:
            self.put_log("red", "Load Error")

    #実行
    def execution(self, event):
        try:
            img = Image.open(self.open_file)
            extension = None
            extension_jpeg = None
            if self.radiobutton_var.get() == 0:
                extension = "png"
            elif self.radiobutton_var.get() == 1:
                extension = "PNG"
            elif self.radiobutton_var.get() == 2:
                extension = "jpg"
                extension_jpeg = "jpeg"
            elif self.radiobutton_var.get() == 3:
                extension = "JPG"
                extension_jpeg = "JPEG"
            elif self.radiobutton_var.get() == 4:
                extension = "jpeg"
            elif self.radiobutton_var.get() == 5:
                extension = "JPEG"
            elif self.radiobutton_var.get() == 6:
                extension = "bmp"
            elif self.radiobutton_var.get() == 7:
                extension = "BMP"
            elif self.radiobutton_var.get() == 8:
                extension = "gif"
            elif self.radiobutton_var.get() == 9:
                extension = "GIF"
            else:
                self.put_log("red", "Extension Error")
                return

            if os.path.exists(converter_data["dir"] + "/" + self.rename_box.get() + "." + extension):
                self.put_log("red", "Already Exists Error")
                return

            if not extension_jpeg:
                img.save(converter_data["dir"] + "/" + self.rename_box.get() + "." + extension, extension, quality=100)
            else:
                img.save(converter_data["dir"] + "/" + self.rename_box.get() + "." + extension, extension_jpeg, quality=100)

            if self.delete_old_data_var.get() == 1:
                os.remove(self.open_file)
                self.open_file = converter_data["dir"] + "/" + self.rename_box.get() + "." + extension

            self.put_log("blue", "Done")

        except:
            self.put_log("red", "Image File Error")

    #ログ
    def put_log(self, color, text):
        self.log_box.delete(0, tk.END)
        self.log_box.configure(fg=color)
        self.log_box.insert(tk.END, text)

    #終了
    def end(self, event):
        with open(data_json, 'w') as f:
            json.dump(converter_data, f, indent=3)
        self.master.destroy()

if __name__ == '__main__':
    f = ui_window(None)
    f.pack()
    f.mainloop()