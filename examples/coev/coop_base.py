
#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

"""This is the base code for all four coevolution examples from *Potter, M.
and De Jong, K., 2001, Cooperative Coevolution: An Architecture for Evolving
Co-adapted Subcomponents.* section 4.2. It shows in a concrete manner how to
re-use initialization code in some other examples.
"""

import random
import numpy as np

from deap import base, creator, tools

IND_SIZE = 64
SPECIES_SIZE = 50

def initTargetSet(schemata, size):
    """Initialize a target set with noisy string to match based on the
    schematas provided.
    """
    test_set = []
    for _ in range(size):
        test = list(random.randint(0, 1) for _ in schemata)
        # test = np.random.randint(0,2, len(schemata))
        for i, x in enumerate(schemata):
            if x == "0":
                test[i] = 0
            elif x == "1":
                test[i] = 1
        test_set.append(test)
    return test_set

def matchStrength(x, y):
    """Compute the match strength for the individual *x* on the string *y*.
    """
    return len([1 for xi, yi in zip(x, y) if xi == yi])

def matchStrengthNoNoise(x, y, n):
    """Compute the match strength for the individual *x* on the string *y*
    excluding noise *n*.
    """
    return len([1 for xi, yi, ni in zip(x, y, n) if ni != "#" and xi == yi])


def matchSetStrength(match_set, target_set):
    """Compute the match strength of a set of strings on the target set of
    strings. The strength is the maximum of all match string on each target.
    """
    return np.mean([max(matchStrength(m, t) for m in match_set) for t in target_set]),

def matchSetStrengthNoNoise(match_set, target_set, noise):
    """Compute the match strength of a set of strings on the target set of
    strings. The strength is the maximum of all match string on each target
    excluding noise.
    """
    return np.mean([max(matchStrengthNoNoise(m, t, noise) for m in match_set) for t in target_set]),


def matchSetContribution(match_set, target_set, index):
    """Compute the contribution of the string at *index* in the match set.
    """
    contribution = 0.0
    for t in target_set:
        i = np.argmax([matchStrength(m, t) for m in match_set])
        if i == index:
            contribution += matchStrength(match_set[i])
            
    return contribution / len(target_set),
     
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("bit", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.bit, IND_SIZE)
toolbox.register("species", tools.initRepeat, list, toolbox.individual, SPECIES_SIZE)
toolbox.register("target_set", initTargetSet)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/IND_SIZE)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("get_best", tools.selBest, k=1)
toolbox.register("evaluate", matchSetStrength)
