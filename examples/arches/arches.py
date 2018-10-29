#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

import numpy as np
import matplotlib
# ~ matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

import nngt
import dense as ds
from dense.units import *

current_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
main_dir = current_dir[:current_dir.rfind("/")]


'''
Main parameters
'''

num_neurons = 1000

num_omp = 6

soma_radius = 3.
use_uniform_branching = False
use_vp = False
use_run_tumble = True
use_critical_resource = False

gc_model = 'persistent_random_walk'

neuron_params = {
    "growth_cone_model": gc_model,
    "use_uniform_branching": use_uniform_branching,
    "use_van_pelt": use_vp,
    "sensing_angle": 0.14,
    "speed_growth_cone": 0.15 * um / minute,
    "filopodia_wall_affinity": 100.,
    "filopodia_finger_length": 5. * um,
    "filopodia_min_number": 20,
    "persistence_length": 400. * um,
    "thinning_ratio": 1./2000.,

    "soma_radius": soma_radius * um,
    'B' : 10. * cpm,
    'T' : 10000. * minute,
    'E' : 0.7,
}

dendrite_params = {
    "use_van_pelt": use_vp,
    "growth_cone_model": gc_model,
    "speed_growth_cone": 0.05 * um / minute,
    "filopodia_wall_affinity": 0.00,
}


'''
Check for optional parameters
'''

if use_uniform_branching:
    neuron_params["uniform_branching_rate"] = 0.001

'''
Simulation
'''

def step(time, loop_n, plot=True):
    ds.Simulate(time)
    if plot:
        ds.PlotNeuron(show_nodes=True, show=True)


if __name__ == '__main__':
    kernel = {
        "seeds": range(num_omp),
        "num_local_threads": num_omp,
        "resolution": 30. * minute,
        "adaptive_timestep": -1.,
        "environment_required": True,
    }

    culture_file = current_dir + "arches_3.svg"
    ds.SetKernelStatus(kernel, simulation_ID="ID")
    gids, culture = None, None
    print(ds.GetKernelStatus("num_local_threads"))

    if kernel["environment_required"]:
        culture = ds.SetEnvironment(culture_file, min_x=0, max_x=800)
        # generate the neurons inside the left chamber
        pos = culture.seed_neurons(
            neurons=num_neurons, soma_radius=soma_radius)
        neuron_params['position'] = pos
    else:
        neuron_params['position'] = np.random.uniform(-1000, 1000, (200, 2)) * um

    print("Creating neurons")
    gids = ds.CreateNeurons(
        n=num_neurons, growth_cone_model="persistent_rw_critical",
        culture=culture, params=neuron_params,
        dendrites_params=dendrite_params, num_neurites=2)

    print("neuron created, starting simu")

    step(5 * day, 0, False)

    # prepare the plot
    ds.plot.PlotNeuron(show_density=True, dstep=4., dmax=10, cmap="jet")