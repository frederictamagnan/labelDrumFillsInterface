from DatasetHandler import DatasetHandler
from pypianoroll import Multitrack,Track

import logging
from logging.handlers import RotatingFileHandler


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
            '/home/ftamagna/Documents/_AcademiaSinica/code/LabelDrumFills/id_lists/tagtraum/tagtraum_Rock.id',
        ]

BEAT_WINDOW_LENGTH = 4

class Processing:

    def __init__(self):
        self.dataset = DatasetHandler(filepath_dataset=PATH, filepath_tags=PATH_TAGS, logger=logger)

        # print(self.dataset.list_path_tracks_to_label)
        self.logger=logger
        self.beat_window_length=BEAT_WINDOW_LENGTH

        self.current_timestep = 0

        self.current_timestep = 0
        self.current_track_id = ""
        self.current_track = None
        self.current_track_path = None
        self.current_multitrack = None
        self.current_track_length = 0
        self.current_beat_resolution = 0
        self.end_extract = None





    def pick_a_new_track_to_label(self,i):

        self.logger.debug("*PICK A NEW TRACK TO LABEL*")
        self.current_timestep=0

        self.logger.debug("--current_timestep : "+ str(self.current_timestep))

        self.current_multitrack = self.dataset.list_multitrack[i]

        self.logger.debug("--loaded a npz into a multitrack object")
        self.current_beat_resolution=self.current_multitrack.beat_resolution
        self.logger.debug("--current beat resolution : " +str(self.current_beat_resolution))

        self.current_timestep_window = self.current_beat_resolution * self.beat_window_length
        self.logger.debug("--current time step window : "+str(self.current_timestep_window))

        self.current_track_id=self.dataset.list_id_tracks_to_label[i]
        self.logger.debug("--current track id " +self.current_track_id)

        self.current_track_path=self.dataset.list_path_tracks_to_label[i]
        self.logger.debug("--current track track path : "+self.current_track_path)

        self.current_track_length=(self.current_multitrack.tracks[0].pianoroll.shape[0])
        self.logger.debug("--current_track_length : " + str(self.current_track_length))

        self.current_track = Track(pianoroll=self.current_multitrack.tracks[0].pianoroll,
                                program=0, is_drum=True,
                                name='current track to label')
        self.logger.debug("--loaded multitrack into track object")

        self.label_array=self.dataset.list_label[i]
        self.logger.debug("--initialized label array")
        self.current_timestep -= self.current_timestep_window




    def process_track(self):

        number_bars=self.current_track_length/self.current_timestep_window
        label_list=[]
        # iterate overtimestep
        while (self.current_timestep + self.current_timestep_window) < self.current_track_length:

            self.current_timestep += self.current_timestep_window
            logger.debug("--case we can slide the timestep by one window ")
            logger.debug("--new timestep : " + str(self.current_timestep))

            if self.current_timestep + self.current_timestep_window < self.current_track_length:
                self.end_extract = self.current_timestep + self.current_timestep_window
                logger.debug("--case the length of the extract is one window ")
            else:
                self.end_extract = self.current_track_length
                logger.debug(
                    "--case the length of the extract is shorter than one window, reaching the end of the track")

                logger.debug("--length of the extract :" + str(self.end_extract - self.current_timestep))

            extract = Track(pianoroll=self.current_track.pianoroll[self.current_timestep:self.end_extract, :],
                            program=0, is_drum=True,
                            name='extract from timestep' + str(self.current_timestep) + " to timestep" + str(
                                self.end_extract))


            

            label_list.append(self.label_array[self.current_timestep:self.end_extract].mean())


        return label_list,number_bars



proc=Processing()
for i in range(0,5):

    proc.pick_a_new_track_to_label(i)
    label_list,number_bars=proc.check_labeling()
    print(label_list,number_bars)



