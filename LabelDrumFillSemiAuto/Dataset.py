import os
import json
from utils import shuffle_list
import numpy as np

class Dataset:


    def __init__(self,filepath_dataset,filepath_tags,logger):

        self.filepath_dataset=filepath_dataset
        self.filepath_tags=filepath_tags
        self.list_path_tracks_to_label = []
        self.list_id_tracks_to_label = []
        self.list_npz_name_tracks_to_label = []
        self.logger=logger
        
        
        
        if not os.path.exists(self.filepath_dataset+"/temp"):
            os.makedirs(self.filepath_dataset+"/temp")


        if not os.path.exists(self.filepath_dataset):
            os.makedirs(self.filepath_dataset)


        if not(os.path.isfile(self.filepath_dataset+"register.json")):
            self.register={"labelised":[]}
            with open(self.filepath_dataset+"register.json", "w") as write_file:
                json.dump(self.register, write_file)
        else:
            with open(self.filepath_dataset + "register.json", "r") as read_file:
                self.register = dict(json.load(read_file))

        if not (os.path.isfile(self.filepath_dataset + "labels.npz")):
            np.savez(self.filepath_dataset+"labels.npz",empty=np.empty([2, 2]))

        self.define_list_npz_path_to_label()


    def define_list_npz_path_to_label(self):

        with open(self.filepath_dataset+"register.json", "r") as read_file:
            register = json.load(read_file)


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


    def pop(self):
        self.list_npz_name_tracks_to_label.pop(0)
        self.list_id_tracks_to_label.pop(0)
        self.list_path_tracks_to_label.pop(0)


    def save_label(self,trackHandler):
        """
        save_label and delete from the list of track to label the track whose label is saved
        :return:
        """
        self.logger.debug("*SAVE LABEL()")

        data=np.load(self.filepath_dataset+'labels.npz')
        data=dict(data)
        self.logger.debug("--loaded labels.npz into dictionnary")
        self.logger.debug("--len of keys of dico "+str(len(data.keys())))

        data[str(trackHandler.current_track_id)]=trackHandler.label_array
        print(trackHandler.label_array)
        self.logger.debug("--added the new label array to the dictionnary")
        self.logger.debug("--len of keys of dico with the added array =" + str(len(data.keys())))
        np.savez(self.filepath_dataset+'labels.npz', **data)
        self.logger.debug("--saved the dictionnary into labels.npz")
        self.logger.debug("-- NB of drum fills :"+str(trackHandler.label_array.sum()/trackHandler.current_timestep_window))


        liste_label=self.register["labelised"]
        liste_label.append(trackHandler.current_track_id)
        self.logger.debug("--New list of labels : "+str(liste_label))
        self.register["labelised"]=liste_label
        self.logger.debug("self.register "+str(self.register))
        with open(self.filepath_dataset+"register.json", 'w') as fp:
            bol=json.dump(obj=self.register,fp=fp)
        self.logger.debug("-- DUMPING JSON ???:"+str(bol))


        # print(self.list_npz_name_tracks_to_label)
        # print(self.list_path_tracks_to_label)
        self.pop()