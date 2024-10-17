from .settings import app, ctk
from .functions import *


class MakeButton:
    def __init__(self, name, width, height, x, y, slider = None):
        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.slider = slider
        self.make_button()
    def make_button(self):
        path_to_image = f'{path_to_images}/{self.name}.png'
        button_img = ImageTk.PhotoImage(Image.open(path_to_image).resize((self.width, self.height)))
        self.button = ctk.CTkLabel(frame_main, image = button_img, text = '')
        self.button.place(x = self.x, y = self.y)
    def bind(self, func):
        self.button.bind('<Button-1>', func)
rotate = MakeButton('rotate', 61, 61, 6, 65)
rotate.bind(lambda event: rotate_func())
bw = MakeButton('bw', 61, 61, 6, 145)
bw.bind(lambda event: bw_func())
crop = MakeButton('crop', 61, 61, 6, 225)
crop.bind(lambda event: crop_func())
blur = MakeButton('blur', 61, 61, 6, 305)
blur.bind(lambda event: blur_func())
brightness = MakeButton('brightness', 61, 61, 6, 395)
brightness.bind(lambda event: open_slider('brightness'))
contrast = MakeButton('contrast', 51, 60, 11, 477)
contrast.bind(lambda event: open_slider('contrast'))
add_text = MakeButton('add_text', 61, 61, 6, 555)
add_text.bind(lambda event: open_text_modal(event))
watermark_remove = MakeButton('watermark', 61, 61, 6, 635)
watermark_remove.bind(lambda event: watermark_remove_func())
background_remove = MakeButton('background', 61, 61, 6, 715)
background_remove.bind(lambda event: background_remove_func())
upload_image = MakeButton('upload_image', 58, 58, 79, 0)
upload_image.bind(lambda event: upload_image_func())
upload_image_from_drive = MakeButton('drive_upload', 55, 49, 156, 4)
upload_image_from_drive.bind(lambda event: upload_image_from_drive_func())
frame_resolution = ctk.CTkFrame(frame_main, border_color = '#959595', bg_color = '#959595', fg_color = '#959595')
frame_resolution.place(x = 600, y = 740)
mutable_objects['entry_width'] = ctk.CTkEntry(frame_resolution, width = 70, fg_color = '#959595', font = ('Arial', 26), placeholder_text = '726', placeholder_text_color = 'black', text_color = 'black', border_color = '#959595', corner_radius = 0)
mutable_objects['entry_width'].grid(row = 0, column = 0)
x = ctk.CTkLabel(frame_resolution, text = 'x', font = ('Arial', 26), text_color = 'black', fg_color = '#959595', bg_color = '#959595')
x.grid(row = 0, column = 1)
mutable_objects['entry_height'] = ctk.CTkEntry(frame_resolution, fg_color = '#959595', font = ('Arial', 26), placeholder_text = '680', placeholder_text_color = 'black', text_color = 'black', border_color = '#959595', corner_radius = 0)
mutable_objects['entry_height'].grid(row = 0, column = 2)
save_image = MakeButton('download', 45, 45, 229, 5)
save_image.bind(lambda event: save_image_func(mutable_objects['entry_width'], mutable_objects['entry_height']))
save_image_to_drive = MakeButton('drive_save', 55, 49, 299, 4)
save_image_to_drive.bind(lambda event: open_drive_save_modal())
redo = MakeButton('redo', 58, 58, 736, 0)
redo.bind(lambda event: redo_changes())
undo = MakeButton('undo', 58, 58, 664, 0)
undo.bind(lambda event: undo_changes())