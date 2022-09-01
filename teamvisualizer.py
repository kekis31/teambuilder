import os
from PIL import Image
from PIL import ImageDraw

class Visualizer:
    def generate_image(self, participantlist):
        participants = len(participantlist)

        imgwidth = int(participants / 2) * 350 + (200 * int((participants / 2) / 3))

        img = Image.new(mode="RGB", size = (imgwidth, 1280), color=(200, 0, 0))
        draw = ImageDraw.Draw(img)

        iconpath = f'{os.getcwd()}/icons'

        for x in range(participants):
            offset = 350*x
            offset += 200 * int(x / 3)
            
            yoffset = 0
            if (x >= participants / 2):
                yoffset += 450
                offset -= 350*participants / 2 + 200 * int(x / 3)
                offset += 200 * int((x - (participants / 2)) / 3)

            draw.rectangle((100 + offset, 100 + yoffset, 400 + offset, 400 + yoffset), outline="green", width=20)
            draw.rectangle((110 + offset, 110 + yoffset, 390 + offset, 390 + yoffset), outline=(0,255,0), width=10)

            rectcenter = (250 + offset, 250 + yoffset)
            rectcorner = (int(120 + offset), int(120 + yoffset))

            icon = Image.open(f'{iconpath}/default.png')
            icon = icon.resize((260, 260))

            img.paste(icon, rectcorner)

        img.show()