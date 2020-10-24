# Wahoo! Results - https://github.com/JohnStrunk/wahoo-results
# Copyright (C) 2020 - John D. Strunk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''Wahoo! Results scoreboard'''

import os
import time
from tkinter import Tk
from typing import List
from PIL import Image  #type: ignore
from PIL.ImageEnhance import Brightness  #type: ignore
import watchdog.events  #type: ignore
import watchdog.observers  #type: ignore

import results
import settings
from config import WahooConfig
from scoreboard import Scoreboard

FILE_WATCHER: watchdog.observers.Observer

def eventlist_to_csv(events: List[results.Event]) -> List[str]:
    '''Converts a list of events into CSV format'''
    lines: List[str] = []
    for i in events:
        lines.append(f"{i.event},{i.event_desc},{i.num_heats},1,A\n")
    return lines

def generate_dolphin_csv(filename: str, directory: str) -> int:
    """
    Write the events from the scb files in the given directory into a CSV
    for Dolphin.
    """
    files = os.scandir(directory)
    events = []
    for file in files:
        if file.name.endswith(".scb"):
            event = results.Event()
            event.from_scb(file.path)
            events.append(event)
    events.sort(key=lambda e: e.event)
    csv_lines = eventlist_to_csv(events)
    outfile = os.path.join(directory, filename)
    csv = open(outfile, "w")
    csv.writelines(csv_lines)
    csv.close()
    return len(events)

class Do4Handler(watchdog.events.PatternMatchingEventHandler):
    '''Handler to process Dolphin .do4 files'''
    _sb: Scoreboard
    _options: WahooConfig
    def __init__(self, scoreboard: Scoreboard, options: WahooConfig):
        self._sb = scoreboard
        self._options = options
        super().__init__(patterns=["*.do4"], ignore_directories=True)
    def on_created(self, event):
        time.sleep(1)
        heat = results.Heat()
        heat.load_do4(event.src_path)
        scb_filename = f"E{heat.event}.scb"
        heat.load_scb(os.path.join(self._options.get_str("start_list_dir"), scb_filename))
        display(self._sb, heat)

def settings_window(root: Tk, options: WahooConfig) -> None:
    '''Display the settings window'''
    # don't watch for new results while in settings menu
    FILE_WATCHER.unschedule_all()

    # Settings window is fixed size
    root.resizable(False, False)
    root.geometry("400x300")

    def sb_run_cb():
        board = scoreboard_window(root, options)
        # Start watching for new results
        do4_handler = Do4Handler(board, options)
        FILE_WATCHER.schedule(do4_handler, options.get_str("dolphin_dir"))

    def sb_test_cb():
        board = scoreboard_window(root, options)
        _set_test_data(board)

    # Invisible container that holds all content
    content = settings.Settings(root, generate_dolphin_csv, sb_run_cb, sb_test_cb, options)
    content.grid(column=0, row=0, sticky="news")

def scoreboard_window(root: Tk, options: WahooConfig) -> Scoreboard:
    """Displays the scoreboard window."""
    # Scoreboard is varible size
    root.resizable(True, True)
    content = Scoreboard(root)
    content.grid(column=0, row=0, sticky="news")
    image = Image.open('rsa2.png')
    content.bg_image(Brightness(image).enhance(0.25), "fit")
    content.set_lanes(options.get_int("num_lanes"))

    def return_to_settings(_) -> None:
        root.unbind('<Double-1>')
        content.destroy()
        root.state('normal') # Un-maximize
        settings_window(root, options)
    root.bind('<Double-1>', return_to_settings)
    return content

def display(board: Scoreboard, heat: results.Heat) -> None:
    """
    Display the results of a heat.
    """
    board.clear()
    board.event(heat.event, heat.event_desc)
    board.heat(heat.heat)

    for i in range(0, 10):
        if not heat.lanes[i].is_empty():
            ftime = heat.lanes[i].final_time()
            place = heat.place(i)
            if not heat.lanes[i].times_are_valid():
                ftime = -ftime
                place = 0
            board.lane(i+1, heat.lanes[i].name, heat.lanes[i].team, ftime, place)
    # heat.dump()

def _set_test_data(board: Scoreboard):
    board.clear()
    board.event(432, "GIRLS 13&O 1650 FREE")
    board.heat(56)
    board.lane(1, "NUMBERONE, SWIMMER", "TEAM1", 16*60 + 31.03, 4)
    board.lane(2, "WINNER, IMTHE", "TEAM1", 48.00, 1)
    board.lane(3, "NUMBERONE, SWIMMER", "TEAM1", 10*60 + 00.20, 3)
    board.lane(4, "NOSHOW, IMA", "TEAM1")
    board.lane(5, "", "", 60*5 + 12.34, 2)
    board.lane(6, "TIMES, INCONSISTENT", "TEAM1", -678.12)
    board.lane(7, "NUMBERONE, SWIMMER", "TEAM1", 1000.03)
    board.lane(8, "NUMBERONE, SWIMMER", "TEAM1", 1000.03)
    board.lane(9, "NUMBERONE, SWIMMER", "TEAM1", 1000.03)
    board.lane(10, "NUMBERONE, SWIMMER", "TEAM1", 1000.03)

def main():
    '''Runs the Wahoo! Results scoreboard'''
    global FILE_WATCHER  # pylint: disable=W0603

    config = WahooConfig()

    root = Tk()
    root.title("Wahoo! Results")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    FILE_WATCHER = watchdog.observers.Observer()
    FILE_WATCHER.start()

    settings_window(root, config)
    root.mainloop()

    config.save()
    FILE_WATCHER.stop()
    FILE_WATCHER.join()

if __name__ == "__main__":
    main()