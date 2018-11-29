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
    './id_lists/tagtraum/tagtraum_Jazz.id',
]

PATH = '/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd/lpd_cleansed/'


class Interface(Frame):
    """Notre fenêtre principale.

    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.pack(fill=BOTH)

        self.nb_clic = 0

        # Création de nos widgets

        self.message = Label(self, text="Vous n'avez pas cliqué sur le bouton.")

        self.message.pack()

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)

        self.bouton_quitter.pack(side="left")

        self.bouton_cliquer = Button(self, text="Cliquez ici", fg="red",

                                     command=self.cliquer)

        self.bouton_cliquer.pack(side="right")
        self.cursor=0


    def cliquer(self):
        """Il y a eu un clic sur le bouton.



        On change la valeur du label message."""

        self.nb_clic += 1
        filepath=self.findtrack()
        os.system("timidity "+filepath)

        self.message["text"] = "Vous avez cliqué {} fois.".format(self.nb_clic)



    def findtrack(self):

        j = 0

        # ITERATE OVER THE TAG LISTS
        for tag_i, tag in enumerate(PATH_TAGS):
            train_x_phr = np.zeros((0, 96, 84))

            if tag_i == 0:
                print('>>' + tag[29:-3])
                with open(tag, 'r') as f:
                    # ITERATE OVER THE FOLDER LISTS

                    for i, file in enumerate(f):
                        print(type(f))
                        # (str(f))
                        #                 print('load files..{}/{}'.format(i + 1, number_files[tag_i]), end="\r")
                        file = file.rstrip()
                        middle = '/'.join(file[2:5]) + '/'
                        p = PATH + middle + file

                        # ITERATE OVER THE NPZ FILES IN EACH FOLDER

                        for npz in os.listdir(p):
                            # LOAD NPZ FILE INTO A PPR OBJECT

                            #loaded = Multitrack(p + "/" + npz)
                            loaded=Multitrack('./midifiles/example.mid')
                            track_unreduced = Track(pianoroll=loaded.tracks[0].pianoroll[self.cursor*96:(self.cursor+1)*96], program=0, is_drum=True,
                                                    name='my awesome piano')
                            multi_unreduced = Multitrack(tracks=[track_unreduced])
                            t = time.strftime("%Y%m%d_%H%M%S")

                            filepath = './midifiles/mid' + t + "_unreduced.mid"
                            ppr.write(multi_unreduced, filepath)

                            self.cursor+=1
                            return filepath












fenetre = Tk()

interface = Interface(fenetre)


interface.mainloop()

interface.destroy()