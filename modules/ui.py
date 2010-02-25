#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

from Tkinter import *
from song import *
from song_rw import *
from constants import *
import preferences, ui_dialogs
import tkMessageBox, tkFileDialog
import sys, os, os.path, popen2, webbrowser, gettext

# Some constants
APPLICATION = 'Pymprovisator 0.1.1'
STYLES = tuple([s.name for s in available_styles])
KEYS = tuple(valid_keys)
HOME_DIR = os.path.expanduser('~')
DEFAULT_PAD = 2
DEFAULT_BORDERWIDTH = 1
DEFAULT_RELIEF = GROOVE
DEFAULT_POSITION = "+20+20"
DEFAULT_BACKGROUND = 'white'
PLATFORM = sys.platform

# General styling, platform deppendant:
if PLATFORM == 'win32':
    DEFAULT_SIZE = (300, 230)
else:
    DEFAULT_SIZE = (320, 250)

_ = gettext.gettext

class MainWindow:
    def __init__(self, song_file=None):
        #Main application window:
        self.root = Tk()
        if PLATFORM == 'win32': self.root.option_readfile('modules/default_font_win32')
        else: self.root.option_readfile('modules/default_font_unix')
        # TK Variables
        self.var_title = StringVar()
        self.var_style = StringVar()
        self.var_key = StringVar()
        self.var_piano = IntVar()
        self.var_bass = IntVar()
        self.var_drums = IntVar()
        self.var_tempo = IntVar()
        self.var_measures = StringVar()
        self.var_choruses = StringVar()
        # Other application variables
        self.var_chords = [] #The chords aren't in any widget
        self.last_dir = HOME_DIR
        #Create all
        self.__create_menus()
        self.__create_toolbar()
        self.__create_mainframe()
        self.__create_statusbar()
        # Trying load song file
        if not song_file:
            self.Song = None
            self.__load_default_song_values()
        else:
            if not os.path.exists(song_file):
                tkMessageBox.showwarning(_("Loading song"), _("The song file '") + os.path.normpath(song_file) + _("' does not exists.\nThere isn't any song loaded now."))
                self.Song = None
                self.__load_default_song_values()
            else:
                self.Song = load_song(song_file)
                if self.Song:
                    self.__read_song_values()
                    self.status_label.configure(text=_("Working on song file '") + os.path.normpath(song_file) + "'")
                else:
                    tkMessageBox.showwarning(_("Loading song"), _("There was an error while reading the song file.\nPlease, check the song file '") + os.path.normpath(song_file) + _("'\nThere isn't any song loaded now."))
                    self.Song = None
                    self.__load_default_song_values()
        self.root.title(APPLICATION)
        self.root.minsize(DEFAULT_SIZE[0], DEFAULT_SIZE[1])
        self.root.geometry(DEFAULT_POSITION)
        #~ self.root.resizable(0, 0)  
        self.root.protocol('WM_DELETE_WINDOW', self.OnExit)

    def __create_menus(self):
        #Menu bar:
        self.menu_bar = Menu(self.root, relief=DEFAULT_RELIEF)
        # "File" menu:
        self.menu_file = Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label=_("New song"), command=self.OnNew)
        self.menu_file.add_command(label=_("Open song"), command=self.OnOpen)
        self.menu_file.add_command(label=_("Save song"), command=self.OnSave)
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Exit"), command=self.OnExit)
        # "Song" menu:
        self.menu_song = Menu(self.menu_bar, tearoff=0)
        self.menu_song.add_command(label=_("Edit chords"), command=self.OnChords)
        self.menu_song.add_command(label=_("Clear chords"), command=self.OnClear)
        self.menu_song.add_command(label=_("Play song"), command=self.OnPlay)
        self.menu_song.add_separator()
        self.menu_song.add_command(label=_("Preferences"), command=self.OnPrefs)
        # "Help" menu:
        self.menu_help = Menu(self.menu_bar, tearoff=0)
        self.menu_help.add_command(label=_("About"), command=self.OnAbout)
        self.menu_help.add_command(label=_("On-line manual"), command=self.OnManual)
        self.menu_help.add_separator()
        self.menu_help.add_command(label=_("Available chords"), command=self.OnAvailableChords)
        # Settin' up all menus
        self.menu_bar.add_cascade(label=_("File"), menu=self.menu_file)
        self.menu_bar.add_cascade(label=_("Song"), menu=self.menu_song)
        self.menu_bar.add_cascade(label=_("Help"), menu=self.menu_help)
        self.root.config(menu=self.menu_bar)

    def __create_toolbar(self):
        self.toolbar_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.toolbar_frame.pack(side=TOP, fill=X)
        self.image_chords = PhotoImage(file='modules/chords.gif')
        self.image_new = PhotoImage(file='modules/new.gif')
        self.image_open = PhotoImage(file='modules/open.gif')
        self.image_save = PhotoImage(file='modules/save.gif')
        self.image_play = PhotoImage(file='modules/play.gif')
        self.image_prefs = PhotoImage(file='modules/prefs.gif')
        self.image_clear = PhotoImage(file='modules/clear.gif')
        self.new_button = Button(self.toolbar_frame, image=self.image_new, command=self.OnNew)
        self.new_button.pack(side=LEFT)
        self.open_button = Button(self.toolbar_frame, image=self.image_open, command=self.OnOpen)
        self.open_button.pack(side=LEFT)
        self.save_button = Button(self.toolbar_frame, image=self.image_save, command=self.OnSave)
        self.save_button.pack(side=LEFT)
        self.chords_button = Button(self.toolbar_frame, image=self.image_chords, command=self.OnChords)
        self.chords_button.pack(side=LEFT)
        self.play_button = Button(self.toolbar_frame, image=self.image_play, command=self.OnPlay)
        self.play_button.pack(side=LEFT)
        self.prefs_button = Button(self.toolbar_frame, image=self.image_prefs, command=self.OnPrefs)
        self.prefs_button.pack(side=LEFT)
        self.exit_button = Button(self.toolbar_frame, image=self.image_clear, command=self.OnClear)
        self.exit_button.pack(side=LEFT)

    def __create_mainframe(self):
        self.main_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=1, ipadx=DEFAULT_PAD, ipady=DEFAULT_PAD)
        # 1st row: TITLE
        self.title_label = Label(self.main_frame, text=_("Title"))
        self.title_label.grid(row=0, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.title_entry = Entry(self.main_frame, textvariable=self.var_title, bg=DEFAULT_BACKGROUND)
        self.title_entry.grid(row=0, column=1, columnspan=3, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        # 2nd row: STYLE AND KEY
        self.style_label = Label(self.main_frame, text=_("Style"))
        self.style_label.grid(row=1, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.style_option = apply(OptionMenu, (self.main_frame, self.var_style) + STYLES)
        self.style_option.configure(width=10)
        self.style_option.grid(row=1, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.key_label = Label(self.main_frame, text=_("Key"))
        self.key_label.grid(row=1, column=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.key_option = apply(OptionMenu, (self.main_frame, self.var_key) + KEYS)
        #~ self.key_option.configure(font=DEFAULT_FONT)
        self.key_option.grid(row=1, column=3, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        # 3rd row: INSTRUMENTS
        self.instruments_label = Label(self.main_frame, text=_("Instruments"))
        self.instruments_label.grid(row=2, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.piano_checkbutton = Checkbutton(self.main_frame, text=_("Piano"), variable=self.var_piano, width=10)
        self.piano_checkbutton.grid(row=2, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.bass_checkbutton = Checkbutton(self.main_frame, text=_("Bass"), variable=self.var_bass, width=10)
        self.bass_checkbutton.grid(row=2, column=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.drums_checkbutton = Checkbutton(self.main_frame, text=_("Drums"), variable=self.var_drums, width=10)
        self.drums_checkbutton.grid(row=2, column=3, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        # 4th row: TEMPO
        self.tempo_label = Label(self.main_frame, text=_("Tempo"))
        self.tempo_label.grid(row=3, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.tempo_scale = Scale(self.main_frame, from_=30, to=350, orient=HORIZONTAL, variable=self.var_tempo)
        self.tempo_scale.grid(row=3, column=1, columnspan=3, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=N+S+E+W)
        # 5th row: MEASURES AND CHORUSES
        self.measures_label = Label(self.main_frame, text=_("Measures"))
        self.measures_label.grid(row=4, column=0, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.measures_entry = Entry(self.main_frame, textvariable=self.var_measures, width=5, bg=DEFAULT_BACKGROUND)
        self.measures_entry.grid(row=4, column=1, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.choruses_label = Label(self.main_frame, text=_("Choruses"))
        self.choruses_label.grid(row=4, column=2, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        self.choruses_entry = Entry(self.main_frame, textvariable=self.var_choruses, width=5, bg=DEFAULT_BACKGROUND)
        self.choruses_entry.grid(row=4, column=3, padx=DEFAULT_PAD, pady=DEFAULT_PAD, sticky=W)
        
    def __create_statusbar(self):
        self.status_frame = Frame(self.root, relief=DEFAULT_RELIEF, borderwidth=DEFAULT_BORDERWIDTH)
        self.status_frame.pack(side=TOP, fill=X)
        self.status_label = Label(self.status_frame, text= _("Welcome to ") + APPLICATION + _(". No song loaded."), 
                                    justify=LEFT)
        self.status_label.pack(side=LEFT, fill=X, padx=1, pady=1, ipadx=2, ipady=2)

    def __load_default_song_values(self):
        self.var_title.set(_("Untitled"))
        self.var_key.set(KEYS[0])
        self.var_style.set(STYLES[0])
        self.var_piano.set(1)
        self.var_bass.set(1)
        self.var_drums.set(1)
        self.var_tempo.set(120)
        self.var_measures.set(32)
        self.var_choruses.set(3)
        self.var_chords = []
        self.status_label.configure(text=_("Welcome to ") + APPLICATION + _(". No song loaded."))
    def __read_song_values(self):
        self.var_title.set(self.Song.title)
        self.var_key.set(self.Song.key)
        self.var_style.set(self.Song.style.name)
        if 'piano' in self.Song.instruments: self.var_piano.set(1)
        if 'bass' in self.Song.instruments: self.var_bass.set(1)
        if 'drums' in self.Song.instruments: self.var_drums.set(1)
        self.var_tempo.set(self.Song.tempo)
        self.var_measures.set(self.Song.n_bars)
        self.var_choruses.set(self.Song.n_choruses)
        self.var_chords = self.Song.chord_seq
        #~ print self.var_chords
    
    def __check_values(self):
        self.input_instruments = []
        if self.var_piano.get(): self.input_instruments.append('piano')
        if self.var_bass.get(): self.input_instruments.append('bass')
        if self.var_drums.get(): self.input_instruments.append('drums')
        try:
            int(self.var_measures.get())
        except:
            return (0, _("You must supply an numerical value in measures."))
        try:
            int(self.var_choruses.get())
        except:
            return (0, _("You must supply an numerical value in choruses."))
        if int(self.var_measures.get()) < 1 :
            return (0, _("You must supply an numerical value in measures greater than zero."))
        if int(self.var_choruses.get()) < 1 :
            return (0, _("You must supply an numerical value in choruses greater than zero."))
        if self.var_title.get().strip().replace(' ', '') == '':
            return (0, _("You must supply the song's title."))
        if self.var_style.get() == '':
            return (0, _("You must supply the song's style."))
        if self.var_key.get() == '':
            return (0, _("You must supply the song's key."))
        if not self.var_chords:
            return (0, _("You must supply the song's chord sequence."))
        if not self.input_instruments:
            return (0, _("You must supply the song's instruments."))
        return (1, '')

# Handlers:
    def OnNew(self):
        if self.Song:
            if tkMessageBox.askyesno(_("New song"), _("If you haven't saved your song, your work will be lost.\nAre you sure?")):
                self.__load_default_song_values()
                self.Song = None
                return

    def OnOpen(self):
        if self.Song:
            if not tkMessageBox.askyesno(_("Open song"), _("If you haven't saved your song, your work will be lost.\nAre you sure?")):
                self.Song = None
                return
        file = tkFileDialog.askopenfilename(title = _("Open song"), filetypes=[(_("Pymprovisator songs"), "*.ymp"), (_("All files"), "*")], initialdir=self.last_dir)
        if not file: return
        self.last_dir = os.path.dirname(file) 
        self.Song = load_song(file)
        if self.Song:
            self.__read_song_values()
            self.status_label.configure(text=_("Working on song file '") + os.path.normpath(file) + "'")
        else:
            tkMessageBox.showwarning(_("Loading song"), _("There was an error while reading the song file.\nPlease, check the song file '") + os.path.normpath(file) + _("'\nThere isn't any song loaded now."))
            self.Song = None
            self.__load_default_song_values()

    def OnSave(self):
        validation = self.__check_values()
        if not validation[0]:
            tkMessageBox.showwarning(_("Saving song"), _("There was an error while saving the song file:\n") + validation[1])
            return
        destination = self.var_title.get().title().replace(' ', '')
        try:
            self.Song = Song(destination, self.var_title.get(), 
                         self.var_tempo.get(), self.var_key.get(),
                         eval('song.' + self.var_style.get()), self.var_chords, 
                         self.var_measures.get(), self.var_choruses.get(), self.input_instruments)
        except MyException, e:
            tkMessageBox.showwarning(_("Error"), _("There was some error generating the song:\n") + str(e) + \
            _("\nPlease, check your song settings and chord sequence.") )
            self.Song = None
            return
        file = tkFileDialog.asksaveasfilename(title = _("Save song"), filetypes=[(_("Pymprovisator songs"), "*.ymp"), (_("All files"), "*")],
                                              initialdir=self.last_dir, 
                                              initialfile= destination + '.ymp')
        if file:
            self.last_dir = os.path.dirname(file) 
            if not save_song(file, self.Song):
                tkMessageBox.showwarning(_("Saving song"), _("There was some error saving the song.\nPlease, check the file name provided and/or your permisions in that directory."))
                self.Song = None
                return

    def OnExit(self):
        if self.Song:
            if tkMessageBox.askyesno(_("Exit"), _("If you haven't saved your song, your work will be lost.\nAre you sure?")):
                self.root.quit()
        else:
                self.root.quit()
    def OnChords(self): ui_dialogs.ChordsWindow(self)
    def OnClear(self): 
        if tkMessageBox.askyesno(_("Clear chords"), _("The chords will be erased.\nAre you sure?")):
            self.var_chords = []
    def OnPlay(self):
        validation = self.__check_values()
        if not validation[0]:
            tkMessageBox.showwarning(_("Playing song"), _("There was an error while generating the song file:\n") + validation[1])
            return
        abc2midi = preferences.get_external_prog_path('ABC2MIDI')
        midiplayer = preferences.get_external_prog_path('MIDIPLAYER')
        if not abc2midi:
            tkMessageBox.showwarning(_("abc2midi program not found"), _("Please, check your preferences file (") + preferences.preferences_file + ")" )
            return
        if not midiplayer:
            tkMessageBox.showwarning(_("MIDI player program not found"), _("Please, check your preferences file (") + preferences.preferences_file + ")" )
            return
        try:
            destination = self.var_title.get().title().replace(' ', '')
            self.Song = Song(destination, self.var_title.get(), 
                            self.var_tempo.get(), self.var_key.get(),
                            eval('song.' + self.var_style.get()), self.var_chords, 
                            self.var_measures.get(), self.var_choruses.get(), self.input_instruments)
        except MyException, e:
            tkMessageBox.showwarning(_("Error"), _("There was some error generating the song:\n") + str(e) + \
                _("\nPlease, check your song settings and chord sequence.") )
            self.Song = None
            return
        final = self.Song.generate_song(preferences.get_prefered_instruments())
        input = tempfile.mktemp('.abc')
        abc_file = open(input, 'w')
        output = os.path.abspath(self.last_dir + '/' + self.Song.id + '.mid')
        for l in final:
            abc_file.write(l + "\n")
        abc_file.close()
        command = abc2midi + ' "' + input + '" -o "' + output + '"'
        popen2.popen2(command)
        command = midiplayer + ' "' + output + '"'
        popen2.popen2(command)
        return
    def OnPrefs(self): ui_dialogs.PrefsWindow(self)
    def OnAbout(self): 
        tkMessageBox.showinfo(_("About ") + APPLICATION , APPLICATION  + _(" was written by David Asorey Álvarez (forodejazz@yahoo.es)\nThis program is free software.\nSee the files README.txt and LICENSE.txt for more details.\nThanks for using ") + APPLICATION + "!")
    def OnAvailableChords(self):
        tkMessageBox.showinfo(_("Available chords"), available_chords)
    def OnManual(self):
        url = 'file://' + os.path.abspath("doc/index.html")
        webbrowser.open(url)
    def run(self):
        self.root.mainloop()

def main(song_file=None):
    if song_file:
        print _("Using song file: '") + os.path.normpath(song_file) + "'"
    app = MainWindow(song_file)
    app.run()

if __name__ == '__main__': 
    os.chdir('..')
    app = MainWindow()
    app.run()
    
