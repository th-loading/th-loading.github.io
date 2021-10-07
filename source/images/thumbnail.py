from PIL import Image

image = Image.open("wp.png")
MAX_SIZE = (1000,1000)
image.thumbnail(MAX_SIZE)
image.save('tb.png')
