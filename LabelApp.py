import os
from tkinter import *


from tkinter import *
from PIL import ImageTk, Image
import os


from utils import save

import numpy as np
from pathlib import Path
import pypianoroll as ppr
from pypianoroll import Multitrack,Track
import time
import random

import json


class LabelApp(Frame):




    def __init__(self, fenetre, **kwargs):

        self.PATH_TAGS = [
            './id_lists/tagtraum/tagtraum_Jazz.id',
        ]

        self.PATH = '/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd/lpd_cleansed/'
        self.current_timestep = 0
        self.current_track_id = ""
        self.current_track = None
        self.current_track_path = None
        self.current_multitrack = None
        self.current_track_length = 0
        self.current_beat_resolution = 0
        self.beat_window_length = 2

        self.label_array = None
        self.current_timestep_window=0





        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.pack(fill=BOTH)


        # Création de nos widgets

        self.message = Label(self, text="LABEL INTERFACE DRUM FILLS")

        self.message.pack()

        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)

        self.bouton_quitter.pack(side="left")

        self.bouton_cliquer = Button(self, text="Cliquez ici", fg="red",

                                     command=self.cliquer)

        self.bouton_cliquer.pack(side="right")

        self.var_choix = StringVar()

        choix_un = Radiobutton(fenetre, text="DRUM FILL", variable=self.var_choix, value=1)

        choix_zero = Radiobutton(fenetre, text="NO DRUM FILL", variable=self.var_choix, value=0)

        img = ImageTk.PhotoImage(Image.open("True1.gif"))
        panel = Label(root, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        root.mainloop()



        choix_un.pack()

        choix_zero.pack()





        #TODO shuffle self.list_path_tracks_to_label
        #TODO CHECK IF TEMP EXIST

        if not os.path.exists(self.PATH+"/temp"):
            os.makedirs(self.PATH+"/temp")


        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)


        if not(os.path.isfile(self.PATH+"register.json")):
            register={"labelised":[]}
            with open(self.PATH+"register.json", "w") as write_file:
                json.dump(register, write_file)



        self.define_list_npz_path_to_label()

    def define_list_npz_path_to_label(self):

        with open(self.PATH+"register.json", "r") as read_file:
            register = json.load(read_file)



        j = 0
        self.list_path_tracks_to_label = []
        self.list_id_tracks_to_label=[]

        # ITERATE OVER THE TAG LISTS

        for tag_i, tag in enumerate(self.PATH_TAGS):

            if tag_i == 0:
                print('>>' + tag[29:-3])
                with open(tag, 'r') as f:
                    # ITERATE OVER THE FOLDER LISTS
                    for i in range(0, 1000):
                        for i, file in enumerate(f):
                            # (str(f))
                            #                 print('load files..{}/{}'.format(i + 1, number_files[tag_i]), end="\r")
                            self.file = file.rstrip()
                            self.middle = '/'.join(self.file[2:5]) + '/'
                            p = self.PATH + self.middle + self.file
                            for npz in os.listdir(p):

                                if npz not in register["labelised"]:
                                    self.list_path_tracks_to_label.append(p)
                                    self.list_id_tracks_to_label.append(npz)


    def pick_a_new_track_to_label(self):

        self.current_multitrack = Multitrack(self.list_path_tracks_to_label[0]+"/"+self.list_id_tracks_to_label[0])
        self.current_beat_resolution=self.current_multitrack.beat_resolution
        self.current_timestep_window = self.current_beat_resolution * self.beat_window_length * 4

        self.current_track_id=self.list_id_tracks_to_label[0]
        self.current_track_path=self.list_path_tracks_to_label[0]
        self.current_track_length=len(self.current_multitrack.tracks[0].pianoroll)
        self.current_track = Track(pianoroll=self.current_multitrack.tracks[0].pianoroll,
                                program=0, is_drum=True,
                                name='current track to label')

        self.label_array=np.zeros(self.current_track.pianoroll.shape[0])
        return self.current_track


    def save_label(self):

        with load(self.PATH+'labels.npz') as data:
            np.savez(self.PATH+'labels.npz', {str(self.current_track_id):self.label_array})




    def cliquer(self):

        if self.current_timestep+self.current_timestep_window<self.current_track_length:
            self.current_timestep+=self.current_timestep_window

            if self.current_timestep+self.current_timestep_window<self.current_track_length:
                end_extract=self.current_timestep+self.current_timestep_window
            else:
                end_extract=self.current_track_length

            print(end_extract-self.current_timestep,"DIFF")

            extract = Track(pianoroll=self.current_track.pianoroll[self.current_timestep:end_extract],
                                    program=0, is_drum=True,
                                    name='my awesome piano')
            extract_multi = Multitrack(tracks=[extract])
            t = time.strftime("%Y%m%d_%H%M%S")

            filepath = self.PATH+'temp/mid' + t + "_extract.mid"
            ppr.write(extract_multi, filepath)
            time1=time.time()
            os.system("timidity " + filepath)
            time2=time.time()
            print("TIME",time2-time1)
            self.label_array[self.current_timestep]=self.var_choix.get()
            #os.remove(filepath)

        else:
            self.pick_a_new_track_to_label()

        print(self.current_timestep_window,"TIMESTEPWINDOW")

        self.message["text"] = "Vous avez cliqué {} fois."+str(self.current_timestep)




fenetre = Tk()

interface = LabelApp(fenetre)



interface.mainloop()
print(interface.label_array[0:interface.current_timestep],"LOOOL")
interface.destroy()



































