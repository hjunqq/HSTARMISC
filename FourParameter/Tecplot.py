import logging
logging.basicConfig(level=logging.DEBUG)

import tecplot

import sys

if '-c' in sys.argv:
    tecplot.session.connect()

tecplot.new_layout()

frame = tecplot.active_frame()
frame.add_text("hello world",position=(36,50),size=34)
