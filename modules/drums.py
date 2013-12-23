#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

from constants import *
import preferences
import gettext
_ = gettext.gettext

bass = notes_abc[percussionname_to_int("Acoustic Bass Drum")]
snare = notes_abc[percussionname_to_int("Acoustic Snare")]
stick = notes_abc[percussionname_to_int("Side Stick")]
crash = notes_abc[percussionname_to_int("Crash Cymbal 1")]
ride = notes_abc[percussionname_to_int("Ride Cymbal 1")]
ride2 = notes_abc[percussionname_to_int("Ride Bell")]
hihat = notes_abc[percussionname_to_int("Pedal Hi Hat")]
openhihat = notes_abc[percussionname_to_int("Open Hi Hat")]
closedhihat = notes_abc[percussionname_to_int("Closed Hi Hat")]
cowbell = notes_abc[percussionname_to_int("Cowbell")]
wood = notes_abc[percussionname_to_int("Hi Wood Block")]
metronome = notes_abc[percussionname_to_int("Metronome Click")]

class DrumsLine:
    def __init__(self):
        pass

    def generate_line(self, song):
        "Probably, the most important piece of code."
        temp = generate_instrument_header('This is the drums line', '3', '10', '0', 
        '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums'])
        )
        if song.style.name == 'swing':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = ride + ' ' + ride + '/> ' + ride + '/ ' + ride + ' ' +  ride + '/> ' + ride + '/ '
            pattern2 = '[' + ride + ' ' + crash +  '] ' + ride + '/> ' + ride + '/ ' + ride + ' ' +  ride + '/> ' + ride + '/ '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
            temp += generate_instrument_header('This is another drums line', '4', '10', '0', 
            '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums']))
            temp.append('z8 ')
            pattern3 = int(song.n_bars)*(' z ' + hihat + ' z ' + hihat)
            for x in range(int(song.n_choruses)):
                temp.append(pattern3)
            temp.append('z4')
        elif song.style.name == 'even_eights':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = ride + ' ' + ride + '/ ' + ride + '/ ' + ride + '/ ' +  ride + ' ' + ride + '/ '
            pattern2 = '[' + ride + ' ' + crash +  '] ' + ride + '/ ' + ride + '/ ' + ride + '/ ' +  ride + ' ' + ride + '/ '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
            temp += generate_instrument_header('This is another drums line', '4', '10', '0', 
            '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums']))
            temp.append('z8 ')
            pattern3 = int(song.n_bars)*('z ' + hihat + ' z ' + hihat)
            for x in range(int(song.n_choruses)):
                temp.append(pattern3)
            temp.append('z4')
        elif song.style.name == 'jazz_waltz':
            header = (metronome + ' ')*6
            temp.append(header)
            pattern1 = ride + ' ' + ride + '/> ' + ride + '/ ' + ride + ' '
            pattern2 = '[' + ride + ' ' + crash +  '] ' + ride + '/> ' + ride + '/ ' + ride + ' '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '3')
            temp += generate_instrument_header('This is another drums line', '4', '10', '0', 
            '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums']))
            temp.append('z6 ')
            pattern3 = int(song.n_bars)*(' z ' + hihat + ' ' + hihat)
            for x in range(int(song.n_choruses)):
                temp.append(pattern3)
            temp.append('z3')
        elif song.style.name == 'waltz':
            header = (metronome + ' ')*6
            temp.append(header)
            pattern1 = '[ ' + bass + ' ' + ride + '] ' + '[ ' + hihat + '/ ' + ride + '/ ]' + bass + '/ ' + '[ ' + hihat + ' ' + ride + '] '
            pattern2 = '[' + bass + ' ' + ride + ' ' + crash +  '] ' + '[ ' + hihat + '/ ' + ride + '/ ]' + bass + '/ ' + '[ ' + hihat + ' ' + ride + '] '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '3')
        elif song.style.name == 'five_swing':
            header = (metronome + ' ')*10
            temp.append(header)
            pattern1 = '[ ' + bass + ride + '] ' + ride + '/> ' + ride + '/ ' + ' ' + ride + ' ' + ride + ' ' + ride + '/> ' + ride + '/ '
            pattern2 = '[' + bass + ride + ' ' + crash +  '] ' + ride + '/> ' + ride + '/ ' + ride + ' ' + ride + ' ' + ride + '/> ' + ride + '/ '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '5')
            temp += generate_instrument_header('This is another drums line', '4', '10', '0', 
            '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums']))
            temp.append('z10 ')
            pattern3 = int(song.n_bars)*(' z ' + hihat + ' ' + hihat + ' z ' + hihat )
            for x in range(int(song.n_choruses)):
                temp.append(pattern3)
            temp.append('z5')
        elif song.style.name == 'five':
            header = (metronome + ' ')*10
            temp.append(header)
            pattern1 = '[ ' + bass + ride + '] ' + ride + '/ ' + ride + '/ ' + ride + ' ' + ride + ' ' + ride + '/ ' + ride + '/ '
            pattern2 = '[' + bass + ride + ' ' + crash +  '] ' + ride + '/ ' + ride + '/ ' + ' ' + ride + ' ' + ride + ' ' + ride + '/ ' + ride + '/ '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '5')
            temp += generate_instrument_header('This is another drums line', '4', '10', '0', 
            '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums']))
            temp.append('z10 ')
            pattern3 = int(song.n_bars)*(' z ' + hihat + ' ' + hihat + ' z ' + hihat )
            for x in range(int(song.n_choruses)):
                temp.append(pattern3)
            temp.append('z5')
        elif song.style.name == 'latin1':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = cowbell + stick + '/ ' + bass + '/ ' + \
            cowbell + '/ ' + stick + '/ ' + 'z/ ' + stick + '/ ' + \
            cowbell + '/ ' + stick + '/ ' + stick + '/ ' + bass + '/ ' + \
            cowbell + '/ ' + stick + '/ ' + 'z/ ' + stick + '/ '
            pattern2 = '[ ' + crash + ' ' + cowbell + ' ]'  + stick + '/ ' + bass + '/ ' + \
            cowbell + '/ ' + stick + '/ ' + 'z/ ' + stick + '/ ' + \
            cowbell + '/ ' + stick + '/ ' + stick + '/ ' + bass + '/ ' + \
            cowbell + '/ ' + stick + '/ ' + 'z/ ' + stick + '/ '
            temp2 = pattern2 + ((int(song.n_bars) - 2)/2)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
        elif song.style.name == 'latin2':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = hihat + '/ ' + closedhihat + '// ' + closedhihat + '// ' + \
            wood + '/ ' + '[ ' + closedhihat + '/ ' + bass + '/ ] ' + \
            stick + '/ ' + '[ ' + closedhihat + '/ ' + bass + '/ ] ' + \
            closedhihat + '/ ' + openhihat + '/ ' + \
            '[ ' + wood + '/ ' + hihat + '/ ] ' + closedhihat + '/ ' + \
            closedhihat + '/ ' + '[ ' + closedhihat + '/ ' + bass + '/ ' + wood + '/ ] ' + \
            'z/ ' + closedhihat + '/ ' + \
            '[ ' + bass + '/ ' + wood + '/ ] ' + openhihat + '/ '
            pattern2 = '[ ' + hihat + '/ ' + crash + '/ ]' + closedhihat + '// ' + closedhihat + '// ' + \
            wood + '/ ' + '[ ' + closedhihat + '/ ' + bass + '/ ] ' + \
            stick + '/ ' + '[ ' + closedhihat + '/ ' + bass + '/ ] ' + \
            closedhihat + '/ ' + openhihat + '/ ' + \
            '[ ' + wood + '/ ' + hihat + '/ ] ' + closedhihat + '/ ' + \
            closedhihat + '/ ' + '[ ' + closedhihat + '/ ' + bass + '/ ' + wood + '/ ] ' + \
            'z/ ' + closedhihat + '/ ' + \
            '[ ' + bass + '/ ' + wood + '/ ] ' + openhihat + '/ '
            temp2 = pattern2 + ((int(song.n_bars) - 2)/2)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
        elif song.style.name == 'bossa':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = '[ ' + bass + ' ' + stick  + ' ]' + hihat + '/ ' + '[ ' + bass + '/ ' + stick  + '/ ]'  + \
            bass + ' [ ' + hihat + '/ ' + stick  + '/ ]'+ bass + '/ ' + \
            bass + ' ' + '[ ' + hihat + '/ ' + stick + '/ ]' + bass + '/ ' +  \
            '[ ' + bass + ' ' + stick  + ' ]'  + hihat + '/ ' + bass + '/ ' 
            pattern2 = '[ ' + crash + ' ' + bass + ' ' + stick  + ' ]' + hihat + '/ ' + '[ ' + bass + '/ ' + stick  + '/ ]'  + \
            bass + ' [ ' + hihat + '/ ' + stick  + '/ ]'+ bass + '/ ' + \
            bass + ' ' + '[ ' + hihat + '/ ' + stick + '/ ]' + bass + '/ ' +  \
            '[ ' + bass + ' ' + stick  + ' ]'  + hihat + '/ ' + bass + '/ ' 
            temp2 = pattern2 + ((int(song.n_bars) - 2)/2)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
        elif song.style.name == 'samba1' or song.style.name == 'samba2':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + ride + '/ ' + \
            '[ ' + hihat + '/ ' + stick + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + ride + '/ ]' + \
            '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + ride + '/ ' + \
            '[ ' + hihat + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + \
            '[ ' + bass + '/ ' + ride + '/ ]' + '[ ' + ride + '/ ' + stick + '/ ]' + \
            '[ ' + hihat + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + \
            '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + ride + '/ ' + \
            '[ ' + hihat + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + ride + '/ ]'
            pattern2 = '[ ' + crash + '/ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + ride + '/ ' + \
            '[ ' + hihat + '/ ' + stick + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + ride + '/ ]' + \
            '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + ride + '/ ' + \
            '[ ' + hihat + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + \
            '[ ' + bass + '/ ' + ride + '/ ]' + '[ ' + ride + '/ ' + stick + '/ ]' + \
            '[ ' + hihat + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + \
            '[ ' + bass + '/ ' + stick + '/ ' + ride + '/ ]' + ride + '/ ' + \
            '[ ' + hihat + '/ ' + ride + '/ ]' + '[ ' + bass + '/ ' + ride + '/ ]'
            temp2 = pattern2 + ((int(song.n_bars) - 2)/2)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
            pass
        elif song.style.name == 'ballad':
            # Like swing, with a stick hit in 4th part
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = ride + ' ' + ride + '/> ' + ride + '/ ' + ride + ' ' +  ride + '/> ' + ride + '/ '
            pattern2 = '[' + ride + ' ' + crash +  '] ' + ride + '/> ' + ride + '/ ' + ride + ' ' +  ride + '/> ' + ride + '/ '
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
            temp += generate_instrument_header('This is another drums line', '4', '10', '0', 
            '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['drums']))
            temp.append('z8 ')
            pattern3 = int(song.n_bars)*(' z ' + hihat + ' z ' + '[ ' + hihat + ' ' + stick + ' ]')
            for x in range(int(song.n_choruses)):
                temp.append(pattern3)
            temp.append('z4')
        elif song.style.name == 'funk':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' + closedhihat + '//' + closedhihat + '//' + \
            '[ ' + snare + '// ' + closedhihat + '// ]' + closedhihat + '//' + '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' + \
            closedhihat + '//' + closedhihat + '//' + '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' + \
            '[ ' + snare + '// ' + closedhihat + '// ]' + closedhihat + '//' + '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' 
            pattern2 = '[ ' + crash + '// ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' + closedhihat + '//' + closedhihat + '//' + \
            '[ ' + snare + '// ' + closedhihat + '// ]' + closedhihat + '//' + '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' + \
            closedhihat + '//' + closedhihat + '//' + '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' + \
            '[ ' + snare + '// ' + closedhihat + '// ]' + closedhihat + '//' + '[ ' + bass + '// ' + closedhihat + '// ]' + closedhihat + '//' 
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
        elif song.style.name == 'rock':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = '[ ' + bass + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + bass + '/ ' + closedhihat + '/ ]' + '[ ' + bass + '/ ' + closedhihat + '/ ]' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + bass + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + bass + '/ ' + closedhihat + '/ ]' + '[ ' + bass + '/ ' + closedhihat + '/ ]' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + openhihat + '/' 
            pattern2 = '[ ' + crash + '/ ' + bass + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + bass + '/ ' + closedhihat + '/ ]' + '[ ' + bass + '/ ' + closedhihat + '/ ]' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + bass + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + closedhihat + '/' + \
            '[ ' + bass + '/ ' + closedhihat + '/ ]' + '[ ' + bass + '/ ' + closedhihat + '/ ]' + \
            '[ ' + snare + '/ ' + closedhihat + '/ ]' + openhihat + '/' 
            temp2 = pattern2 + ((int(song.n_bars) - 2)/2)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
        elif song.style.name == 'basic':
            header = metronome + ' z ' + metronome + ' z ' + (metronome + ' ')*4
            temp.append(header)
            pattern1 = bass + ' ' + stick + ' ' + bass + ' ' + stick + ' '
            pattern2 = '[' + bass + ' ' + crash +  '] ' + stick + ' ' + bass + ' ' + stick + ' ' 
            temp2 = pattern2 + (int(song.n_bars) - 1)*pattern1
            for x in range(int(song.n_choruses)):
                temp.append(temp2)
            temp.append(crash + '4')
        else:
            raise MyException(_("Style not found"))
        #~ print temp
        return temp
        
if __name__ == '__main__':
    from song import *
    example_input = ['32CM']
    s = Song( 'test', 'Test Song', '140', 'C', even_eights, example_input, '8', '2', ['drums'])
    final = s.generate_song()
    abc_file = open('DELETE_ME.abc', 'w')
    for l in final:
        abc_file.write(l + "\n")
    abc_file.close()
    import os
    os.system('abc2midi DELETE_ME.abc -o DELETE_ME.mid')
    os.system('timidity -ig  DELETE_ME.mid')
    os.system('rm -Rf DELETE_ME*')
