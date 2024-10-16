import customtkinter as ctk
import os

changed_image = None
image = None
app = ctk.CTk()
app.title('Photo Editor')
app.geometry('800x700')
label = ctk.CTkLabel(app, text = '')
crop_x = None
crop_y = None
path_to_temp_image = os.path.abspath(__file__ + '/../../temp_image.png')
mutable_objects = {}