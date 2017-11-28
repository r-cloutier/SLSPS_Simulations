from imports import *
import rvs_custom as rvs


def loadpickle(fname):
    f = open(fname, 'rb')
    self = pickle.load(f)
    f.close()
    return self


class SLSPS_Simulation():

    def __init__(self, pickle_name, fname):
        
        self._pickle_name, self.fname = pickle_name, fname


    def create_SLSPS_simulation(self):
        '''
        Compile the results from a single MC realization from the simulated 
        SLSPS to a concise file including all the necessary information.
        '''
        d = loadpickle(self._pickle_name)

        # get single realization indices 
        self.Nstar = np.unique(d.starnum_EP).size
        self._inds = np.array([np.where(d.starnum_EP == starnum)[0][0]
                               for starnum in np.unique(d.starnum_EP)]) 

        # get parameters
        self._get_star(d)
        self._get_planets(d)
        self._get_auxiliary(d)
	self._get_attribute_units()
        
        self._clean_up()
        self._pickleobject()
        
        

    def _get_star(self, d):
        '''
        Get the stellar parameters from one MC realization. 
        '''
        self.starnums = np.arange(self.Nstar)
        self.Jmag, self.SpT = d.Jmag_EP[self._inds], d.SpT_EP[self._inds]
        self.Ms, self.Rs = d.Ms_EP[self._inds], d.Rs_EP[self._inds]
        self.Teff, self.dist = d.Teff_EP[self._inds], d.dist_EP[self._inds]
        self.Prot, self.vsini = d.Prot_EP[self._inds], d.vsini_EP[self._inds]
        self.I, self.fB = d.I_EP[self._inds], d.B_EP[self._inds]
        self._get_HZ_Plims()
        

    def _get_HZ_Plims(self):
        '''
        Compute the orbital period corresponding to the inner and outer edge 
        of the habitable zone defined by the water-loss and maximum greenhouse 
        limits respectively. Based on equations from Kopparapu et al 2013.
        '''
        # define coefficients
        SeffSun = np.array([1.014, .3438])
        a = np.array([8.1774e-5, 5.8942e-5])
        b = np.array([1.7063e-9, 1.6558e-9])
        c = np.array([-4.3241e-12, -3.0045e-12])
        d = np.array([-6.6462e-16, -5.2983e-16])
        Ts = self.Teff - 5780.

        # get stellar luminosity from Baraffe et al 1998  
        Ls = rvs.get_baraffe_Ls(self.Ms)

        # return inner and outer periods in days
        Seffs = np.zeros((Ts.size, 2))
        for i in range(2):
            Seffs[:,i] = SeffSun[i] + a[i]*Ts + b[i]*Ts**2 + \
                         c[i]*Ts**3 + d[i]*Ts**4
        ain, aout = np.sqrt(Ls/Seffs[:,0]), np.sqrt(Ls/Seffs[:,1])
        self.HZPlims = np.array([rvs.period_sma(ain, self.Ms, 0),
                                 rvs.period_sma(aout, self.Ms, 0)]).T


    def _get_planets(self, d, albedo=.3):
        '''
        Get the planetary system parameters from one MC realization. 
        '''
        self.nplanets = d.nplanets_EP[self._inds].astype(int)
        self.nplanets_detected = \
                        d.nplanets_detectedCV_noalias_EP[self._inds].astype(int)
        self.Ps, self.T0s = d.Ps_EP[self._inds], d.T0s_EP[self._inds]
        self.rps, self.mps = d.Rps_EP[self._inds], d.Mps_EP[self._inds]
        self.incs, self.eccs = d.incs_EP[self._inds], d.eccs_EP[self._inds]
        self.HZ_flags = d.inHZ_EP[self._inds]
        self.imagable_flags = d.imagable_EP[self._inds]
        self.detection_flags = d.detectedCV_noalias_EP[self._inds]

        # compute quantities of interest 
        self.mpsinis = self.mps * np.sin(np.deg2rad(self.incs))
        Ms2d = np.repeat(self.Ms, self.Ps.shape[1]).reshape(self.Nstar,
                                                            self.Ps.shape[1])
        self.smas = rvs.semimajoraxis(self.Ps, Ms2d, self.mps)
        self.Ks = rvs.RV_K(self.Ps, Ms2d, self.mps, self.eccs, self.incs)
        dist2d = np.repeat(self.dist,self.Ps.shape[1]).reshape(self.Nstar,
                                                               self.Ps.shape[1])
        self.seps = rvs.projected_sep(self.smas, dist2d)
        self.albedos = np.zeros(self.Ps.shape) + albedo
        self.contrasts = rvs.planet_contrast(self.rps, self.smas, self.albedos)

        self._trim_planet_arrays()
                            
                            
    def _trim_planet_arrays(self):
        '''
        Remove unnecessary entires in the planets arrays.
        '''
        nplanets_max = int(self.nplanets.max())
        self.Ps              = self.Ps[:,:nplanets_max]
        self.T0s             = self.T0s[:,:nplanets_max]
        self.rps             = self.rps[:,:nplanets_max]
        self.mps             = self.mps[:,:nplanets_max]
        self.incs            = self.incs[:,:nplanets_max]
        self.eccs            = self.eccs[:,:nplanets_max]
        self.HZ_flags        = self.HZ_flags[:,:nplanets_max]
        self.imagable_flags  = self.imagable_flags[:,:nplanets_max]
        self.detection_flags = self.detection_flags[:,:nplanets_max]        
        self.mpsinis         = self.mpsinis[:,:nplanets_max]
        self.smas            = self.smas[:,:nplanets_max]
        self.Ks              = self.Ks[:,:nplanets_max]
        self.seps            = self.seps[:,:nplanets_max]
        self.albedos         = self.albedos[:,:nplanets_max]
        self.contrasts       = self.contrasts[:,:nplanets_max]


    def _get_auxiliary(self, d, albedo=.3):
        '''
        Get any outstanding parameters of interest.
        '''
        self.nobs = d.nobs_EP[self._inds]
        self.sigmaRV = d.sigmaRV_EP[self._inds]


    def _get_attribute_units(self):
        self.units_star = {'starnums' : '',
                           'Jmag' : '',
                           'SpT' : 'numerical spectral type',
                           'Ms' : 'solar masses',
                           'Rs' : 'solar radii',
                           'Teff' : 'kelvin',
                           'dist' : 'parsecs',
                           'Prot' : 'days',
                           'vsini' : 'km/s',
                           'I' : 'deg',
                           'fB' : 'kiloGauss',
                           'HZPlims' : 'days'}
        self.units_planet = {'nplanets' : '',
                             'nplanets_detected' : '',
                             'Ps' : 'days',
                             'T0s' : 'BJD',
                             'rps' : 'Earth radii',
                             'mps' : 'Earth masses',
                             'incs' : 'deg',
                             'eccs' : '',
                             'HZ_flags' : 'binary flag',
                             'imagable_flags' : 'binary flag',
                             'detection_flags' : 'binary flag',
                             'mpsinis' : 'Earth masses',
                             'smas' : 'AU',
                             'Ks' : 'm/s',
                             'seps' : 'arcsec',
                             'albedos' : '',
                             'contrasts' : ''}
        self.units_auxiliary = {'nobs' : '',
                                'sigmaRV' : 'm/s'}

        
    def _clean_up(self):
        '''
        Remove unwanted attributes.
        '''
        del self._pickle_name
        del self._inds


    def _pickleobject(self):
        '''
        Write the results to a pickle.
        '''
        f = open(self.fname, 'wb')
        pickle.dump(self, f)
        f.close()
