
from utils import draw_figure
import pypianoroll as ppr
from pypianoroll import Multitrack,Track
import numpy as np
import time
from RuleHandler import RuleHandler
import os
BEAT_WINDOW_LENGTH = 4


class TrackHandler:





    def __init__(self,dataset,logger):


        self.logger=logger

        self.dataset=dataset

        self.current_timestep=0

        self.current_timestep = 0
        self.current_track_id = ""
        self.current_track = None
        self.current_track_path = None
        self.current_multitrack = None
        self.current_track_length = 0
        self.current_beat_resolution = 0
        self.beat_window_length = BEAT_WINDOW_LENGTH

        self.end_extract = None

        self.label_set=False

        self.ruleHandler = RuleHandler(self.logger)


    def pick_a_new_track_to_label(self):

        self.logger.debug("*PICK A NEW TRACK TO LABEL*")
        self.current_timestep=0

        self.logger.debug("--current_timestep : "+ str(self.current_timestep))

        self.current_multitrack = Multitrack(self.dataset.list_path_tracks_to_label[0]+"/"+self.dataset.list_npz_name_tracks_to_label[0])

        self.logger.debug("--loaded a npz into a multitrack object")
        self.current_beat_resolution=self.current_multitrack.beat_resolution
        self.logger.debug("--current beat resolution : " +str(self.current_beat_resolution))

        self.current_timestep_window = self.current_beat_resolution * self.beat_window_length * 4
        self.logger.debug("--current time step window : "+str(self.current_timestep_window))

        self.current_track_id=self.dataset.list_id_tracks_to_label[0]
        self.logger.debug("--current track id " +self.current_track_id)

        self.current_track_path=self.dataset.list_path_tracks_to_label[0]
        self.logger.debug("--current track track path : "+self.current_track_path)

        self.current_track_length=len(self.current_multitrack.tracks[0].pianoroll)
        self.logger.debug("--current_track_length : " + str(self.current_track_length))

        self.current_track = Track(pianoroll=self.current_multitrack.tracks[0].pianoroll,
                                program=0, is_drum=True,
                                name='current track to label')
        self.logger.debug("--loaded multitrack into track object")

        self.label_array=np.full(self.current_track.pianoroll.shape[0],-1)
        self.logger.debug("--initialized label array")
        self.current_timestep -= self.current_timestep_window



    def plotBar(self,canvas,extract_multi):
        fig_x, fig_y = 100, 100
        fig, ax = extract_multi.plot()
        canvas.photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
        self.logger.debug("--draw the pplot into canvas")





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

        filepath = self.dataset.filepath_dataset + 'temp/mid' + t + "_extract.mid"
        ppr.write(extract_multi, filepath)
        time1 = time.time()
        os.system("timidity " + filepath)


    def listen_current_extract(self):
        self.logger.debug("TIMIDITY CURRENT")

        os.system("timidity " + self.filepath_current_extract)
        self.logger.debug("TIMIDITY CURRENT")




    def playBar(self,extract_multi):

        self.logger.debug("--loaded the track object into a multitrack object")
        t = time.strftime("%Y%m%d_%H%M%S")

        self.filepath_current_extract = self.dataset.filepath_dataset + 'temp/mid' + t + "_extract.mid"
        ppr.write(extract_multi, self.filepath_current_extract)
        self.logger.debug("--wrote the extract to a midi temp file")
        time1 = time.time()
        os.system("timidity " + self.filepath_current_extract)
        self.logger.debug("--played the midi file with timidity")
        time2 = time.time()
        print("TIME", time2 - time1)
        
        
    
    def nextBar(self):


        self.label_set=False
        #CASE WE HAVE REACH THE END OF THE TRACK


        # iterate overtimestep
        if self.current_timestep + self.current_timestep_window < self.current_track_length:

            self.current_timestep += self.current_timestep_window
            self.logger.debug("--case we can slide the timestep by one window ")
            self.logger.debug("--new timestep : " + str(self.current_timestep))

            if self.current_timestep + self.current_timestep_window < self.current_track_length:
                self.end_extract = self.current_timestep + self.current_timestep_window
                self.logger.debug("--case the length of the extract is one window ")
            else:
                self.end_extract = self.current_track_length
                self.logger.debug(
                    "--case the length of the extract is shorter than one window, reaching the end of the track")

                self.logger.debug("--length of the extract :" + str(self.end_extract - self.current_timestep))

            extract = Track(pianoroll=self.current_track.pianoroll[self.current_timestep:self.end_extract, :],
                            program=0, is_drum=True,
                            name='extract from timestep' + str(self.current_timestep) + " to timestep" + str(
                                self.end_extract))
            self.logger.debug("--loaded the extract into a track object")
            extract_multi = Multitrack(tracks=[extract])

            return extract,extract_multi,False

        return 0, 0, True

    def iterate_over_bars(self):

        first_iteration=True
        extract=None
        extract_multi=None
        while not(self.ruleHandler.isContainingDrumFills(extract,first_iteration)) :


                self.logger.debug("--case we can slide the timestep by one window ")
                self.logger.debug("--new timestep : " + str(self.current_timestep))
                extract,extract_multi,reachTheEnd=self.nextBar()
                if reachTheEnd:
                    return 0,0,reachTheEnd


                first_iteration=False
                self.label_array[self.current_timestep:self.end_extract] = 0


        return extract,extract_multi,False


    def to_label(self,label):
        self.label_array[self.current_timestep:self.end_extract] = label
        self.label_set=True

