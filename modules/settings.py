import customtkinter as ctk
import os


changed_image = None
image = None
app = ctk.CTk()
app.title('Photo Editor')
app.geometry('800x780')
frame_main = ctk.CTkFrame(app, width = 800, height = 780, fg_color = '#959595', corner_radius = 0)
frame_main.place(x = 0, y = 0)
frame_image = ctk.CTkFrame(frame_main, width = 726, height = 680, fg_color = '#D9D9D9', corner_radius = 0)
frame_image.place(x = 73, y = 58)
label = ctk.CTkLabel(frame_main, 726, 680, text = '')
crop_x = None
crop_y = None
path_to_temp_image = os.path.abspath(__file__ + '/../../temp_image.png')
mutable_objects = {}
path_to_images = os.path.abspath(__file__ + '/../../images')