#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

from constants import *
import gettext

_ = gettext.gettext

class Chord:
  """Represents a chord. The format is: X[y]Z
      X: Root of the chord: C, D, E, F, G, A or B
      y: b | # Optional. Flat or sharp.
      Z: Chord's type:
        'M', '6', 'maj7', 'maj9', 'maj13', 'm', , 'm6', 'm7', 'm9', 'm11', 'susb9', '#11', 'maj7#11',
        '7', '9', '13', '11', 'sus', 'sus7', 'sus9', 'sus13', 'mb6', 'm7b6', 'm7b5',
        'mmaj7', 'mmaj9', '+maj7', 'maj7+5', 'alt', '+', '+7', 'º', 'º7', 'dism', '7b9', '7b5'
    """
  def __init__(self, chord_name):
    """Chord attributes: 'name', 'root', 'rt', 'type', 'tp', """
    if chord_name.strip() == "":
        raise MyException(_("Not chord given"))
    self.name = chord_name[0].upper() + chord_name[1:]
    if not self.name[0] in ['A','B','C','D','E','F','G']:
        raise MyException(_("Chord not valid -> Root not valid: ") + self.name[0])
    else:
      #print self.name
      if len(self.name) > 1:
        if self.name[1] == 'b':
          pointer = 2
          root = -1
        elif self.name[1] == '#':
          pointer = 2
          root = 1
        else:
          pointer = 1
          root = 0
      else:
        pointer = 0
        root = 0
      #First, we set the root
      if self.name[0] == 'G':
        self.root = 55 + root
      elif self.name[0] == 'A':
        self.root = 57 + root
      elif self.name[0] == 'B':
        self.root = 59 + root
      elif self.name[0] == 'C':
        self.root = 60 + root
      elif self.name[0] == 'D':
        self.root = 62 + root
      elif self.name[0] == 'E':
        self.root = 64 + root
      if self.name[0] == 'F':
        self.root = 65 + root
      #Second, we set the chord quality
      if pointer:
        self.tp = self.name[pointer:]  # ex: 7#11
        temp = [v for (k,v) in chord_escale.items() if k == self.tp]
        if temp:
          self.type = temp[0] # ex: 'lidian-dominant'
        else:
            raise MyException(_("Chord not valid: ") + chord_name + _(" -> Chord type not found"))
      else:
        self.tp = 'M'
        self.type = "ionian"
      self.rt = self.name[:pointer]
      if not self.tp in chord_arpeggio.keys(): raise MyException(_("Unknown chord")+": "+self.tp)
      self.scale = []
      for note in escale_notes[self.type]:
          self.scale.append(note + self.root)
      self.arpeggio = []
      for note in chord_arpeggio[self.tp]:
          self.arpeggio.append(note + self.root)


  #~ def __cmp__(self, chord2):
    #~ if self.root == chord2.root:
      #~ return 0
    #~ elif self.root < chord2.root:
      #~ return -1
    #~ elif self.root > chord2.root:
      #~ return 1
  def __str__(self):
    return "%s chord root = %s (%s), chord type = %s (%s)" % \
           (self.name, self.root, self.rt, self.type, self.tp,)
  def generate_abc_scale(self):
    """Returns a list containing the appropiated notes for the current chord in ABC format."""
    return [notes_abc[i] for i in self.scale]
  def generate_abc_arpeggio(self):
    """Returns a list containing the arpeggio notes for the current chord in ABC format."""
    return [notes_abc[i] for i in self.arpeggio]
    

class ChordItem:
    """This class is like a double linked list node. Contains an object 'Chord'
        and references to previous and next chord.
        __init__(self, chord_string, prev=None, next=None)
        Class attributes:
        prev_parts, prev_chord, next_parts, next_chord, parts, chord"""
    def __init__(self, chord_string, prev=None, next=None):
        """Chord string is like XZ, X: parts. Z: chord. Ex: 4C7."""
        self.prev_parts = '0'
        self.prev_chord = 'None'
        self.next_parts = '0'
        self.next_chord = 'None'        
        aux = self.parse_chord_string(chord_string)
        self.parts = aux[0]
        self.chord = aux[1]
        if prev:
            aux = self.parse_chord_string(prev)
            self.prev_parts = aux[0]
            self.prev_chord = aux[1]
        if next:
            aux = self.parse_chord_string(next)
            self.next_parts = aux[0]
            self.next_chord = aux[1]
    def parse_chord_string(self, chord_string):
        x=0; temp=''; ch=''
        for c in chord_string:
            if c.isdigit():
                temp += c
                x += 1
            else:
                ch = chord_string[x:]
                break
        return [temp, Chord(ch)]
    def __str__(self):
        return "Current chord: %s, %s parts.\nPrevious chord: %s, %s parts.\nNext chord: %s, %s parts.\n" \
            % (str(self.chord), self.parts, str(self.prev_chord), self.prev_parts, \
            str(self.next_chord), self.next_parts)
 
if __name__ == "__main__":
    example_input = ['4C7', '2Dm7', '2G7alt', '4Cm7', '4F7', '8Bbmaj7#11']
    example_output = []
    example_output.append(ChordItem(example_input[0], prev=None, next=example_input[1])) #First chord
    for x in range(1,len(example_input)-1): #Middle chords
        example_output.append(ChordItem(example_input[x], prev=example_input[x-1], next=example_input[x+1]))
    example_output.append(ChordItem(example_input[-1], prev=example_input[-2], next=None)) #Last chord
    for y in example_output:
        print str(y)
    #~ ch = Chord('Cm7')
    #~ print ch.generate_abc_arpeggio()
