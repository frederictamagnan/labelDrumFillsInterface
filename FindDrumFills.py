from tkinter import *

import logging
from logging.handlers import RotatingFileHandler

from Dataset import Dataset
from TrackHandler import TrackHandler

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





PATH = '/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd_debug/'
PATH_TAGS = [
            './id_lists/tagtraum/tagtraum_Rock.id',
        ]




class FindDrumFills(Frame):




    def __init__(self, fenetre, **kwargs):



        self.dataset = Dataset(filepath_dataset=PATH, filepath_tags=PATH_TAGS, logger=logger)
        self.trackHandler = TrackHandler(dataset=self.dataset, logger=logger)

        self.isTrackLoaded=False




        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.pack(fill=BOTH)


        # Création de nos widgets

        self.message = Label(self, text="LABEL INTERFACE DRUM FILLS")

        self.message.pack()

        self.button_quit = Button(self, text="Quit", command=self.quit)

        self.button_quit.pack(side="left")

        self.button_label=Button(self,text="Label it",command=self.to_label)

        self.button_label.pack()
        self.button_next = Button(self, text="Next Track",command=self.next)

        self.button_next.pack(side="right")
        self.button_listen_four_bar=Button(self,text="Listen to four bars",command=self.trackHandler.listen)
        self.button_listen_four_bar.pack()

        self.button_listen_current_extract = Button(self, text="ReListen current bar", command=self.trackHandler.listen_current_extract)
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







        #TODO shuffle self.list_path_tracks_to_label
        #TODO CHECK IF TEMP EXIST



        logger.debug("self.register "+str(self.register))






    


    def next(self):
        """
        define the next button to iterate over bars or pick a new track
        :return:
        """


        if not(self.isTrackLoaded):
            self.trackHandler.pick_a_new_track_to_label()
            self.button_info["text"]="A new track is loaded"
            self.button_next["text"]="Next Bar"
            self.isTrackLoaded=True
            self.trackHandler.label_set=True


        else:


            if not(self.trackHandler.label_set):
                self.button_info["text"]="You have to choose label"
                return

            self.reset_radio_button()

            extract,extract_multi,reachTheEnd=self.trackHandler.iterate_over_bars()
            if reachTheEnd:
                self.button_info["text"] = "Reached the end of the track"
                self.button_next["text"]="Next Track"
                self.isTrackLoaded=False
                self.dataset.save_label(trackHandler=self.trackHandler)

            else:
                self.trackHandler.plotBar(self.canvas,extract_multi)
                self.trackHandler.playBar(extract_multi)


    def reset_radio_button(self):
        self.var_choix.set(None)


    def to_label(self):

        label=self.var_choix.get()
        if not (self.control_if_radio_button_is_checked(label)):
            self.button_info["text"] = "the radio button isn't checked"
            return


        self.trackHandler.to_label(label)
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
interface = FindDrumFills(fenetre)
interface.mainloop()
interface.destroy()



































