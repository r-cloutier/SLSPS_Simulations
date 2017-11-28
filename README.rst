Simulation files from the simulated SPIRou Legacy Survey-Planet Search (SLS-PS)
===============================================================================

Overview
--------

Cloutier et al 2018 (link to paper) ran a detailed Monte-Carlo simulation of 
the SLS-PS to make predictions of the survey's planet yield based on our 
current understanding of the occurrence rates of planets around M dwarfs and 
host star properties. This repository provides the details from one 
Monte-Carlo realization for each of the six survey versions presented in Sect. 
13 of Cloutier et al 2018. 

This repository includes the data presented for each survey version, in the 
form of a python pickle (https://docs.python.org/3/library/pickle.html), along
with the scripts required to access the data.

Quick Example
-------------

First clone the repository which includes all of the necessary python scripts
and the individual simulation files for each of the six survey versions::

  git clone https://github.com/r-cloutier/SLSPS_Pickles.git

Then from an ipython shell, first import the library and load a sample SLSPS
simulation:

.. code:: python

   from SLSPS_Simulations import *
   self = loadpickle('Simulations/SLSPS_Optimized')

The loaded file contains data for one realization of the *Optimized* version
of the simulated SLSPS. The data included are either pertaining to the host
star, the planetary system, or auxiliary parameters. The parameters from each
class and their units can be quickly viewed via:: 

  print self.units_star

Similarly, all planetary parameters can be accessed individually from the
*self.planet* object::

  print self.planet.Ps, self.planet.units.Ps

Lastly all time-series, in the form of numpy arrays, can be accessed from the
*self.timeseries* object. For example::

  import pylab as plt
  plt.errorbar(self.timeseries.bjd-245e4, self.timeseries.rvs, self.timeseries.erv, fmt='k.')
  plt.xlabel('BJD - 2,450,000'), plt.ylabel('Radial Velocity (m/s)')
  plt.show()
  

Acknowledgement
---------------

The results presented in the slsps pickles are derived from the simulations in
Cloutier et al 2017 (link to paper). If you use the results of these simulations
in your own work please cite the aforementioned study.
