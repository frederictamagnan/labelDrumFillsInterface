from tkinter import *
import os
import numpy as np

import time
from utils import shuffle_list
import json
import logging
from logging.handlers import RotatingFileHandler

from utils import draw_figure
from Dataset import Dataset
from TrackHandler import TrackHandler
from RuleHandler import RuleHandler
from utils import touch

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


import sys









class FindDrumFills(Frame):




    def __init__(self, fenetre, **kwargs):

        self.PATH_TAGS = [
            './id_lists/tagtraum/tagtraum_Rock.id',
        ]

        self.PATH = '/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd_debug/'


        self.dataset=Dataset(self.PATH,self.PATH_TAGS)



        self.label_array = None
        self.current_timestep_window=0
        self.filepath_current_extract=""

        self.is_current_extract_labeled=False



        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.pack(fill=BOTH)


        # Création de nos widgets

        self.message = Label(self, text="LABEL INTERFACE DRUM FILLS")

        self.message.pack()

        self.quit_button = Button(self, text="Quit", command=self.quit)

        self.quit_button.pack(side="left")

        self.label_button=Button(self,text="Label it",command=self.to_label)

        self.next_button = Button(self, text="Next Track",command=self.next)

        self.next_button.pack(side="right")
        # self.grid(row=1,column=4,columnspan=2)
        self.button_listen_four_bar=Button(self,text="Listen to four bars",command=self.listen)
        self.button_listen_four_bar.pack()

        self.button_listen_current_extract = Button(self, text="ReListen current bar", command=self.listen_current_extract)
        self.button_listen_current_extract.pack()

        self.var_choix = StringVar()

        self.radioButton_one = Radiobutton(self, text="DRUM FILL", variable=self.var_choix, value=1)

        self.radioButton_zero = Radiobutton(self, text="NO DRUM FILL", variable=self.var_choix, value=0)

        self.radioButton_one.pack()

        self.radioButton_zero.pack()

        self.warning="nowarning"
        self.dico_warning={"warning":["You have to choose a label option","red"],"nowarning":[":)","black"]}

        self.button_info = Label(self, text="        ", height=2, width=20)
        self.button_info.pack(side="bottom")




        self.champ_label = Label(self, text=self.dico_warning[self.warning][0],fg=self.dico_warning[self.warning][1])

        self.champ_label.pack()

        w, h = 1000, 500
        self.canvas = Canvas(self, width=w, height=h)
        self.canvas.pack()


        self.ruleHandler=RuleHandler(logger)
        self.dataset=Dataset(filepath_dataset=self.PATH,filepath_tags=self.PATH_TAGS,logger)
        self.trackHandler=TrackHandler(dataset=self.dataset,logger)




        #TODO shuffle self.list_path_tracks_to_label
        #TODO CHECK IF TEMP EXIST



        logger.debug("self.register "+str(self.register))


        dataset.define_list_npz_path_to_label()






    def next(self):
        """
        define the next button to iterate over row or pick a new track
        :return:
        """


        logger.debug("*NEXT()")

        if self.current_timestep<0:
            self.pick_a_new_track_to_label()
            self.button_info["text"] = "A new track to label is picked"
            self.next_button["text"] = "Next bar"
            return None

        elif self.can_iterate():

            extract,extract_multi=self.iterate_over_bars()

            self.plotBar(extract_multi)
            self.listen_current_extract(extract_multi)

        else:
            self.save_label()





        self.button_info["text"] = "LISTEN AND LABEL THE BAR !"


    def can_iterate(self):
        return self.can_iterate




    def is_current_extract_labeled(self):

        return self.is_current_extract_labeled

    
    def reset_radio_button(self):
        logger.debug("--check the value of the form : " + str(label))
        self.var_choix.set(None)


    def to_label(self,label):
        
        self.label_array[self.current_timestep:self.end_extract] = label
        logger.debug("--fill the label_array with label")
        
        
        
    def control_if_radio_button_is_checked(self,label):

        
        try:
            label = int(label)
        except:
            pass
        # in case user didn't fill the form --->warning
        if label not in [0, 1]:
            self.warning = "warning"
            logger.debug("--/!\ the user didn't fill the form /!\ ")
            return False
        else:
            return True




























fenetre = Tk()

interface = LabelApp(fenetre)



interface.mainloop()
print(interface.label_array[0:interface.current_timestep],"LOOOL")
interface.destroy()



































