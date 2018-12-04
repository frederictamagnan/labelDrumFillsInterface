
from pypianoroll import *
import os





GLOBAL_EXTRACT_LENGTH=4

PATH_TAGS = [
    './id_lists/tagtraum/tagtraum_Blues.id',
    './id_lists/tagtraum/tagtraum_Country.id',
    './id_lists/tagtraum/tagtraum_Electronic.id',
    './id_lists/tagtraum/tagtraum_Folk.id',
    './id_lists/tagtraum/tagtraum_Jazz.id',
    './id_lists/tagtraum/tagtraum_Latin.id',
    './id_lists/tagtraum/tagtraum_Metal.id',
    './id_lists/tagtraum/tagtraum_New-Age.id',
    './id_lists/tagtraum/tagtraum_Pop.id', # 8
    './id_lists/tagtraum/tagtraum_Punk.id',
    './id_lists/tagtraum/tagtraum_Rap.id',
    './id_lists/tagtraum/tagtraum_Reggae.id',
    './id_lists/tagtraum/tagtraum_RnB.id',
    './id_lists/tagtraum/tagtraum_Rock.id', # 13
    './id_lists/tagtraum/tagtraum_World.id',   
]
PATH = '/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd/lpd_cleansed/'


PATH2='/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd_debug/'

if not os.path.exists(PATH2):
    os.makedirs(PATH2)




def define_list_npz_path_to_label():




    # ITERATE OVER THE TAG LISTS

    for tag_i, tag in enumerate(PATH_TAGS):

        if True:
            print('>>' + tag[29:-3])
            with open(tag, 'r') as f:
                # ITERATE OVER THE FOLDER LISTS
                for i in range(0, 1000):
                    for i, file in enumerate(f):
                        # (str(f))
                        #                 print('load files..{}/{}'.format(i + 1, number_files[tag_i]), end="\r")
                        file = file.rstrip()
                        middle = '/'.join(file[2:5]) + '/'
                        p = PATH + middle + file

                        for npz in os.listdir(p):
                            loaded = Multitrack(p + "/" + npz)
                            croped=crop_multitrack(loaded)
                            if not os.path.exists(PATH2+middle+file):
                                os.makedirs(PATH2+middle+file)

                            save(PATH2+middle+file+"/"+npz,croped)



def crop_multitrack(multitrack):
    beat_window_length=4


    current_beat_resolution = multitrack.beat_resolution

    current_timestep_window = current_beat_resolution * beat_window_length * 4


    current_track = Track(pianoroll=multitrack.tracks[0].pianoroll[0:current_timestep_window*GLOBAL_EXTRACT_LENGTH,:],
                               program=0, is_drum=True,
                               name='current track to label')

    return Multitrack(tracks=[current_track])


define_list_npz_path_to_label()