import customtkinter as ctk

changed_image = None
image = None
app = ctk.CTk()
app.title('Photo Editor')
app.geometry('800x700')
label = ctk.CTkLabel(app, text = '')
crop_x = None
crop_y = None