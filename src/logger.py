"""
    PyFT Engine 1
    Copyright (C) 2023  DonTSmi1e

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    DESCRIPTION: Engine logger. Conveniently saves logs, displays messages in the terminal.
"""

from colorama import just_fix_windows_console, Fore, Style
from datetime import datetime

just_fix_windows_console()

log = []
warnings = 0
errors = 0

def Print(script, text, state="INFO"):
    global log, warnings, errors

    match state:
        case "DEBUG":
            color = Fore.CYAN
        case "WARN":
            color = Fore.YELLOW
            warnings += 1
        case "ERROR":
            color = Fore.RED
            errors += 1
        case _:
            color = ""

    text = color + f'({datetime.now().strftime("%H:%M:%S")}) ({state}) {script}: "{text}"' + Style.RESET_ALL
    log.append(text)
    print(log[-1])
    