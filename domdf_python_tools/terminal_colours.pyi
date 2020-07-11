#!/usr/bin/env python
#
#  terminal_colours.py
"""
Functions for adding colours to terminal print statements.

This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Based on colorama
#  https://github.com/tartley/colorama
#  Copyright Jonathan Hartley 2013
#  Distrubuted under the BSD 3-Clause license.
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  * Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright notice,
#  |    this list of conditions and the following disclaimer in the documentation
#  |    and/or other materials provided with the distribution.
#  |
#  |  * Neither the name of the copyright holders, nor those of its contributors
#  |    may be used to endorse or promote products derived from this software without
#  |    specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  |  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  |  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  |  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  |  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  |  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Includes modifications to colorama made by Bram Geelen in
#  https://github.com/tartley/colorama/pull/141/files

# stdlib
from abc import ABC
from typing import List

# 3rd party
from typing_extensions import Final

CSI: Final[str] = '\033['
OSC: Final[str] = '\033]'
BEL: Final[str] = '\a'

fore_stack: List[str] = []
back_stack: List[str] = []
style_stack: List[str] = []


def code_to_chars(code) -> str: ...
def set_title(title: str) -> str: ...
def clear_screen(mode: int = 2) -> str: ...
def clear_line(mode: int = 2) -> str: ...


class Color(str):
	style: str
	reset: str
	stack: List[str]

	def __new__(cls, style: str, stack: List[str], reset: str) -> "Color": ...
	def __enter__(self) -> None: ...
	def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
	def __call__(self, text) -> str: ...


class AnsiCodes(ABC):
	_stack: List[str]
	_reset: str

	def __init__(self) -> None: ...


class AnsiCursor:

	def UP(self, n: int = 1) -> str: ...
	def DOWN(self, n: int = 1) -> str: ...
	def FORWARD(self, n: int = 1) -> str: ...
	def BACK(self, n: int = 1) -> str: ...
	def POS(self, x: int = 1, y: int = 1) -> str: ...


class AnsiFore(AnsiCodes):

	_stack = fore_stack
	_reset = "\033[39m"

	BLACK: Color
	RED: Color
	GREEN: Color
	YELLOW: Color
	BLUE: Color
	MAGENTA: Color
	CYAN: Color
	WHITE: Color
	RESET: Color

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX: Color
	LIGHTRED_EX: Color
	LIGHTGREEN_EX: Color
	LIGHTYELLOW_EX: Color
	LIGHTBLUE_EX: Color
	LIGHTMAGENTA_EX: Color
	LIGHTCYAN_EX: Color
	LIGHTWHITE_EX: Color


class AnsiBack(AnsiCodes):

	_stack = back_stack
	_reset = "\033[49m"

	BLACK: Color
	RED: Color
	GREEN: Color
	YELLOW: Color
	BLUE: Color
	MAGENTA: Color
	CYAN: Color
	WHITE: Color
	RESET: Color

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX: Color
	LIGHTRED_EX: Color
	LIGHTGREEN_EX: Color
	LIGHTYELLOW_EX: Color
	LIGHTBLUE_EX: Color
	LIGHTMAGENTA_EX: Color
	LIGHTCYAN_EX: Color
	LIGHTWHITE_EX: Color


class AnsiStyle(AnsiCodes):

	_stack = style_stack
	_reset = "\033[22m"

	BRIGHT: Color
	DIM: Color
	NORMAL: Color
	RESET_ALL: Color


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()

fore_stack.append(Fore.RESET)
back_stack.append(Back.RESET)
style_stack.append(Style.NORMAL)
