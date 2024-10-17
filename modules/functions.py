import io, numpy as np
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from .settings import *
from .google_drive import connection, list_images, MediaIoBaseDownload, MediaFileUpload
from rembg import remove 

list_changes = []
list_undo_changes = []
redo_changing = False
changing = False
file_path = None
def show_image(image):
    global list_changes, changing, redo_changing, list_undo_changes
    if not changing:
        list_changes.append(image)
    if redo_changing:
        list_undo_changes = []
        redo_changing = False
    changing = False
    image_display = image.resize((726, 680))
    image = ImageTk.PhotoImage(image_display)
    label.configure(image = image)
    label.image = image
def upload_image_func(image_path = None):
    global changed_image, image, file_path, list_changes
    if image_path == None:
        file_path = ctk.filedialog.askopenfilename(filetypes = [('PNG', '*.png'), ('JPEG', '*.jpeg'), ('WEBP', '*.webp'), ('JPG', '*.jpg')])
    else:
        file_path = image_path
    if file_path:
        image = Image.open(file_path)
        changed_image = image.copy()
        list_changes = []
        show_image(image)
        label.place(x = 73, y = 58)
        if 'slider' in mutable_objects.keys():
            mutable_objects['slider'].set(1)
        # mutable_objects['slider_contrast'].set(1)
        # mutable_objects['entry_width'].delete(0, 10)
        # mutable_objects['entry_height'].delete(0, 10)
        # mutable_objects['entry_width'].insert(0, changed_image.width)     
        # mutable_objects['entry_height'].insert(0, changed_image.height)
def select_drive_image(id):
    global service
    image = service.files().get_media(fileId = id)
    file = io.FileIO('temp_image.png', 'wb')
    downloader = MediaIoBaseDownload(file, image)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}.")
    upload_image_func(path_to_temp_image)
def upload_image_from_drive_func():
    global list_images, service
    service = connection()
    if list_images != []:
        modal_drive_image = ctk.CTkToplevel(frame_main)
        modal_drive_image.title('Select Image From Drive')
        modal_drive_image.geometry('500x400')
        frame_drive = ctk.CTkScrollableFrame(modal_drive_image, 450, 340)
        frame_drive.grid(row = 0, column = 0, padx = 20, pady = 20)
        class DriveButton:
            def __init__(self, text, id):
                self.text = text
                self.id = id
            def make_button(self):
                button = ctk.CTkButton(frame_drive, text = self.text, command = self.click)
                button.pack(pady = 5)
            def click(self):
                select_drive_image(self.id)
        for i in range(len(list_images)):
            button = DriveButton(list_images[i].split('%')[0], list_images[i].split('%')[1])
            button.make_button()
def open_drive_save_modal():
    global changed_image, service
    if changed_image != None:
        modal = ctk.CTkToplevel(frame_main)
        modal.title('Save Image To Drive')
        modal.geometry('300x250')
        entry_name = ctk.CTkLabel(modal, text = 'Enter image name')
        entry_name.pack(pady = 5)
        entry_input_name = ctk.CTkEntry(modal, 250)
        entry_input_name.pack(pady = 5)
        entry_extension = ctk.CTkLabel(modal, text = 'Choose image extension')
        entry_extension.pack(pady = 5)
        options = ctk.CTkOptionMenu(modal, values = ['png', 'jpeg', 'jpg', 'webp'])
        options.pack(pady = 5)
        def save_image_to_drive():
            global changed_image
            service = connection()
            name = entry_input_name.get()
            extension = options.get()
            changed_image.save(path_to_temp_image)
            file_data = {
                'name': f'{name}.{extension}'
            }
            data = MediaFileUpload(path_to_temp_image)
            file = service.files().create(body = file_data, media_body = data, fields = 'id').execute()
            modal.destroy()
        button_apply = ctk.CTkButton(modal, text = 'Apply',  command = lambda: save_image_to_drive())
        button_apply.pack(pady = 30)
def rotate_func():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.rotate(90)
        show_image(changed_image)
def save_image_func(entry_width = None, entry_height = None):
    global changed_image
    if changed_image != None:
        width_image = int(changed_image.width)
        height_image = int(changed_image.height)
        path_save = ctk.filedialog.asksaveasfilename(defaultextension = '.png', filetypes = [('PNG', '*.png'), ('JPEG', '*.jpeg')])
        if path_save:
            # changed_image = changed_image.resize((int(entry_width.get()), int(entry_height.get())))
            changed_image.save(path_save)
            changed_image = changed_image.resize((width_image, height_image))
def bw_func():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.convert('L')
        show_image(changed_image)
def blur_func():
    global changed_image
    if changed_image != None:
        changed_image = changed_image.filter(ImageFilter.BLUR)
        show_image(changed_image)
def brightness_func(value):
    global changed_image
    if changed_image != None:
        bright = ImageEnhance.Brightness(changed_image)
        changed_image = bright.enhance(value)
        show_image(changed_image)
def contrast_func(value):
    global changed_image
    if changed_image != None:
        contrast = ImageEnhance.Contrast(changed_image)
        changed_image = contrast.enhance(value)
        show_image(changed_image)
def open_slider(value):
    if changed_image != None:
        if 'text' in mutable_objects.keys():
            mutable_objects['text'].configure(text = '')
        if value == 'brightness':
            mutable_objects['slider'] = ctk.CTkSlider(app, from_ = 0.9, to = 1.1, command = brightness_func, bg_color = '#959595', fg_color = 'black', progress_color = '#001173', button_color = 'black')
            mutable_objects['text'] = ctk.CTkLabel(app, text = 'Brightness', font = ('Arial', 18), bg_color = '#959595', text_color = 'black')
            mutable_objects['text'].place(x = 458, y = 0)
        elif value == 'contrast':
            mutable_objects['slider'] = ctk.CTkSlider(app, from_ = 0, to = 2, command = contrast_func, bg_color = '#959595', fg_color = 'black', progress_color = '#001173', button_color = 'black')
            mutable_objects['text'] = ctk.CTkLabel(app, text = 'Contrast', font = ('Arial', 18), bg_color = '#959595', text_color = 'black')
            mutable_objects['text'].place(x = 464, y = 0)
        mutable_objects['slider'].place(x = 400, y = 30)
def undo_changes():
    global list_changes, changed_image, changing, list_undo_changes
    if changed_image != None and len(list_changes) > 1:
        changing = True
        list_undo_changes.append(list_changes[-1])
        list_changes.pop(-1)
        changed_image = list_changes[-1]
        show_image(changed_image)
    elif changed_image != None and len(list_changes) == 1:
        changing = True
        changed_image = list_changes[0]
        show_image(changed_image)
def redo_changes():
    global list_undo_changes, changed_image, changing, redo_changing
    if changed_image != None and len(list_undo_changes) > 1:
        redo_changing = True
        changed_image = list_undo_changes[-1]
        list_undo_changes.pop(-1)
        show_image(changed_image)
    elif changed_image!= None and len(list_undo_changes) == 1:
        redo_changing = True
        changed_image = list_undo_changes[0]
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
def crop_func():
    global changed_image
    if changed_image != None:
        label.bind('<Button-1>', start_crop)
        label.bind('<ButtonRelease-1>', end_crop)
def open_text_modal(event):
    global changed_image
    if changed_image != None:
        text_x = event.x
        text_y = event.y
        
        modal = ctk.CTkToplevel(frame_main)
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
                draw.text((text_x * change_x, text_y * change_y), entry_input_text.get(), font = font, fill = fill)
                modal.destroy()
                show_image(changed_image)
        button_send_text = ctk.CTkButton(modal, text = 'Apply', command = add_text)
        button_send_text.pack(pady = 5)
def watermark_remove_func():
    global changed_image, file_path
    if changed_image != None:
        img = np.array(changed_image)
        alpha = 2.0
        beta = -160
        new = alpha * img + beta
        new_img = np.clip(new, 0, 255).astype(np.uint8)
        changed_image = Image.fromarray(new_img)
        show_image(changed_image)
def background_remove_func():
    global changed_image
    if changed_image != None:
        changed_image = remove(changed_image)
        show_image(changed_image)
