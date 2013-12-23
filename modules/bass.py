#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

from constants import *
import preferences

class BassLine:
    def __init__(self, instrument):
        self.instrument = instrument

    def generate_line(self, song):
        "Probably, the most important piece of code."
        meter = song.style.meter[0]
        temp = generate_instrument_header('This is the bass line', '1', '1', 
               str(instrument_names.index(self.instrument)), 
               'I:clef=bass octave=-2', '%%MIDI control 10 1', 
               '%%MIDI control 7 ' + str(preferences.get_prefered_volume()['bass'])
               )
        if song.style.name == 'swing':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                parts = int(ch.parts)
                bass_line += walking_pattern(ch, parts, int(meter))
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'even_eights':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                parts = int(ch.parts)
                bass_line += walking_pattern(ch, parts, int(meter))
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'jazz_waltz':
            temp.append('z6')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                parts = int(ch.parts)
                bass_line += walking_pattern(ch, parts, int(meter))
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'waltz':
            temp.append('z6')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + ' ' + note2 + ' '
                elif parts == 3:
                    bass_line += note1 + '2 ' + note2 + ' '
                elif parts > 3:
                    multiplier, parts2 = split_long_chord(parts, 3)
                    bass_line += multiplier*(note1 + '2 ' + note2 + ' ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + ' ' + note2 + ' '
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'five_swing':
            temp.append('z10')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                parts = int(ch.parts)
                bass_line += walking_pattern(ch, parts, int(meter))
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
            pass
        elif song.style.name == 'five':
            temp.append('z10')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + ' ' + note2 + ' '
                elif parts == 3:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 '
                elif parts == 4:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 ' + note1 + ' '
                elif parts == 5:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 ' + note1 + ' ' + note2 + ' '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 5)
                    bass_line += multiplier*(note1 + '3/2 ' + note2 + '3/2 ' + note1 + ' ' + note2 + ' ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + ' ' + note2 + ' '
                    elif parts2 == 3:
                        bass_line += note1 + '3/2 ' + note2 + '3/2 '
                    elif parts2 == 4:
                        bass_line += note1 + '3/2 ' + note2 + '3/2 ' + note1 + ' '
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'latin1':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                note3 = notes_abc[ch.chord.root + 12] # 8th
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + ' ' + note3 + '/ ' + note2 + '/ '
                elif parts == 3:
                    bass_line += note1 + '3/2 ' + note3 + '/ ' + note2 + ' '
                elif parts == 4:
                    bass_line += note1 + '/ ' + note3 + ' ' + note2 + '/ ' + note1 + ' ' + note2 + '/ ' + note3 + '/ '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '/ ' + note3 + ' ' + note2 + '/ ' + note1 + ' ' + note2 + '/ ' + note3 + '/ ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + ' ' + note3 + '/ ' + note2 + '/ '
                    elif parts2 == 3:
                        bass_line += note1 + '3/2 ' + note3 + '/ ' + note2 + ' '
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'latin2':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                note3 = notes_abc[ch.chord.root + 12] # 8th
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + ' ' + note1 + ' '
                elif parts == 3:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 '
                elif parts == 4:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 ' + note3 + ' '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '3/2 ' + note2 + '3/2 ' + note3 + ' ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + ' ' + note2 + ' '
                    elif parts2 == 3:
                        bass_line += note1 + '3/2 ' + note2 + '3/2 '
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'bossa':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + '3/2 ' + note1 + '/ '
                elif parts == 3:
                    bass_line += note1 + '3/2 ' + note1 + '/ ' + note2
                elif parts == 4:
                    bass_line += note1 + '3/2 ' + note1 + '/ ' + note2 + '3/2 ' + note2 + '/ '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '3/2 ' + note1 + '/ ' + note2 + '3/2 ' + note2 + '/ ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + '3/2 ' + note1 + '/ '
                    elif parts2 == 3:
                        bass_line += note1 + '3/2 ' + note1 + '/ ' + note2
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'samba1' or song.style.name == 'samba2':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + '3/2 ' + note1 + '/ '
                elif parts == 3:
                    bass_line += note1 + '3/2 ' + note1 + '/ ' + note2
                elif parts == 4:
                    bass_line += note1 + '3/2 ' + note1 + '/ ' + note2 + '3/2 ' + note2 + '/ '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '3/2 ' + note1 + '/ ' + note2 + '3/2 ' + note2 + '/ ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + '3/2 ' + note1 + '/ '
                    elif parts2 == 3:
                        bass_line += note1 + '3/2 ' + note1 + '/ ' + note2
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'ballad':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + '2 '
                elif parts == 3:
                    bass_line += note1 + '2 ' + note2 + ' '
                elif parts == 4:
                    bass_line += note1 + '2 ' + note2 + '2 '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '2 ' + note2 + '2 ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + '2 '
                    elif parts2 == 3:
                        bass_line += note1 + '2 ' + note2 + ' '
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'funk':
            # Copy & Paste from H. Hancock's 'Cantaloupe island' ;-)
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][4]]  # 5th note of chord
                note3 = notes_abc[ch.chord.root + escale_notes[ch.chord.type][6]]  # 7th note of chord
                note4 = notes_abc[ch.chord.root + 12] # 8th
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + ' '
                elif parts == 2:
                    bass_line += note1 + '3/2 ' + note2 + '/ '
                elif parts == 3:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 '
                elif parts == 4:
                    bass_line += note1 + '3/2 ' + note2 + '3/2 ' + note3 + '/ ' + note4 + '/ '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '3/2 ' + note2 + '3/2 ' + note3 + '/ ' + note4 + '/ ')
                    if parts2 == 1:
                        bass_line += note1 + ' '
                    elif parts2 == 2:
                        bass_line += note1 + ' ' + note2 + ' '
                    elif parts2 == 3:
                        bass_line += note1 + '3/2 ' + note2 + '/ '
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'rock':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_line = ''
                note1 = notes_abc[ch.chord.root]
                note2 = notes_abc[ch.chord.root - escale_notes[ch.chord.type][3]]  # 5th note of chord, descending
                parts = int(ch.parts)
                if parts == 1:
                    bass_line += note1 + '/ ' + note2 + '/ ' 
                elif parts == 2:
                    bass_line += note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note2 + '/ '
                elif parts == 3:
                    bass_line += note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note2 + '/ ' 
                elif parts == 4:
                    bass_line += note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note2 + '/ '
                elif parts > 4:
                    multiplier, parts2 = split_long_chord(parts, 4)
                    bass_line += multiplier*(note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note2 + '/ ')
                    if parts2 == 1:
                        bass_line += note1 + '/ ' + note2 + '/ ' 
                    elif parts2 == 2:
                        bass_line += note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note2 + '/ '
                    elif parts2 == 3:
                        bass_line += note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note1 + '/ ' + note2 + '/ ' 
                temp2.append(bass_line)
            temp += int(song.n_choruses)*temp2
        elif song.style.name == 'basic':
            temp.append('z8')
            temp2 = []
            for ch in song.chord_item_collection:
                bass_note = notes_abc[ch.chord.root]
                temp2 += [bass_note]*int(ch.parts)
            for x in range(int(song.n_choruses)):
                temp.append(" ".join(temp2))
        else:
            raise MyException("Style not found")
        temp.append(notes_abc[song.chord_item_collection[0].chord.root] + meter)
        return temp
        
def split_long_chord(parts, unit):
    result = Q, R = divmod(parts, unit)
    return result

def get_distance(chord1, chord2):
    if  str(chord2) == 'None':
        return 'unison'
    r1 = chord1.root % 12
    r2 = chord2.root % 12
    distance = abs(r1 - r2)
    if distance == 0:
        return 'unison'
    elif 1 <= distance <= 2:
        return '2nd'
    elif 3 <= distance <= 4:
        return '3rd'
    elif 4 <= distance <= 5:
        return '4th'
    elif 6 <= distance <= 7:
        return '5th'
    elif 8 <= distance <= 9:
        return '6th'
    elif 10 <= distance <= 11:
        return '7th'
    else:
        raise MyException(_("Error calculating distance between chords."))

def walking_pattern(ch, parts, meter):
    pattern_unison = (
        (1, 5),
        (1, 5, 3),
        (1, 3, 5, 7),
        (1, 3, 5, 7, 5),
        (1, 3, 5, 7, 5, 3), 
        (1, 3, 5, 7, 5, 3, 5), 
        (1, 3, 5, 7, 5, 3, 5, 3),
        (1, 3, 5, 7, 5, 3, 2, 1, 3),
        (1, 3, 5, 7, 5, 3, 1, 3, 5, 7, 5, 3),
    )
    pattern_2nd = (
        (1, 3),                          # 2 parts -> first and third notes of the chord.
        (1, 2, 3),                       # 3 parts -> first, second and third.
        (1, 2, 3, 1),                    # and so on...
        (1, 2, 3, 1, 3),
        (1, 2, 3, 5, 3, 1), 
        (1, 2, 3, 5, 3, 2, 1), 
        (1, 2, 3, 4, 5, 3, 2, 1),
        (1, 2, 3, 1, 3, 1, 2, 3, 1),
        (1, 2, 3, 1, 3, 1, 2, 3, 1, 3),
    )
    pattern_3rd = (
        (1, 2),
        (1, 3, 2),
        (1, 5, 3, 2),
        (1, 3, 5, 3, 2),
        (1, 2, 3, 5, 3, 2), 
        (1, 2, 3, 5, 1, 3, 2), 
        (1, 2, 3, 4, 5, 3, 1, 2),
        (1, 2, 3, 4, 5, 3, 2, 1, 2),
        (1, 2, 3, 4, 5, 3, 5, 3, 2),
    )
    pattern_4th = (
        (1, 5),
        (1, 3, 5),
        (1, 2, 3, 5),
        (1, 2, 3, 1, 5),
        (1, 2, 3, 1, 3, 5), 
        (1, 2, 3, 5, 1, 3, 5), 
        (1, 2, 3, 2, 1, 2, 3, 5),
        (1, 2, 3, 4, 5, 3, 2, 1, 5),
        (1, 2, 3, 4, 5, 3, 2, 1, 3, 5),
    )
    pattern_5th = (
        (1, 3),
        (1, 5, 3),
        (1, 3, 5, 3),
        (1, 2, 3, 5, 3),
        (1, 2, 3, 5, 1, 3), 
        (1, 2, 3, 5, 1, 5, 3), 
        (1, 2, 3, 5, 1, 3, 5, 3),
        (1, 2, 3, 5, 3, 1, 3, 5, 3),
        (1, 2, 3, 5, 3, 1, 2, 3, 5, 3),
    )
    pattern_6th = (
        (1, 7),
        (1, 5, 7),
        (1, 3, 5, 7),
        (1, 2, 3, 5, 7),
        (1, 2, 3, 5, 3, 7), 
        (1, 2, 3, 5, 1, 5, 7), 
        (1, 2, 3, 5, 1, 3, 5, 7),
        (1, 2, 3, 5, 3, 1, 3, 5, 7),
        (1, 2, 3, 5, 3, 1, 2, 3, 5, 7),
    )
    pattern_7th = (
        (1, 5),
        (1, 5, 1),
        (1, 2, 3, 1),
        (1, 2, 3, 5, 1),
        (1, 2, 3, 5, 3, 1), 
        (1, 2, 3, 5, 1, 5, 1), 
        (1, 2, 3, 5, 1, 5, 3, 1),
        (1, 2, 3, 5, 3, 1, 3, 5, 1),
        (1, 2, 3, 5, 3, 1, 5, 3, 2, 1),
    )
    chord = ch.chord
    n_chord = ch.next_chord
    base_note = chord.root
    distance = get_distance(chord, n_chord)
    pattern = eval('pattern_' + distance)
    if parts < 1: raise MyException(_("Error in given parts. You must supply a value greater than 0."))
    if parts == 1:
        return notes_abc[base_note] + ' '
    elif 2 <= parts <= 10:
        return ' '.join([notes_abc[base_note + escale_notes[chord.type][i -1]] for i in pattern[parts-2]])
    else:
        aux = ''
        multiplier, parts2 = split_long_chord(parts, meter)
        aux += multiplier*(' '.join([notes_abc[base_note + escale_notes[chord.type][i -1]] for i in pattern[meter-2]]))
        if parts2 == 1:
            aux += notes_abc[base_note] + ' '
        elif 2 <= parts2 <= 10:
            aux += ' '.join([notes_abc[base_note + escale_notes[chord.type][i -1]] for i in pattern[parts2-2]])
        return aux

if __name__ == '__main__':
    from song import *
    example_input = ['4cm7', '4cm7', '4fm7', '3fm7', '1a7' , '4dm7b5', '4g7', '4cm6', '4cm7', '4ebm7', '4ab7', 
    '4dbmaj7', '4dbmaj7', '4dm7b5', '4g7', '4cm6', '2dm7b5', '2g7alt']
    s = Song( 'test', 'Test Song', '130', 'C', even_eights, example_input, '16', '2', ['bass', 'drums'])
    #~ example_input = ['6cm7', '3fm7', '2fm7', '1a7' , '3dm7b5', '3g7', '3cm6', '3cm7', '3ebm7', '3ab7', 
    #~ '6dbmaj7', '3dm7b5', '3g7', '3cm6', '2dm7b5', '1g7alt']
    #~ s = Song( 'test', 'Test Song', '140', 'C', jazz_waltz, example_input, '16', '2', ['bass', 'drums'])
    final = s.generate_song()
    abc_file = open('DELETE_ME.abc', 'w')
    for l in final:
        abc_file.write(l + "\n")
    abc_file.close()
    import os
    os.system('abc2midi DELETE_ME.abc -o DELETE_ME.mid')
    os.system('timidity -ig DELETE_ME.mid')
    os.system('rm -Rf DELETE_ME*')
    #~ print split_long_chord(130, 4)
