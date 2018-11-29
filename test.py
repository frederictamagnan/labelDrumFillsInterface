import os
from tkinter import *







import numpy as np
from pathlib import Path
import pypianoroll as ppr
from pypianoroll import Multitrack,Track
import time
import random




PATH_HOME = str(Path.home())
PATH_TAGS = [
    './id_lists/tagtraum/tagtraum_Electronic.id',
]

PATH = '/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd/lpd_cleansed/'

j = 0
list_path=[]
# ITERATE OVER THE TAG LISTS

for tag_i, tag in enumerate(PATH_TAGS):
    train_x_phr = np.zeros((0, 96, 84))

    if tag_i == 0:
        print('>>' + tag[29:-3])
        with open(tag, 'r') as f:
            # ITERATE OVER THE FOLDER LISTS
            for i in range(0,1000):
                for i, file in enumerate(f):
                    print(type(f))
                    # (str(f))
                    #                 print('load files..{}/{}'.format(i + 1, number_files[tag_i]), end="\r")
                    file = file.rstrip()
                    middle = '/'.join(file[2:5]) + '/'
                    p = PATH + middle + file
                    for npz in os.listdir(p):


                    list_path.append(p+"/"+npz)
                # ITERATE OVER THE NPZ FILES IN EACH FOLDER

                # for npz in os.listdir(p):
                #     # LOAD NPZ FILE INTO A PPR OBJECT
                #
                #     # loaded = Multitrack(p + "/" + npz)
                #     loaded = Multitrack('./midifiles/example.mid')
                #     track_unreduced = Track(
                #         pianoroll=loaded.tracks[0].pianoroll[self.cursor * 96:(self.cursor + 1) * 96], program=0,
                #         is_drum=True,
                #         name='my awesome piano')
                #     multi_unreduced = Multitrack(tracks=[track_unreduced])
                #     t = time.strftime("%Y%m%d_%H%M%S")
                #
                #     filepath = './midifiles/mid' + t + "_unreduced.mid"
                #     ppr.write(multi_unreduced, filepath)
                #
                #     self.cursor += 1
                #     return filepath

print(len(list_path))