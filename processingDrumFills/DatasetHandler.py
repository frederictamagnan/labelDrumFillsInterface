import os
import json
from utils import shuffle_list

from pypianoroll import Multitrack,Track
import numpy as np
import sys

class DatasetHandler:

    def __init__(self, filepath_dataset, filepath_tags, logger):

        self.filepath_dataset = filepath_dataset
        self.filepath_tags = filepath_tags
        self.list_path_tracks_to_label = []
        self.list_id_tracks_to_label = []
        self.list_npz_name_tracks_to_label = []
        self.logger = logger
        self.list_multitrack=[]
        self.list_label=[]

        if not (os.path.isfile(self.filepath_dataset + "register.json")):
            logger.error("can't find register.json")
            sys.exit()
        else:
            with open(self.filepath_dataset + "register.json", "r") as read_file:
                self.register = dict(json.load(read_file))



        if not (os.path.isfile(self.filepath_dataset + "labels.npz")):
            logger.error("can't find labels.npz")
            sys.exit()



        if not (os.path.isfile(self.filepath_dataset + "drumFills.npz")):
            np.savez(self.filepath_dataset+"labels.npz",drumfills=np.empty((0,96,9,1,1)))
        else:
            self.data["drumfills"] = np.load(self.filepath_dataset + 'drumFills.npz')


        self.find_multitrack_labelised()

    def find_multitrack_labelised(self):

        with open(self.filepath_dataset + "register.json", "r") as read_file:
            register = json.load(read_file)
        self.logger.debug("--register "+str(register))
        # ITERATE OVER THE TAG LISTS

        for tag_i, tag in enumerate(self.filepath_tags):

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
                            p = self.filepath_dataset + self.middle + self.file

                            for npz in os.listdir(p):

                                if self.file in register["labelised"]:
                                    self.logger.debug("---Find a labeled track")
                                    self.list_path_tracks_to_label.append(p)
                                    self.list_npz_name_tracks_to_label.append(npz)
                                    self.list_id_tracks_to_label.append(self.file)
                                    self.list_multitrack.append(Multitrack(p+'/'+npz))
                                    data = np.load(self.filepath_dataset + 'labels.npz')
                                    self.list_label.append(data[self.file])


        # shuffle the list in the same order to keep corresponding indices
        # self.list_path_tracks_to_label, self.list_id_tracks_to_label, self.list_npz_name_tracks_to_label = shuffle_list(
        #     self.list_path_tracks_to_label, self.list_id_tracks_to_label, self.list_npz_name_tracks_to_label)
        #
        # # CAST TUPLE TO LIST - SORRY TO do THAT LIKE THIS
        # self.list_npz_name_tracks_to_label = list(self.list_npz_name_tracks_to_label)
        # self.list_path_tracks_to_label = list(self.list_path_tracks_to_label)
        # self.list_id_tracks_to_label = list(self.list_id_tracks_to_label)
