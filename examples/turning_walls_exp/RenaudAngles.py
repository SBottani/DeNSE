# -*- coding: utf-8 -*-
#
# RenaudAngles.py
#
# This file is part of DeNSE.
#
# Copyright (C) 2019 SeNEC Initiative
#
# DeNSE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# DeNSE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeNSE. If not, see <http://www.gnu.org/licenses/>.


import dense as ds
from dense.units import *

import matplotlib.pyplot as plt
import os

import numpy as np


current_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
main_dir = current_dir[:current_dir.rfind("/")]

plt.rc("font", size=18)

'''
Main parameters
'''

num_neurons = 100  # number of neurons
soma_radius = 4.*um

# Environment parameters and file
min_x = 0  # "Arches20reduced2c2.svg" has x segment of length 164.91 cm
max_x = 500  # and height of 84.94 cm
min_y = -132
max_y = 132 # set here same aspect ratio  X , Y as size of environment
#  in the svg file
culture_file = current_dir + "/angle40.svg"

neuron_params = {
    "growth_cone_model": 'run-and-tumble'
    "axon_angle": 0.*deg,
    "use_uniform_branching": False,
    "taper_rate": 4./700.,
    "uniform_branching_rate": 0.001 * cpm,
    "persistence_length": 400.*um,
    "sensing_angle": 45.*deg,
    "soma_radius": soma_radius,
    "speed_growth_cone": 0.1*um/minute,
    "filopodia_wall_affinity": 8000.,
    "filopodia_finger_length": 10.*um,
    "filopodia_min_number": 30
        # "gc_split_angle_mean": 30.,
    # "gc_split_angle_std": 10.,
    # "B" : 6.5,
    # "E" : 0.08,
    # "S" : 1.02, # large S leads to core dump
    # "T" : 0.01,
    #~ "axon_angle":0.,
    # #critical_resource model
    # "critical_resource_amount":100.,
    # "critical_resource_initial_demand":1.,
    # "critical_resource_topo_coeff": 1.,
    # "critical_resource_elongation_th": 9.,
    # "critical_resource_std": 0.1,
    # "critical_resource_retraction_th": 2.,
    #~ "critical_resource_speed_factor": 0.5,
    # "critical_resource_split_th": 80.,
    #~ "critical_resource_split_tau": 100.,
    # "lateral_branching_angle_mean": 50.,
    # "lateral_branching_angle_std": 20.,


}

neuron_params['growth_cone_model'] = 'run-and-tumble'

dendrite_params = {

}


def step(n, loop_n, plot=True):
    ds.simulate(n*minute)
    if plot:
        ds.plot.plot_neurons(show_nodes=True, show=True)


if __name__ == '__main__':
    number_of_threads = 10
    kernel = {"seeds": range(number_of_threads),
              "num_local_threads": number_of_threads,
              "resolution": 10. * minute, #10
              "adaptive_timestep": -1.,
              "environment_required": True}

    # kernel= {
    #     "seeds": [i for i in range(num_omp)],
    #     "num_local_threads": num_omp,
    #     "resolution": 10.*minute,
    #     #~ "adaptive_timestep": -1.
    # }

    ds.set_kernel_status(kernel, simulation_id="ID")

    gids = None
    culture = ds.set_environment(culture_file, min_x=min_x, max_x=max_x)

    ds.environment.plot.plot_shape(culture, show=True)

    # generate the neurons inside the left chamber
    pos_left = culture.seed_neurons(neurons=num_neurons, xmin=0, xmax=100,
                                    soma_radius=soma_radius)
    neuron_params['position'] = pos_left

    gids = ds.create_neurons(n=num_neurons, culture=culture,
                             params=neuron_params,
                             num_neurites=1)

    #~ ds.plot.plot_neurons(show=True)

    #~ step(200, 0, False)
    # Launch simulation
    for loop_n in range(5):
        step(1000, loop_n, True)

    # prepare the plot
    fig, ax = plt.subplots()
    #~ ds.plot.plot_neurons(gid=range(100), culture=culture, soma_color="k",
    #~ axon_color='#00ff00a0', axis=ax, show=False)
    #~ ds.plot.plot_neurons(gid=range(100, 200), show_culture=False, axis=ax,
    #~ soma_color='k', axon_color='#ffa000a0',
    #~ show=True)
    # ax, ax2 = ds.plot.plot_neurons(gid=range(40), culture=culture, soma_color="k",
    #                    axon_color='g', show_density=True, dstep=8., dmax=50.,
    #                    dmin=None, axis=ax, show=False)

    ax, ax2 = ds.plot.plot_neurons(culture=culture,
                                   soma_alpha=0.4,
                                   axon_color='g',
                                   gc_color="r",
                                   axis=ax,
                                   show_density=True,
                                   dstep=100.,
                                   x_min=min_x,
                                   x_max=max_x,
                                   y_min=min_y,
                                   y_max=max_y,
                                   #dmin=0,
                                   #dmax=10,
                                   show=False)

    ax2.set_ylim(bottom=-5)
    ax2.set_xlim(left=0)

    plt.tight_layout()

    ds.environment.plot_shape(culture, alpha=0., axis=ax2, ec=(1, 1, 1, 0.5),
                              show=True)
