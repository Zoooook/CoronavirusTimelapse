import os
import imageio

with imageio.get_writer('Coronavirus.gif', mode='I', fps=8) as writer:
    for filename in os.listdir('images/'):
        image = imageio.imread('images/' + filename)
        writer.append_data(image)