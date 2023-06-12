from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Separator
from PIL import Image, ImageFont, ImageDraw

# paths of photos to edit and watermark
W_LOGO = None
W_TEXT = None
PHOTOS = []

# percentage of photos width/height to cover with the watermark
w_ratio = 10

# font of TKinter text
font_title = ('times', 18, 'bold')
font_body = ('times', 12, 'normal')

# accepted file types for images
file_types = [('Image', '*.jpg'), ('Image', '*.png')]


# ------------------------------------------------- FUNCTIONS ----------------------------------------------------- #
def add_watermark():
    """Takes the watermark (priority to image, if both image and text are given) and adds it to all the images uploaded.
    Then it stops the program"""
    if W_LOGO:
        # ADD LOGO
        for photo in PHOTOS:
            with Image.open(photo) as img, Image.open(W_LOGO) as logo:
                # logo_res = logo.resize((100, 100))  # fixed logo size
                ratio = max([img.size[0] / w_ratio / logo.size[0], img.size[1] / w_ratio / logo.size[1]])  # logo size scalable on photo size
                new_size = (int(logo.size[0] * ratio), int(logo.size[1] * ratio))
                logo_res = logo.resize(new_size)
                # logo_res.show()
                img_new = img
                img_new.paste(logo_res, box=(img.size[0] - logo_res.size[0] - 20, img.size[1] - logo_res.size[1] - 20), mask=logo_res.convert('RGBA'))
                # a partial transparent logo is correctly viewed, but the mask must be converted to RGBA to avoid possibile errors
                # img_new.show()
                img_new.save(f'C:/Users/simom/OneDrive/Immagini/Watermark_app/{photo.split("/")[-1]}')
    else:
        # ADD TEXT
        for photo in PHOTOS:
            with Image.open(photo) as img:
                draw = ImageDraw.Draw(img)
                # font = ImageFont.truetype(<font-file>, <font-size>)
                font = ImageFont.truetype('SansSerif.ttf', img.size[1]//w_ratio)
                # draw.text((x, y),"Sample Text",(r,g,b))
                draw.text((0, 0), W_TEXT, (255, 255, 255), font=font)
                img.show()
                img.save(f'C:/Users/simom/OneDrive/Immagini/Watermark_app/{photo.split("/")[-1]}')
    window.destroy()


def upload_logo():
    """Select and upload a single image to be used as loo for watermark"""
    global W_LOGO
    W_LOGO = filedialog.askopenfilename(filetypes=file_types)
    if W_LOGO:
        choose_logo.config(text='Upload logo (done!)')


def upload_photos():
    """Select and upload all photos to watermark"""
    global PHOTOS
    PHOTOS = filedialog.askopenfilename(multiple=True, filetypes=file_types)
    if PHOTOS:
        choose_photos.config(text='Upload photos (done!)')


def confirm_choices():
    """If a text is given as a watermark, get it.
    Confirm the selection of photos and watermark uploaded and proceed."""
    global W_TEXT
    W_TEXT = choose_text.get()
    if (W_TEXT or W_LOGO) and PHOTOS != []:
        add_watermark()

    # PARTIAL CODE to get a preview of photos with the watermark and the possibility to move it
    # very difficult: not worth to add it
        # for elem in window.grid_slaves()[:-1]:  à to remove elements from tkinter window
        #     print(elem)
        #     elem.destroy()
        #
        # curr_photo = Label(image=PHOTOS[0])  # (image=ImageTk.PhotoImage(file='images/snorlax.jpg')) #(image=PHOTOS[0])
        # curr_photo.bind("<Button-1>", callback)
        # curr_photo.focus_set()
        # curr_photo.grid(row=1, column=0, columnspan=2, pady=50)
        #
        # confirm_add = Button(text='Save photo and continue', command=save_and_next, font=font_body)
        # confirm_add.grid(row=2, column=1)

        # def save_and_next():
        #     pass
        #
        # def callback(event):
        #     print("clicked at", event.x, event.y)


# -------------------------------------------- SETUP UI ---------------------------------------------------
window = Tk()
# window.geometry(window_size)  # Size of the window
window.title("Watermark App")
window.config(padx=50, pady=25)

main_text = Label(text='Choose a logo or text to add to your images', font=font_title)
main_text.grid(row=0, column=0, columnspan=2, pady=25)

choose_logo = Button(text='Upload logo', width=20, command=upload_logo, pady=20, font=font_body)
choose_logo.grid(row=1, column=0, rowspan=2)

text2 = Label(text='OR write your text:', font=font_body)
text2.grid(row=1, column=1)

choose_text = Entry(width=20, font=font_body)
choose_text.grid(row=2, column=1)

separator = Separator(orient='horizontal')
separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=30)

text3 = Label(text='Choose pictures to watermark', font=font_title)
text3.grid(row=4, column=0, columnspan=2)

choose_photos = Button(text='Upload photos', command=upload_photos, font=font_body, width=20, pady=20)
choose_photos.grid(row=5, column=0, columnspan=2, pady=25)

confirm_but = Button(text='Confirm', width=20, command=confirm_choices, font=font_body)
# confirm_but['state'] = 'disable'
confirm_but.grid(row=6, column=0, columnspan=2, pady=25)

window.mainloop()
