from PIL import Image

with Image.open("rocket.png") as original:
    # original.show()
    print(original.size)
    pic_gray = original.convert("L")
    pic_gray = pic_gray.transpose(Image.ROTATE_180)
    pic_gray.show()