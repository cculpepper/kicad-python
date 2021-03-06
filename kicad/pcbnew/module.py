#  Copyright 2014 Piers Titus van der Torren <pierstitus@gmail.com>
#  Copyright 2015 Miguel Angel Ajo <miguelangel@ajo.es>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
pcbnew = __import__('pcbnew')

import kicad
from kicad import Point
from kicad.pcbnew.item import HasPosition, HasRotation
from kicad.pcbnew.layer import Layer

class Module(HasPosition, HasRotation, object):

    def __init__(self, ref=None, pos=None, board=None):
        self._obj = pcbnew.MODULE(board.native_obj)
        if ref:
            self.reference = ref
        if pos:
            self.position = pos
        if board:
            board.add(self)

    @property
    def native_obj(self):
        return self._obj

    @staticmethod
    def wrap(instance):
        if type(instance) is pcbnew.MODULE:
            return kicad.new(Module, instance)

    @property
    def reference(self):
        return self._obj.GetReference()

    @reference.setter
    def reference(self, value):
        self._obj.SetReference(value)

    @property
    def layer(self):
        return Layer(self._obj.GetLayer())

    @layer.setter
    def layer(self, value):
        if value != self.layer:
            if value in [Layer.Front, Layer.Back]:
                # this will make sure all components of the module is
                # switched to correct layer
                self._obj.Flip(self._obj.GetCenter())
            else:
                raise ValueError("You can place a module only on Front or Back layers!")

    def copy(self, ref, pos=None, board=None):
        """Create a copy of an existing module on the board"""
        _module = pcbnew.MODULE(board and board._obj)
        _module.Copy(self._obj)
        module = Module.wrap(_module)
        module.reference = ref
        if pos:
            module.position = pos
        if board:
            board.add(module)
        return module
