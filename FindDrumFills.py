from tkinter import *
import os
import numpy as np
import pypianoroll as ppr
from pypianoroll import Multitrack,Track
import time
from utils import shuffle_list
import json
import logging
from logging.handlers import RotatingFileHandler

from utils import draw_figure
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
        self.current_timestep = 0
        self.current_track_id = ""
        self.current_track = None
        self.current_track_path = None
        self.current_multitrack = None
        self.current_track_length = 0
        self.current_beat_resolution = 0
        self.beat_window_length = 4

        self.end_extract=None

        self.label_array = None
        self.current_timestep_window=0
        self.filepath_current_extract=""





        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)

        self.pack(fill=BOTH)


        # Création de nos widgets

        self.message = Label(self, text="LABEL INTERFACE DRUM FILLS")

        self.message.pack()

        self.bouton_quitter = Button(self, text="Quit", command=self.quit)

        self.bouton_quitter.pack(side="left")

        self.bouton_cliquer = Button(self, text="Next bar",command=self.cliquer)

        self.bouton_cliquer.pack(side="right")
        # self.grid(row=1,column=4,columnspan=2)
        self.button_listen_four_bar=Button(self,text="Listen to four bars",command=self.listen)
        self.button_listen_four_bar.pack()

        self.button_listen_current_extract = Button(self, text="ReListen current bar", command=self.listen_current_extract)
        self.button_listen_current_extract.pack()

        self.var_choix = StringVar()

        self.choix_un = Radiobutton(self, text="DRUM FILL", variable=self.var_choix, value=1)

        self.choix_zero = Radiobutton(self, text="NO DRUM FILL", variable=self.var_choix, value=0)

        self.choix_un.pack()

        self.choix_zero.pack()

        self.warning="nowarning"
        self.dico_warning={"warning":["You have to choose a label option","red"],"nowarning":[":)","black"]}

        self.button_info = Button(self, text="        ", height=2, width=20)
        self.button_info.pack(side="bottom")




        self.champ_label = Label(self, text=self.dico_warning[self.warning][0],fg=self.dico_warning[self.warning][1])

        self.champ_label.pack()

        w, h = 1000, 500
        self.canvas = Canvas(self, width=w, height=h)
        self.canvas.pack()



        #TODO shuffle self.list_path_tracks_to_label
        #TODO CHECK IF TEMP EXIST

        if not os.path.exists(self.PATH+"/temp"):
            os.makedirs(self.PATH+"/temp")


        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)


        if not(os.path.isfile(self.PATH+"register.json")):
            self.register={"labelised":[]}
            with open(self.PATH+"register.json", "w") as write_file:
                json.dump(self.register, write_file)
        else:
            with open(self.PATH + "register.json", "r") as read_file:
                self.register = dict(json.load(read_file))

        if not (os.path.isfile(self.PATH + "labels.npz")):
            np.savez(self.PATH+"labels.npz",empty=np.empty([2, 2]))

        logger.debug("self.register "+str(self.register))


        self.define_list_npz_path_to_label()
        self.pick_a_new_track_to_label()


    def define_list_npz_path_to_label(self):

        with open(self.PATH+"register.json", "r") as read_file:
            register = json.load(read_file)



        self.list_path_tracks_to_label = []
        self.list_id_tracks_to_label=[]
        self.list_npz_name_tracks_to_label=[]

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

                                if self.file not in register["labelised"]:
                                    self.list_path_tracks_to_label.append(p)
                                    self.list_npz_name_tracks_to_label.append(npz)
                                    self.list_id_tracks_to_label.append(self.file)


        #shuffle the list in the same order to keep corresponding indices
        self.list_path_tracks_to_label,self.list_id_tracks_to_label,self.list_npz_name_tracks_to_label=shuffle_list(self.list_path_tracks_to_label,self.list_id_tracks_to_label,self.list_npz_name_tracks_to_label)

        #CAST TUPLE TO LIST - SORRY TO do THAT LIKE THIS
        self.list_npz_name_tracks_to_label=list(self.list_npz_name_tracks_to_label)
        self.list_path_tracks_to_label=list(self.list_path_tracks_to_label)
        self.list_id_tracks_to_label=list(self.list_id_tracks_to_label)



        # sys.exit()

    def pick_a_new_track_to_label(self):

        self.button_info["text"]="NEW TRACK IS PICKED"
        logger.debug("*PICK A NEW TRACK TO LABEL*")
        self.current_timestep=0

        logger.debug("--current_timestep : "+ str(self.current_timestep))

        self.current_multitrack = Multitrack(self.list_path_tracks_to_label[0]+"/"+self.list_npz_name_tracks_to_label[0])

        logger.debug("--loaded a npz into a multitrack object")
        self.current_beat_resolution=self.current_multitrack.beat_resolution
        logger.debug("--current beat resolution : " +str(self.current_beat_resolution))

        self.current_timestep_window = self.current_beat_resolution * self.beat_window_length * 4
        logger.debug("--current time step window : "+str(self.current_timestep_window))

        self.current_track_id=self.list_id_tracks_to_label[0]
        logger.debug("--current track id " +self.current_track_id)

        self.current_track_path=self.list_path_tracks_to_label[0]
        logger.debug("--current track track path : "+self.current_track_path)

        self.current_track_length=len(self.current_multitrack.tracks[0].pianoroll)
        logger.debug("--current_track_length : " + str(self.current_track_length))

        self.current_track = Track(pianoroll=self.current_multitrack.tracks[0].pianoroll,
                                program=0, is_drum=True,
                                name='current track to label')
        logger.debug("--loaded multitrack into track object")

        self.label_array=np.zeros(self.current_track.pianoroll.shape[0])
        logger.debug("--initialized label array")
        self.current_timestep -= self.current_timestep_window
        return self.current_track













    def save_label(self):
        logger.debug("*SAVE LABEL()")

        data=np.load(self.PATH+'labels.npz')
        data=dict(data)
        logger.debug("--loaded labels.npz into dictionnary")
        logger.debug("--len of keys of dico "+str(len(data.keys())))

        data[str(self.current_track_id)]=self.label_array
        logger.debug("--added the new label array to the dictionnary")
        logger.debug("--len of keys of dico with the added array =" + str(len(data.keys())))
        np.savez(self.PATH+'labels.npz', **data)
        logger.debug("--saved the dictionnary into labels.npz")
        logger.debug("-- NB of drum fills :"+str(self.label_array.sum()/self.current_timestep_window))


        liste_label=self.register["labelised"]
        liste_label.append(self.current_track_id)
        logger.debug("--New list of labels : "+str(liste_label))
        self.register["labelised"]=liste_label
        logger.debug("self.register "+str(self.register))
        with open(self.PATH+"register.json", 'w') as fp:
            bol=json.dump(obj=self.register,fp=fp)
        logger.debug("-- DUMPING JSON ???:"+str(bol))


        # print(self.list_npz_name_tracks_to_label)
        # print(self.list_path_tracks_to_label)
        self.list_npz_name_tracks_to_label.pop(0)
        self.list_id_tracks_to_label.pop(0)
        self.list_path_tracks_to_label.pop(0)

        self.bouton_cliquer["text"]="NEXT TRACK"



    def cliquer(self):
        logger.debug("*CLIQUER()")
        self.button_info["text"]="LISTEN AND LABEL THE BAR !"


        label = self.var_choix.get()
        logger.debug("--check the value of the form : "+ str(label))
        self.var_choix.set(None)

        try:
            label=int(label)
        except:
            pass
        # in case user didn't fill the form --->warning
        if label not in [0,1]:
            self.warning="warning"
            logger.debug("--/!\ the user didn't fill the form /!\ ")


        else:
            self.warning="nowarning"

            if self.current_timestep>0:

                self.label_array[self.current_timestep:self.end_extract]=label
                logger.debug("--fill the label_array with label")

            # iterate overtimestep
            if self.current_timestep+self.current_timestep_window<self.current_track_length:
                self.bouton_cliquer["text"] = "Next bar"

                self.current_timestep+=self.current_timestep_window
                logger.debug("--case we can slide the timestep by one window ")
                logger.debug("--new timestep : " + str(self.current_timestep))

                if self.current_timestep+self.current_timestep_window<self.current_track_length:
                    self.end_extract=self.current_timestep+self.current_timestep_window
                    logger.debug("--case the length of the extract is one window ")
                else:
                    self.end_extract=self.current_track_length
                    logger.debug("--case the length of the extract is shorter than one window, reaching the end of the track")

                    logger.debug("--length of the extract :" +str(self.end_extract-self.current_timestep))

                extract = Track(pianoroll=self.current_track.pianoroll[self.current_timestep:self.end_extract,:],
                                        program=0, is_drum=True,
                                        name='extract from timestep'+str(self.current_timestep)+" to timestep"+str(self.end_extract))
                logger.debug("--loaded the extract into a track object")
                extract_multi = Multitrack(tracks=[extract])

                fig_x, fig_y = 100, 100
                fig,ax=extract_multi.plot()
                self.canvas.photo=draw_figure(self.canvas,fig,loc=(fig_x,fig_y))
                logger.debug("--draw the pplot into canvas")


                logger.debug("--loaded the track object into a multitrack object")
                t = time.strftime("%Y%m%d_%H%M%S")

                self.filepath_current_extract = self.PATH+'temp/mid' + t + "_extract.mid"
                ppr.write(extract_multi, self.filepath_current_extract)
                logger.debug("--wrote the extract to a midi temp file")
                time1=time.time()
                os.system("timidity " + self.filepath_current_extract)
                logger.debug("--played the midi file with timidity")
                time2=time.time()
                print("TIME",time2-time1)




                #os.remove(filepath)
            #or pick a new track if it's the end
            else:
                self.save_label()
                logger.debug("--we load a new track to label !!")
                self.pick_a_new_track_to_label()

        print(self.current_timestep_window,"TIMESTEPWINDOW")


        self.champ_label["text"]=self.dico_warning[self.warning][0]
        self.champ_label["fg"]=self.dico_warning[self.warning][1]
        logger.debug("--refreshed the warning info")



    def listen(self):

        if self.current_timestep + 2*self.current_timestep_window < self.current_track_length:
            end_extract = self.current_timestep + 2*self.current_timestep_window
        else:
            end_extract = self.current_track_length





        if self.current_timestep - 2*self.current_timestep_window >0:
            start_extract = self.current_timestep - 2*self.current_timestep_window
        else:
            start_extract = 0



        extract = Track(pianoroll=self.current_track.pianoroll[start_extract:end_extract, :],
                             program=0, is_drum=True,
                             name='extract from timestep' + str(self.current_timestep) + " to timestep" + str(
                                 self.end_extract))
        extract_multi = Multitrack(tracks=[extract])



        t = time.strftime("%Y%m%d_%H%M%S")

        filepath = self.PATH + 'temp/mid' + t + "_extract.mid"
        ppr.write(extract_multi, filepath)
        time1 = time.time()
        os.system("timidity " + filepath)


    def listen_current_extract(self):
        logger.debug("TIMIDITY CURRENT")

        os.system("timidity " + self.filepath_current_extract)
        logger.debug("TIMIDITY CURRENT")

fenetre = Tk()

interface = LabelApp(fenetre)



interface.mainloop()
print(interface.label_array[0:interface.current_timestep],"LOOOL")
interface.destroy()



































