import threading
from PIL import Image

import random

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self, img):
        post_processing(image=img)



def post_processing(image, size=(640, 360)):

    pp_args = {
    'resample': 0,
    'box': None 
    }

    filename = "test1.jpg"
    new_image = Image.Image.resize(image, size, pp_args['resample'], pp_args['box'])

    rotation = random.randrange(45, 90, 1)

    new_image = new_image.rotate(rotation)
    new_image.save(filename)