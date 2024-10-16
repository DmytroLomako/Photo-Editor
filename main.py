from modules.settings import *
from modules.widgets import *
from modules.functions import *

app.mainloop()  
if os.path.exists(path_to_temp_image):
    os.remove(path_to_temp_image)