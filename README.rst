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

  git clone https://github.com/r-cloutier/SLSPS_Simulations.git
  cd ./SLSPS_Simulations
  
Then from an ipython shell, import the library and load a sample SLSPS
simulation:

.. code:: python

   >>> from SLSPS_Simulations import *
   >>> self = loadpickle('Simulations/SLSPS_Optimized')

The loaded SLSPS simulation *self* contains all of the information for a single
realization of the *Optimized* survey version including information about the
target stars and their simulated planetary systems.

For example, we can view the J-band magnitudes of all of the target stars:

.. code:: python

  >>> print self.Jmag
  [  5.244   5.335   5.189   5.721   5.714   6.222   7.085   6.884   5.934
   5.583   5.95    6.505   6.104   6.106   6.789   6.581   7.258   6.905
   6.301   6.838   6.314   6.724   7.514   6.706   7.09    6.51    7.124
   7.184   6.752   7.319   6.812   7.465   7.617   7.333   7.561   7.195
   8.394   7.601   6.9     8.235   6.908   7.391   7.555   7.273   7.635
   8.275   7.562   7.734   7.295   4.203   5.252   8.438   8.857   5.538
   8.742  10.27    5.104   9.908   5.827   9.436   6.608   7.949   7.294
   8.424   5.36    6.176   8.853   8.74    9.148   8.242   8.639   5.902
   6.161   5.888   6.36    8.11    8.488   8.64    6.529   8.662   8.456
   9.871   8.775   6.579   8.496   6.419   7.734   7.278   6.625   9.842
   7.337   7.787   9.945   7.819   9.35    9.029   8.367   7.901   8.768
   8.323]
  
We can also view some select properties of one of the host stars:

.. code:: python

  >>> i = 0
  >>> print self.Jmag[i], self.Teff[i], self.dist[i], self.Prot[i]
  5.244 3229.971594 1.833516685 121.0
  
Alternatively and with the appropriate units:

.. code:: python

  >>> attributes = ['Jmag', 'Teff', 'dist', 'Prot']
  >>> for j in range(len(attributes)):
  ...     print '%s = %.2f %s' %(attributes[j], getattr(self, attributes[j])[i], self.units_star[attributes[j]])
  Jmag = 5.24 
  Teff = 3229.97 kelvin
  dist = 1.83 parsecs
  Prot = 121.00 days
  
All of the contents of the loaded SLSPS simulation file can be viewed in a
similar ways as above. See the ipython notebook ipython_example.ipynb for a more
detailed description and visualization of the files contents.


Acknowledgement
---------------

The results presented in the SLSPS simulation files were derived from the
Monte-Carlo simulations of the SLSPS presented in Cloutier et al 2017 (link to
paper). If you use the results of these simulations in your own work please
cite the aforementioned study.
