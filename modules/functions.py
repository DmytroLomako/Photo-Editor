import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from .settings import *
import os

def show_image(image):
    image_display = image.resize((400, 400))
    image = ImageTk.PhotoImage(image_display)
    label.configure(image = image)
    label.image = image
def upload_image(slider_bright, entry_width, entry_height):
    global changed_image, image
    file_path = ctk.filedialog.askopenfilename(filetypes = [('PNG', '*.png'), ('JPEG', '*.jpeg')])
    if file_path:
        image = Image.open(file_path)
        changed_image = image.copy()
        show_image(image)
        label.pack(pady = 100)
        slider_bright.set(1)
        entry_width.insert(0, changed_image.width)
        entry_height.insert(0, changed_image.height)
def rotate_image():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.rotate(90)
        show_image(changed_image)
def save_image(entry_width, entry_height):
    global changed_image
    if changed_image != None:
        width_image = int(changed_image.width)
        height_image = int(changed_image.height)
        path_save = ctk.filedialog.asksaveasfilename(defaultextension = '.png', filetypes = [('PNG', '*.png'), ('JPEG', '*.jpeg')])
        if path_save:
            changed_image = changed_image.resize((int(entry_width.get()), int(entry_height.get())))
            changed_image.save(path_save)
            changed_image = changed_image.resize((width_image, height_image))
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
def undo_changes():
    global image, changed_image
    if image != None:
        changed_image = image
        show_image(changed_image)
def start_crop(event):
    global crop_x, crop_y
    crop_x = event.x
    crop_y = event.y
def end_crop(event):
    global crop_x, crop_y, changed_image
    if crop_x!= None and crop_y!= None:
        change_x = changed_image.width/400
        change_y = changed_image.height/400
        left = min(crop_x, event.x)
        right = max(crop_x, event.x)
        top = min(crop_y, event.y)
        bottom = max(crop_y, event.y)
        changed_image = changed_image.crop((left * change_x, top * change_y, right * change_x, bottom * change_y))
        show_image(changed_image)
        label.unbind('<Button-1>')
        label.unbind('<ButtonRelease-1>')
def crop():
    global changed_image
    if changed_image != None:
        label.bind('<Button-1>', start_crop)
        label.bind('<ButtonRelease-1>', end_crop)
def open_text_modal(event):
    global changed_image
    text_x = event.x
    text_y = event.y
    
    modal = ctk.CTkToplevel(app)
    modal.title('Add Text')
    modal.geometry('300x300')
    entry_text = ctk.CTkLabel(modal, text = 'enter text:')
    entry_text.pack(pady = 5)
    entry_input_text = ctk.CTkEntry(modal, 250)
    entry_input_text.pack(pady = 5)
    entry_size = ctk.CTkLabel(modal, text = 'enter size:')
    entry_size.pack(pady = 5)
    entry_input_size = ctk.CTkEntry(modal, 250)
    entry_input_size.pack(pady = 5)
    label_color = ctk.CTkLabel(modal, text = 'select color:')
    label_color.pack(pady = 5)
    options = ctk.CTkOptionMenu(modal, values = ['white', 'black'])
    options.pack(pady = 5)
    def add_text():
        global changed_image
        if changed_image != None:
            path = os.path.abspath(__file__ + '/../arial.ttf')
            draw = ImageDraw.Draw(changed_image)
            font = ImageFont.truetype(path, int(entry_input_size.get()))
            fill = (255, 255, 255)
            if options.get() == 'black':
                fill = (0, 0, 0)
            change_x = changed_image.width/400
            change_y = changed_image.height/400
            draw.text((text_x * change_x, text_y * change_y), entry_input_text.get(), font = font, fill = (255, 255, 255))
            show_image(changed_image)
            modal.destroy()
    button_send_text = ctk.CTkButton(modal, text = 'Apply', command = add_text)
    button_send_text.pack(pady = 5)