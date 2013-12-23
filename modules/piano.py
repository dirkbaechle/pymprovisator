#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

from constants import *
import preferences, song
import gettext, random


_ = gettext.gettext

class PianoLine:
    def __init__(self, instrument):
        self.instrument = instrument
        
    def generate_line(self, song):
        "Probably, the most important piece of code."
        meter = song.style.meter[0]
        temp = generate_instrument_header('This is the piano line', '2', '2', 
               str(instrument_names.index(self.instrument)), 
               '%%MIDI control 10 127', 
               '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['piano'])
               )
        temp.append('z' + str(int(meter)*2))
        style_name = song.style.name
        if style_name == 'basic':
            aux = ''
            for ch in song.chord_item_collection:
                aux += piano_chord(ch.chord, ch.parts)
            for x in range(int(song.n_choruses)):
                temp.append(aux)
            ch = song.chord_item_collection[0]
            temp.append(piano_chord(ch.chord, '4'))
        else:
            aux = ''
            for ch in song.chord_item_collection:
                aux += patterns_generator(ch.chord, ch.parts, style_name, meter)
            for x in range(int(song.n_choruses)):
                temp.append(aux)
            ch = song.chord_item_collection[0]
            temp.append(piano_chord(ch.chord, meter))
        #~ print temp
        return temp

def patterns_generator(chord, parts, style, meter):
    iparts = int(parts)
    #~ print chord
    # style: string -> Walking bass
    if style == 'swing' or style == 'jazz_waltz' or style == 'five_swing':
        """abcMIDI does not support "broken" rythms in chords ex.: [A/> C/> E/> A/ C/ E/]
        Let's use a trick: a quarter note = 16 sixteen notes. Thus, we can aproximate:
        two swing eights notes = 10/16 and 6/16 = 16/16 = 1 quarter note.
        It's strange, but sounds well!"""
        temp1 = piano_chord(chord, '10/16')  # eight note, with swing
        temp2 = piano_chord(chord, '6/16')  # second eight note, with swing
        temp3 = piano_chord(chord, '1')
        temp4 = piano_chord(chord, '2')
        temp5 = piano_chord(chord, '54/16')
        temp6 = piano_chord(chord, '38/16')
        temp7 = piano_chord(chord, '22/16')
        if iparts == 1:
            return temp3
        elif iparts == 2:
            pat1 = temp1 + 'z6/16' + temp1 + 'z6/16'
            pat2 = 'z ' + temp3
            pat3 = temp1 + ' z6/16 ' + ' z10/16 ' + temp2 
            pat4 = 'z  z10/16 ' + temp2
            pat5 = temp1 + temp2 + 'z'
            return random.choice([pat1, pat2, pat3, pat4, pat5])
        elif iparts == 3:
            pat1 = temp1 + ' z6/16 ' + ' z10/16 ' + temp2 + 'z'
            pat2 = temp1 + temp6
            pat3 = 'z10/16' + temp6
            pat4 = temp4 + temp3
            pat5 = temp3 + temp1 + temp7
            return random.choice([pat1, pat2, pat3, pat4, pat5])
        elif iparts == 4:
            pat1 = temp1 + ' z6/16 ' + ' z10/16 ' + temp2 + 'z2'
            pat2 = temp1 + temp5
            pat3 = temp1 + temp2 + 'z' + temp3 + 'z'
            pat4 = temp1 + 'z6/16 z10/16 ' + temp6
            pat5 = 'z' + temp3 + temp1 + temp2 + 'z'
            return random.choice([pat1, pat2, pat3, pat4, pat5])
        elif iparts == 5:
            pat1 = temp1 + ' z6/16 ' + ' z10/16 ' + temp2 + 'z2' + temp3
            pat2 = temp1 + temp5 + temp3
            pat3 = temp1 + temp2 + 'z' + temp3 + temp4
            pat4 = temp1 + 'z6/16 z10/16 ' + temp6 + 'z'
            pat5 = 'z' + temp3 + temp1 + temp2 + 'z' + temp3
            return random.choice([pat1, pat2, pat3, pat4, pat5])
        elif iparts > 5:
            aux = ''
            imeter = int(meter)
            multiplier, parts2 = split_long_chords(iparts, imeter)
            if imeter == 3:
                aux += multiplier*(temp3 + temp1 + temp7)
            elif imeter == 4:
                aux += multiplier*(temp1 + 'z6/16 z10/16 ' + temp6)
            elif imeter == 5:
                aux += multiplier*(temp1 + temp2 + 'z' + temp3 + temp4)
            if parts2 == 1:
                aux += temp3
            elif parts2 == 2:
                aux += temp4
            elif parts2 == 3:
                aux += (temp4 + 'z')
            elif parts2 == 4:
                aux += (temp4 + 'z2')
            return aux
    elif style == 'ballad':
        pat1 = piano_chord(chord, '1')
        pat2 = piano_chord(chord, '2')
        pat3 = piano_chord(chord, '3')
        pat4a = piano_chord(chord, '4')
        pat4b = piano_chord(chord, '2') + piano_chord(chord, '2')
        pat4c = piano_chord(chord, '1') + piano_chord(chord, '2') + piano_chord(chord, '1')
        pat4d = piano_chord(chord, '1') + piano_chord(chord, '3')
        pat4e = piano_chord(chord, '3') + piano_chord(chord, '1')
        aux = ''
        if iparts > 4:
            imeter = int(meter)
            multiplier, parts2 = split_long_chords(iparts, imeter)
            aux += multiplier*(random.choice([pat4a, pat4b, pat4c, pat4d, pat4e]))
            aux += eval("pat" + str(parts2))
        elif iparts == 4:
            aux += random.choice([pat4a, pat4b, pat4c, pat4d, pat4e])
        else:
            aux += eval("pat" + parts)
        return aux
    elif style == 'even_eights' or style == 'waltz' or style == 'five' \
         or style == 'rock' or style == 'funk' or style == 'bossa' or \
         style == 'samba1' or style == 'latin1':
        pat1a = piano_chord(chord, '1')
        pat1b = piano_chord(chord, '/') + piano_chord(chord, '/')
        pat2a = piano_chord(chord, '2')
        pat2b = piano_chord(chord, '/') + piano_chord(chord, '/') + 'z '
        pat2c = piano_chord(chord, '/') + piano_chord(chord, '1') + piano_chord(chord, '/')
        pat3a = piano_chord(chord, '3')
        pat3b = piano_chord(chord, '2') + piano_chord(chord, '/') + 'z/ '
        pat3c = piano_chord(chord, '1') + piano_chord(chord, '2')
        pat3d = piano_chord(chord, '/') + piano_chord(chord, '5/2')
        pat3e = piano_chord(chord, '/') + piano_chord(chord, '/') + 'z ' + piano_chord(chord, '/') + 'z/ '
        pat4a = piano_chord(chord, '2') + piano_chord(chord, '2')
        pat4b = piano_chord(chord, '1') + piano_chord(chord, '2') + piano_chord(chord, '1')
        pat4c = piano_chord(chord, '1') + 'z ' + piano_chord(chord, '1') + piano_chord(chord, '1')
        pat4d = piano_chord(chord, '1') + 'z/ ' + piano_chord(chord, '1') + 'z/ ' + piano_chord(chord, '1')
        pat4e = piano_chord(chord, '/') + piano_chord(chord, '/') + 'z2 ' + piano_chord(chord, '1')
        pat4f = piano_chord(chord, '1') + 'z ' + piano_chord(chord, '/') + piano_chord(chord, '/') + 'z '
        pat5a = piano_chord(chord, '3') + piano_chord(chord, '2')
        pat5b = piano_chord(chord, '2') + piano_chord(chord, '2') + piano_chord(chord, '1')
        pat5c = piano_chord(chord, '1') + 'z ' + piano_chord(chord, '1') + piano_chord(chord, '2')
        pat5d = piano_chord(chord, '/') + piano_chord(chord, '/') + 'z ' + piano_chord(chord, '/') + \
        'z/ ' + 'z ' + piano_chord(chord, '1')
        pat5e = piano_chord(chord, '/') + piano_chord(chord, '1') + piano_chord(chord, '/') + piano_chord(chord, '/') + \
        'z/ ' + piano_chord(chord, '1') + piano_chord(chord, '1')   # Thank's, Dave Brubeck  ;-)

        aux = ''
        if iparts == 1:
            aux += random.choice([pat1a, pat1b])
        elif iparts == 2:
            aux += random.choice([pat2a, pat2b, pat2c])
        elif iparts == 3:
            aux += random.choice([pat3a, pat3b, pat3c, pat3d, pat3e])
        elif iparts == 4:
            aux += random.choice([pat4a, pat4b, pat4c, pat4d, pat4e, pat4f])
        elif iparts == 5:
            aux += random.choice([pat5a, pat5b, pat5c, pat5d, pat5e])
        elif iparts > 5:
            imeter = int(meter)
            multiplier, parts2 = split_long_chords(iparts, imeter)
            if imeter == 3:
                aux += multiplier*(random.choice([pat3a, pat3b, pat3c, pat3d, pat3e]))
            elif imeter == 4:
                aux += multiplier*(random.choice([pat4a, pat4b, pat4c, pat4d, pat4e, pat4f]))
            elif imeter == 5:
                aux += multiplier*(random.choice([pat5a, pat5b, pat5c, pat5d, pat5e]))
            if parts2 == 1:
                aux += random.choice([pat1a, pat1b])
            elif parts2 == 2:
                aux += random.choice([pat2a, pat2b, pat2c])
            elif parts2 == 3:
                aux += random.choice([pat3a, pat3b, pat3c, pat3d, pat3e])
            elif parts2 == 4:
                aux += random.choice([pat4a, pat4b, pat4c, pat4d, pat4e, pat4f])
        return aux
    elif style == 'latin2' or style == 'samba2':
        # Let's try a "tumbao" ...
        notes_1 = [notes_abc[i-12] for i in chord.arpeggio]
        notes_2 = [notes_abc[i + 12] for i in chord.arpeggio]
        pat1 = '[ ' + notes_1[0] + '/ ' + notes_2[0] + '/ ]' + '[ ' + notes_1[2] + '/ ' + notes_2[2] + '/ ]'
        pat2 = '[ ' + notes_1[0] + '/ ' + notes_2[0] + '/ ]' + \
               '[ ' + notes_1[1] + ' ' + notes_2[1] + ' ]' + \
               '[ ' + notes_1[2] + '/ ' + notes_2[2] + '/ ]' 
        pat3 = '[ ' + notes_1[0] + '/ ' + notes_2[0] + '/ ]' + \
               '[ ' + notes_1[1] + ' ' + notes_2[1] + ' ]' + \
               '[ ' + notes_1[2] + ' ' + notes_2[2] + ' ]' + \
               '[ ' + notes_1[1] + '/ ' + notes_2[1] + '/ ]'
        pat4 = '[ ' + notes_1[0] + '/ ' + notes_2[0] + '/ ]' + \
               '[ ' + notes_1[1] + ' ' + notes_2[1] + ' ]' + \
               '[ ' + notes_1[2] + ' ' + notes_2[2] + ' ]' + \
               '[ ' + notes_1[1] + ' ' + notes_2[1] + ' ]' + \
               '[ ' + notes_1[2] + '/ ' + notes_2[2] + '/ ]'
        aux = ''
        if iparts > 4:
            imeter = int(meter)
            multiplier, parts2 = split_long_chords(iparts, imeter)
            aux += multiplier*(pat4)
            aux += eval("pat" + str(parts2))
        else:
            aux += eval("pat" + parts)
        return aux

    else:
        pass



def piano_chord(chord, parts):
    return '[' + ' '.join([elem + parts for elem in chord.generate_abc_arpeggio()]) + '] '
    


def piano_arpeggio(chord, parts):
    iparts = int(parts)
    if iparts == 1:
        return piano_chord(chord, parts)
    else:
        arpeggio = chord.generate_abc_arpeggio()
        temp = ''
        for n in arpeggio:
            temp += n + '// '
        dif = str(16*iparts - 4*len(arpeggio)) + '/16'
        return temp + ' [' + ' '.join([elem + dif for elem in arpeggio]) + '] '

def split_long_chords(duration, meter=4):
    Q, R = divmod(duration, meter)
    return (Q, R)

if __name__ == '__main__':
    # Testing code ...
    from song import *
    example_input = ['4cm9', '4cm7', '4fm7', '3fm7', '1a7' , '4dm7b5', '4g7', '4cm6', '4cm7', 
    '4ebm7', '4ab7', '4dbmaj7', '4dbmaj7', '4dm7b5', '4g7', '4cm6', '2dm7b5', '2g7alt']
    s = Song( 'test', 'Test Song', '230', 'C', samba1, example_input, '16', '2', ['bass', 'drums', 'piano'])

    #~ example_input = ['6cm7', '3fm7', '2fm7', '1a7' , '3dm7b5', '3g7', '3cm6', '3cm7', '3ebm7', '3ab7', 
    #~ '6dbmaj7', '3dm7b5', '3g7', '3cm6', '2dm7b5', '1g7alt']
    #~ s = Song( 'test', 'Test Song', '140', 'C', waltz, example_input, '16', '2',  ['bass', 'drums', 'piano'])
    
    #~ example_input = ['6cm7', '4cm6', '5fm7', '3fm7', '2a7' , '5dm7b5', '5g7', '5cm6', '5cm7', 
    #~ '5ebm7', '5ab7', '5dbmaj7', '5dbmaj7', '5dm7b5', '5g7', '5cm6', '3dm7b5', '2g7alt']
    #~ s = Song( 'test', 'Test Song', '130', 'C', five, example_input, '16', '2', ['bass', 'drums', 'piano'])
    
    #~ final = s.generate_song({'bass': 'Fretless Bass', 'piano': 'Rock Organ'})
    final = s.generate_song()
    abc_file = open('DELETE_ME.abc', 'w')
    for l in final:
        abc_file.write(l + "\n")
    abc_file.close()
    import os
    os.system('abc2midi DELETE_ME.abc -v -o DELETE_ME.mid')
    os.system('mplay32 DELETE_ME.mid')
    os.system('rm -Rf DELETE_ME*')
    #~ print split_long_chord(130, 4)
