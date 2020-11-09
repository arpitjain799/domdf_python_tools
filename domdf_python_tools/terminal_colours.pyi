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
#  Distributed under the BSD 3-Clause license.
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

CSI: Final[str]
OSC: Final[str]
BEL: Final[str]

fore_stack: List[str]
back_stack: List[str]
style_stack: List[str]


def code_to_chars(code) -> str: ...
def set_title(title: str) -> str: ...
def clear_screen(mode: int = ...) -> str: ...
def clear_line(mode: int = ...) -> str: ...


def strip_ansi(value: str) -> str: ...


class Colour(str):
	style: str
	reset: str
	stack: List[str]

	def __new__(cls, style: str, stack: List[str], reset: str) -> "Colour": ...
	def __enter__(self) -> None: ...
	def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
	def __call__(self, text) -> str: ...


class AnsiCodes(ABC):
	_stack: List[str]
	_reset: str

	def __init__(self) -> None: ...


class AnsiCursor:

	def UP(self, n: int = ...) -> str: ...
	def DOWN(self, n: int = ...) -> str: ...
	def FORWARD(self, n: int = ...) -> str: ...
	def BACK(self, n: int = ...) -> str: ...
	def POS(self, x: int = ..., y: int = ...) -> str: ...


class AnsiFore(AnsiCodes):

	_stack = fore_stack
	_reset = ...

	BLACK: Colour
	RED: Colour
	GREEN: Colour
	YELLOW: Colour
	BLUE: Colour
	MAGENTA: Colour
	CYAN: Colour
	WHITE: Colour
	RESET: Colour

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX: Colour
	LIGHTRED_EX: Colour
	LIGHTGREEN_EX: Colour
	LIGHTYELLOW_EX: Colour
	LIGHTBLUE_EX: Colour
	LIGHTMAGENTA_EX: Colour
	LIGHTCYAN_EX: Colour
	LIGHTWHITE_EX: Colour


class AnsiBack(AnsiCodes):

	_stack: List[str]
	_reset: str

	BLACK: Colour
	RED: Colour
	GREEN: Colour
	YELLOW: Colour
	BLUE: Colour
	MAGENTA: Colour
	CYAN: Colour
	WHITE: Colour
	RESET: Colour

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX: Colour
	LIGHTRED_EX: Colour
	LIGHTGREEN_EX: Colour
	LIGHTYELLOW_EX: Colour
	LIGHTBLUE_EX: Colour
	LIGHTMAGENTA_EX: Colour
	LIGHTCYAN_EX: Colour
	LIGHTWHITE_EX: Colour


class AnsiStyle(AnsiCodes):

	_stack: List[str]
	_reset: str

	BRIGHT: Colour
	DIM: Colour
	NORMAL: Colour
	RESET_ALL: Colour


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()
