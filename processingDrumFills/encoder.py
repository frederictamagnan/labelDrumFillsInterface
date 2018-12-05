from pypianoroll import Multitrack,Track
import numpy as np

DEFAULT_DRUM_TYPE_PITCHES = [
    # bass drum
    [36, 35],

    # snare drum
    [38, 27, 28, 31, 32, 33, 34, 37, 39, 40, 56, 65, 66, 75, 85],

    # closed hi-hat
    [42, 44, 54, 68, 69, 70, 71, 73, 78, 80],

    # open hi-hat
    [46, 67, 72, 74, 79, 81],

    # low tom
    [45, 29, 41, 61, 64, 84],

    # mid tom
    [48, 47, 60, 63, 77, 86, 87],

    # high tom
    [50, 30, 43, 62, 76, 83],

    # crash cymbal
    [49, 55, 57, 58],

    # ride cymbal
    [51, 52, 53, 59, 82]
]

_drum_map = dict(enumerate(DEFAULT_DRUM_TYPE_PITCHES))
_inverse_drum_map =  dict((pitch, index)
                                  for index, pitches in _drum_map.items()
                                  for pitch in pitches)



class MultiDrumOneHotEncoding():
    def __init__(self):
        self._drum_type_pitches = DEFAULT_DRUM_TYPE_PITCHES
        self._drum_map = dict(enumerate(DEFAULT_DRUM_TYPE_PITCHES))
        self._inverse_drum_map = dict((pitch, index)
                                      for index, pitches in _drum_map.items()
                                      for pitch in pitches)

    def encode_drum(self, pitches_in):
        nonzero = np.where(pitches_in == 1)[0] + 24
        ret = np.zeros(len(self._drum_type_pitches))
        for reduced, pitches in _drum_map.items():
            for p in pitches:
                if p in nonzero:
                    ret[reduced] = 1
                    break
        return ret

    def decode_drum(self, pitches_out):
        ret = np.zeros(84)
        for reduced, p in enumerate(pitches_out):
            if p == 1:
                ret[self._drum_type_pitches[reduced][0] - 24] = 1
        return ret

    def checkDrumEmpty(track):
        compare = (track == np.zeros(track.shape))
        count = np.size(compare) - np.count_nonzero(compare)
        if count > 3:
            return True
        return False

drum_encoding = MultiDrumOneHotEncoding()
multi=Multitrack('/home/ftamagna/Documents/_AcademiaSinica/dataset/lpd/lpd_cleansed/A/A/A/TRAAAGR128F425B14B/b97c529ab9ef783a849b896816001748.npz')

for i in range(96,1000):
    if multi.tracks[0].pianoroll[i,:].sum()>0:
        print(multi.tracks[0].pianoroll[i,:])
        print(i)
        break
print(drum_encoding.encode_drum(multi.tracks[0].pianoroll[i,:]))

