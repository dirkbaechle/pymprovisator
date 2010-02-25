#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

import sys, tempfile, os.path, getopt, popen2, gettext
from modules import song_rw, preferences, constants

_ = gettext.gettext
gettext.bindtextdomain('messages', os.path.abspath('i18n'))
gettext.textdomain('messages')


def help():
    print _("""Welcome to pymprovisator. 
Written by David Asorey Álvarez (forodejazz@yahoo.es)
This program generates and play an accompaniment MIDI file. 
See README.txt for more details.
Usage:    pymprovisator [-g] file
          pymprovisator -h
          pymprovisator -c
    -g (--gui): launch a graphical user interface. 
    file: file containg a song in pymprovisator format (see 'pymprovisator/examples/')
    -h (--help): shows this help message.
    -c (--chords): shows the available chords.
    -s (--setup): creates a configuration file in your home directory.
""")


def main(file):
    s = song_rw.load_song(file)
    if s:
        abc2midi = preferences.get_external_prog_path('ABC2MIDI')
        if not abc2midi:
            print '\n' + _("abc2midi program not found."), _("Please, check your preferences file (") + preferences.preferences_file + ")"
            sys.exit(2)
        midiplayer = preferences.get_external_prog_path('MIDIPLAYER')
        if not midiplayer:
            print '\n' + _("MIDI player program not found."), _("Please, check your preferences file (") + preferences.preferences_file + ")"
            sys.exit(2)
        final_song = s.generate_song(preferences.get_prefered_instruments())
        input = tempfile.mktemp('.abc')
        abc_file = open(input, 'w')
        output = os.path.abspath(os.path.dirname(file) + '/' + s.id + '.mid')
        for l in final_song:
            abc_file.write(l + "\n")
        abc_file.close()
        command = abc2midi + ' "' + input + '" -o "' + output + '"'
        print '\n' + _("Executing: ") + command
        print '\n' + _("MIDI file saved on ") + output
        popen2.popen2(command)
        command = midiplayer + ' "' + output + '"'
        print '\n' + _("Executing: ") + command
        os.system(command)
    else:
        print '\n' + _("There was some problem while loading the song file ") + os.path.normpath(file) + '\n' + _("Please, check that file.")


if __name__ == '__main__':
    gui = 0
    try:
        opt, arg = getopt.getopt(sys.argv[1:], 'ghcs', ['gui', 'help', 'chords', 'setup'])
    except:
        help()
        sys.exit(2)
    for a, b in opt:
        if a in ('-g', '--gui'):
            from modules import ui
            gui = 1
            if not arg:
                ui.main()
                break
            file = os.path.normpath(arg[0])
            ui.main(os.path.abspath(file))
            break
        elif a in ('-s', '--setup'):
            preferences.set_defaults()
            sys.exit(0)
        elif a in ('-h', '--help'): 
            help()
            sys.exit(0)
        elif a in ('-c', '--chords'):
            print '\n' + _("AVAILABLE CHORDS:") + '\n\n' + constants.available_chords
            sys.exit(0)
    if not gui:
        if not arg:
            help()
            sys.exit(2)
        file = os.path.abspath(arg[0])
        if not os.path.exists(file):
            print '\n' + _("File '%s' not found. Please, check your typing") % (file,)
            sys.exit(2)
        main(os.path.abspath(file))
