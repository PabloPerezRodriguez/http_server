# http_server

This is a very simple multi-threaded HTTP 1.0 web server written in Python 3.
It can only serve GET requests so far, but I plan on adding some more.

I'm ~~probably~~ not doing the best job at anything, not even receiving the TCP data, but it's fun to work on this.

This server serves files from the './public' folder (you have to create the folder).
Errors use templates, but you can customize error messages by adding a './private/errors/{ERROR-CODE}.html' file



Copyright (C) <2019>  <Pablo Pérez Rodríguez>

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
