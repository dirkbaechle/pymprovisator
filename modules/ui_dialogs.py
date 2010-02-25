#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

from Tkinter import *
from song import *
from song_rw import *
from constants import *
import preferences
import tkMessageBox, tkFileDialog, sys, os, os.path, gettext

_ = gettext.gettext

DEFAULT_PAD = 2
DEFAULT_BORDERWIDTH = 1
DEFAULT_RELIEF = GROOVE
DEFAULT_POSITION = "+2+2"
DEFAULT_BACKGROUND = 'white'
BACKGROUND_GRAY = 'beige'
PLATFORM = sys.platform
PIANO_INSTRUMENTS = tuple(instrument_names[0:24])
BASS_INSTRUMENTS = tuple(instrument_names[32:40])

# General styling, platform deppendant:
if PLATFORM == 'win32':
    DEFAULT_SMALL_FONT = ('helvetica', 6)
    TUPLE_EXES = [(_("Windoze Executable files"), "*.exe"), (_("All files"), "*")]
else:
    DEFAULT_SMALL_FONT = ('helvetica', 8)
    TUPLE_EXES = [(_("All files"), "*"), (_("Windoze Executable files"), "*.exe")]


class PrefsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.root = Toplevel()
        self.root.geometry(DEFAULT_POSITION)
        self.main_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=1, ipadx=DEFAULT_PAD, ipady=DEFAULT_PAD)
        self.buttons_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.buttons_frame.pack(side=TOP, fill=X, ipadx=DEFAULT_PAD, ipady=DEFAULT_PAD)
        self.__create_widgets()
        self.__load_default_values()
        self.__create_buttons()
        self.root.grab_set()
        self.root.protocol('WM_DELETE_WINDOW', self.OnCancel)
    def __create_widgets(self):
        self.var_abc2midi = StringVar()
        self.var_midiplayer = StringVar()
        self.var_piano = StringVar()
        self.var_bass = StringVar()
        self.var_pianovol = IntVar()
        self.var_bassvol = IntVar()
        self.var_drumsvol = IntVar()
        self.root.title(_("Preferences"))
        # abc2midi
        Label(self.main_frame, text=_("Path to abc2midi:")).grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        Button(self.main_frame, text="...", command=self.OnABC2MIDI).grid(row=0, column=1, sticky=W)
        self.entry_abc2midi = Entry(self.main_frame, width=25, bg=DEFAULT_BACKGROUND, textvariable=self.var_abc2midi)
        self.entry_abc2midi.grid(row=0, column=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        # midiplayer
        Label(self.main_frame, text=_("Path to external midiplayer:")).grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)   
        Button(self.main_frame, text="...", command=self.OnMIDIPLAYER).grid(row=1, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.entry_midiplayer = Entry(self.main_frame, width=25, bg=DEFAULT_BACKGROUND, textvariable=self.var_midiplayer)
        self.entry_midiplayer.grid(row=1, column=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        # prefered piano
        Label(self.main_frame, text=_("Prefered instrument for piano line:")).grid(row=2, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)   
        self.prefered_piano = apply(OptionMenu, (self.main_frame, self.var_piano) + PIANO_INSTRUMENTS)
        self.prefered_piano.grid(row=2, column=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W+E)
        Label(self.main_frame, text=_("Volume for piano line:")).grid(row=3, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=S+E+W)
        self.piano_volumen = Scale(self.main_frame, from_=0, to=127, orient=HORIZONTAL, variable=self.var_pianovol)
        self.piano_volumen.grid(row=3, column=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=E+W)
        # prefered bass
        Label(self.main_frame, text=_("Prefered instrument for bass line:")).grid(row=4, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)   
        self.prefered_bass = apply(OptionMenu, (self.main_frame, self.var_bass) + BASS_INSTRUMENTS)
        self.prefered_bass.grid(row=4, column=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W+E)
        Label(self.main_frame, text=_("Volume for bass line:")).grid(row=5, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=S+E+W)
        self.bass_volumen = Scale(self.main_frame, from_=0, to=127, orient=HORIZONTAL, variable=self.var_bassvol)
        self.bass_volumen.grid(row=5, column=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=E+W)
        # prefered drums
        Label(self.main_frame, text=_("Volume for drums line:")).grid(row=6, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=S+E+W)
        self.drums_volumen = Scale(self.main_frame, from_=0, to=127, orient=HORIZONTAL, variable=self.var_drumsvol)
        self.drums_volumen.grid(row=6, column=1, columnspan=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=E+W)
    def __load_default_values(self):
        instruments = preferences.get_prefered_instruments()
        self.var_piano.set(instruments['piano'])
        self.var_bass.set(instruments['bass'])
        volume = preferences.get_prefered_volume()
        self.var_pianovol.set(volume['piano'])
        self.var_bassvol.set(volume['bass'])
        self.var_drumsvol.set(volume['drums'])
        self.var_abc2midi.set(preferences.get_external_prog_path('ABC2MIDI'))
        self.var_midiplayer.set(preferences.get_external_prog_path('MIDIPLAYER'))

    def __create_buttons(self):
        self.button_done = Button(self.buttons_frame, text=_("Done"), command=self.OnDone)
        self.button_done.pack(side=LEFT, padx=1, pady=1, expand=1)
        self.button_cancel = Button(self.buttons_frame, text=_("Cancel"), command=self.OnCancel)
        self.button_cancel.pack(side=RIGHT, padx=1, pady=1, expand=1)
    def OnABC2MIDI(self):
        file = tkFileDialog.askopenfilename(filetypes=TUPLE_EXES)
        self.var_abc2midi.set(os.path.normpath(file))
    def OnMIDIPLAYER(self):
        file = tkFileDialog.askopenfilename(filetypes=TUPLE_EXES)
        self.var_midiplayer.set(os.path.normpath(file))
    def OnDone(self):
        preferences.set_prefered_instruments({"piano": self.var_piano.get(), "bass": self.var_bass.get()})
        preferences.set_prefered_volume({"piano": self.var_pianovol.get(),
                                        "bass": self.var_bassvol.get(),
                                        "drums": self.var_drumsvol.get()})
        preferences.set_external_prog_path('ABC2MIDI', self.var_abc2midi.get())
        preferences.set_external_prog_path('MIDIPLAYER', self.var_midiplayer.get())
        self.root.destroy()
        self = None
        return 0

    def OnCancel(self):
        if tkMessageBox.askyesno(_("Cancel"), _("Your changes will be lost.\nAre you sure?")):
            self.root.destroy()
            self = None
            return 0
            




class ChordsWindow:
    def __init__(self, parent):
        self.parent = parent
        #~ print self.parent.var_chords
        self.root = Toplevel()
        self.root.geometry(DEFAULT_POSITION)
        self.chords_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.buttons_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.cells = []
        self.__create_chords_table()
        self.__create_buttons()
        self.chords_frame.pack(side=TOP, fill=BOTH, expand=1, ipadx=DEFAULT_PAD, ipady=DEFAULT_PAD)
        self.buttons_frame.pack(side=TOP, fill=X, expand=1, ipadx=DEFAULT_PAD, ipady=DEFAULT_PAD)
        #~ self.chords_frame.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        #~ self.buttons_frame.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=E+W)
        self.root.grab_set()
        self.root.protocol('WM_DELETE_WINDOW', self.OnCancel)
    def __create_chords_table(self):
        style = eval('song.' + self.parent.var_style.get())
        self.root.title( _("Style: ") + style.name + _("  ---  Meter: ") + style.meter + _("  ---  Key: ") + self.parent.var_key.get())
        parts = int(style.meter[0])
        bars = int(self.parent.var_measures.get())
        Label(self.chords_frame, text=_("Parts 1 to ") + style.meter[0] ).grid(row=0, column=0, columnspan=parts, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        Label(self.chords_frame, text=_("Parts 1 to ") + style.meter[0] ).grid(row=0, column=parts, columnspan=parts, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        Label(self.chords_frame, text=_("Parts 1 to ") + style.meter[0] ).grid(row=0, column=2*parts, columnspan=parts, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        Label(self.chords_frame, text=_("Parts 1 to ") + style.meter[0] ).grid(row=0, column=3*parts, columnspan=parts, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        chords_list = self.parent.var_chords
        current_row=1
        current_col=1
        if chords_list:
            counter = 0
            for c in chords_list:
                parts_aux = ''
                chord_aux = ''
                for i in range(len(c)):
                    if c[i].isdigit():
                        parts_aux += c[i]
                        chord_aux = c[i+1:]
                    else:
                        break
                if current_col > 4*parts:
                    current_col = 1
                    current_row += 1
                lbl = Label(self.chords_frame, text=_("Bar #") + str(4*current_row-3), font=DEFAULT_SMALL_FONT)
                lbl.grid(row=current_row, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                if counter% parts == 0:
                    cell = Entry(self.chords_frame, width=5, bg=BACKGROUND_GRAY)
                else:
                    cell = Entry(self.chords_frame, width=5, bg=DEFAULT_BACKGROUND)
                cell.insert(0, chord_aux)
                cell.grid(row=current_row, column=current_col, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                self.cells.append(cell)
                current_col += 1
                counter += 1
                for x in range(int(parts_aux)-1):
                    if current_col > 4*parts:
                        current_col = 1
                        current_row += 1
                    lbl = Label(self.chords_frame, text=_("Bar #") + str(4*current_row-3), font=DEFAULT_SMALL_FONT)
                    lbl.grid(row=current_row, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                    if counter % parts == 0:
                        cell = Entry(self.chords_frame, width=5, bg=BACKGROUND_GRAY)
                    else:
                        cell = Entry(self.chords_frame, width=5, bg=DEFAULT_BACKGROUND)
                    cell.grid(row=current_row, column=current_col, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                    self.cells.append(cell)
                    current_col += 1
                    counter += 1
            if len(self.cells) < (bars*parts):
                counter = 0
                for x in range(bars*parts-len(self.cells)):
                    if current_col > 4*parts:
                        current_col = 1
                        current_row += 1
                    lbl = Label(self.chords_frame, text=_("Bar #") + str(4*current_row-3), font=DEFAULT_SMALL_FONT)
                    lbl.grid(row=current_row, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                    if counter % parts == 0:
                        cell = Entry(self.chords_frame, width=5, bg=BACKGROUND_GRAY)
                    else:
                            cell = Entry(self.chords_frame, width=5, bg=DEFAULT_BACKGROUND)
                    cell.grid(row=current_row, column=current_col, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                    self.cells.append(cell)
                    current_col += 1
                    counter += 1
        else:
            counter = -1
            for x in range(bars*parts):
                counter += 1
                if current_col > 4*parts:
                            current_col = 1
                            current_row += 1
                lbl = Label(self.chords_frame, text=_("Bar #") + str(4*current_row-3), font=DEFAULT_SMALL_FONT)
                lbl.grid(row=current_row, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                if counter % parts == 0:
                    cell = Entry(self.chords_frame, width=5, bg=BACKGROUND_GRAY)
                else:
                    cell = Entry(self.chords_frame, width=5, bg=DEFAULT_BACKGROUND)
                cell.grid(row=current_row, column=current_col, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
                self.cells.append(cell)
                current_col += 1
            
    def __create_buttons(self):
        self.button_done = Button(self.buttons_frame, text=_("Done"), command=self.OnDone)
        self.button_done.pack(side=LEFT, padx=1, pady=1, expand=1)
        self.button_cancel = Button(self.buttons_frame, text=_("Cancel"), command=self.OnCancel)
        self.button_cancel.pack(side=RIGHT, padx=1, pady=1, expand=1)
    def OnDone(self):
        if self.cells[0].get() == '':
               tkMessageBox.showwarning(_("Empty cells"), _("You have to fill the first chord at least."))
               return 0
        else:
            chords = []
            first_time = 1
            for cell in self.cells: 
                c = cell.get()
                #~ print c
                if first_time:
                    aux = 1, c
                    chords.append(aux)
                else:
                    if c == '':
                        aux = (chords[-1][0] + 1, chords[-1][1])
                        chords[-1] = aux
                    else:
                        aux = 1, c
                        chords.append(aux)
                first_time = 0
            self.parent.var_chords = ["%d%s"%(n, c) for n, c in chords]
            #~ print self.parent.var_chords
            input_instruments = []
            if self.parent.var_piano.get(): input_instruments.append('piano')
            if self.parent.var_bass.get(): input_instruments.append('bass')
            if self.parent.var_drums.get(): input_instruments.append('drums')
            try:
                self.parent.Song = Song(self.parent.var_title.get().strip().lower(), self.parent.var_title.get(), 
                                              str(self.parent.var_tempo.get()), self.parent.var_key.get(), eval('song.' + self.parent.var_style.get()), 
                                              self.parent.var_chords, self.parent.var_measures.get(), self.parent.var_choruses.get(), input_instruments)
                self.parent.status_label.configure(text=_("Working on ") + self.parent.var_title.get())
            except MyException, e:
                tkMessageBox.showwarning(_("Error"), _("There was some error generating the song:\n") + str(e) + \
                _("\nPlease, check your chords.\nIf your chords are correct, check the number of measures.") )
                self.root.grab_set()
                return 0
            self.root.destroy()
            self = None
            return 1
    def OnCancel(self):
        if tkMessageBox.askyesno(_("Cancel"), _("Your changes will be lost.\nAre you sure?")):
            self.root.destroy()
            self = None
            return 0
