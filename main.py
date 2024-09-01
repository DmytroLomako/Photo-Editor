import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

changed_image = None
app = ctk.CTk()
app.title('Photo Editor')
app.geometry('600x500')
label = ctk.CTkLabel(app, text = '')
def show_image(image):
    image_display = image.resize((300, 300))
    image = ImageTk.PhotoImage(image_display)
    label.configure(image = image)
    label.image = image
def upload_image():
    global changed_image
    file_path = ctk.filedialog.askopenfilename(filetypes = [('PNG', '*.png'), ('JPEG', '*.jpeg')])
    if file_path:
        image = Image.open(file_path)
        changed_image = image.copy()
        show_image(image)
        label.pack(pady = 30)
        slider_bright.set(1)
def rotate_image():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.rotate(90)
        show_image(changed_image)
def save_image():
    global changed_image
    if changed_image != None:
        path_save = ctk.filedialog.asksaveasfilename(defaultextension = '.png', filetypes = [('PNG', '*.png'), ('JPEG', '*.jpeg')])
        if path_save:
            changed_image.save(path_save)
def bw_image():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.convert('L')
        show_image(changed_image)
def blur_image():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.filter(ImageFilter.BLUR)
        show_image(changed_image)
def brightness_image(value):
    global changed_image
    if changed_image != None:
        bright = ImageEnhance.Brightness(changed_image)
        changed_image = bright.enhance(value)
        show_image(changed_image)
def contrast_image(value):
    global changed_image
    if changed_image != None:
        contrast = ImageEnhance.Contrast(changed_image)
        changed_image = contrast.enhance(value)
        show_image(changed_image)
frame = ctk.CTkFrame(app)
button = ctk.CTkButton(frame, text = 'Завантажити зображення', command = upload_image)
button_download = ctk.CTkButton(frame, text = 'Зберегти', command = save_image)
frame.pack(pady = 20)
button.pack(pady = 5)
button_download.pack(pady = 5)
button_rotate = ctk.CTkButton(app, text = 'Повернути', command = rotate_image)
button_rotate.place(x = 450, y = 20)
button_bw = ctk.CTkButton(app, text = 'Ч/б', command = bw_image)
button_bw.place(x = 450, y = 60)
button_blur = ctk.CTkButton(app, text = 'Заблюрить', command = blur_image)
button_blur.place(x = 450, y = 100)
label_bright = ctk.CTkLabel(app, text = 'Осветлить')
label_bright.place(x = 70, y = 15)
slider_bright = ctk.CTkSlider(app, from_ = 0.9, to = 1.1, command = brightness_image)
slider_bright.place(x = 5, y = 50)
label_contrast = ctk.CTkLabel(app, text = 'Контраст')
label_contrast.place(x = 75, y = 90)
slider_bright = ctk.CTkSlider(app, from_ = 0, to = 2, command = contrast_image)
slider_bright.place(x = 5, y = 125)

app.mainloop()