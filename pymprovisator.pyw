#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Pymprovisator v. 0.1.1
# This program is free software. See the files LICENSE.TXT and README.TXT for more details
# Written by David Asorey Álvarez (forodejazz@yahoo.es). Madrid (Spain). August 2003.

import gettext, os
from modules import ui

_ = gettext.gettext
gettext.bindtextdomain('messages', os.path.abspath('i18n'))
gettext.textdomain('messages')

ui.main()

if __name__ == '__main__':
    ui.main
