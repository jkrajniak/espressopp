#!/usr/bin/env python3
#
#  Copyright (C) 2020(H)
#      Jozef Stefan Institute
#      Max Planck Institute for Polymer Research
#  Copyright (C) 2013-2017(H)
#      Max Planck Institute for Polymer Research
#
#  This file is part of ESPResSo++.
#
#  ESPResSo++ is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ESPResSo++ is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -*- coding: utf-8 -*-

import sys
import time
import espressopp
import mpi4py.MPI as MPI
from espressopp.tools import timers


system = espressopp.System()
box=(10,10,10)
system.bc = espressopp.bc.OrthorhombicBC(system.rng, box)
system.skin = 0.3
system.comm = MPI.COMM_WORLD
nodeGrid = espressopp.tools.decomp.nodeGrid(espressopp.MPI.COMM_WORLD.size)
cellGrid = espressopp.tools.decomp.cellGrid(box, nodeGrid, rc=1.5, skin=0.3)
system.storage = espressopp.storage.DomainDecomposition(system,nodeGrid,cellGrid)

vl = espressopp.VerletList(system, cutoff=1.4)
lj1 = espressopp.interaction.VerletListLennardJones(vl)
lj2 = espressopp.interaction.VerletListLennardJones(vl)
lj3 = espressopp.interaction.VerletListLennardJones(vl)
lj4 = espressopp.interaction.VerletListLennardJones(vl)

system.addInteraction(lj1, 'lj1')
system.addInteraction(lj2, 'lj2')
system.addInteraction(lj3, 'lj3')
system.addInteraction(lj4)

# Checks if all interactions are present.
assert set(['lj1', 'lj2', 'lj3']) == set(system.getAllInteractions().keys())
assert id(lj1) == id(system.getInteractionByName('lj1'))

assert id(lj1) == id(system.getInteraction(0))
assert id(lj2) == id(system.getInteraction(1))
assert id(lj3) == id(system.getInteraction(2))

# Checks remove by name.
assert system.getNumberOfInteractions() == 4
system.removeInteractionByName('lj2')
assert system.getNumberOfInteractions() == 3

# Checks if interactions are renumbered correctly.
assert id(lj1) == id(system.getInteractionByName('lj1'))
assert id(lj3) == id(system.getInteractionByName('lj3'))
