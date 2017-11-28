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
  cd ./SLSPS_Simulations
  
Then from an ipython shell, first import the library and load a sample SLSPS
simulation:

.. code:: python

   from SLSPS_Simulations import *
   self = loadpickle('Simulations/SLSPS_Optimized')

The loaded SLSPS simulation *self* contains all of the information for a single
realization of the *Optimized* survey version including information about the
target stars and their simulated planetary systems.

For example, we can view the J-band magnitudes of all of the target stars::

  $ print self.Jmag
  
We can also view some select properties of one of the host stars::

  i = 0
  print self.Jmag[i], self.Teff[i], self.dist[i], self.Prot[i]

Alternatively with the appropriate units::

  attributes = ['Jmag', 'Teff', 'dist', 'Prot']
  for j in range(len(attributes)):
    print '%s = %.2f %s' %(attributes[j], getattr(self, attributes[j])[i], self.units_star[attributes[j]])

Or we Similarly for planetary system parameters::

  



Acknowledgement
---------------

The results presented in the slsps pickles are derived from the simulations in
Cloutier et al 2017 (link to paper). If you use the results of these simulations
in your own work please cite the aforementioned study.

