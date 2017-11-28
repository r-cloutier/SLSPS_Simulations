from imports import *

global G
G = 6.67e-11

# Conversion functions
def days2sec(t):
    return t*24.*60*60
def sec2days(t):
    return t / days2sec(1)
def Msun2kg(m):
    return m*1.98849925145e30
def kg2Msun(m):
    return m / Msun2kg(1)
def Rsun2m(r):
    return r*695500e3
def m2Rsun(r):
    return r / Rsun2m(1)
def Mearth2kg(m):
    return m*6.04589804468e24
def kg2Mearth(m):
    return m / Mearth2kg(1)
def Rearth2m(r):
    return r*6371e3
def m2Rearth(r):
    return r / Rearth2m(1)
def AU2m(r):
    return r*1.495978707e11
def m2AU(r):
    return r / AU2m(1)
def pc2m(r):
    return r*3.08567758149137e16
def m2pc(r):
    return r / pc2m(1)

def RV_K(P_days, Ms_Msun, mp_Mearth, ecc=0., inc_deg=90.):
    '''Compute the RV semiamplitude in m/s.'''
    P, Ms, mp, inc = days2sec(P_days), Msun2kg(Ms_Msun), Mearth2kg(mp_Mearth), \
                     np.deg2rad(inc_deg)
    return (2*np.pi*G/(P*Ms*Ms))**(1./3) * mp*np.sin(inc) / np.sqrt(1.-ecc**2)


def semimajoraxis(P_days, Ms_Msun, mp_Mearth):
    '''Compute the semimajor axis in AU from Kepler's third law.'''
    P, Ms, mp = days2sec(P_days), Msun2kg(Ms_Msun), Mearth2kg(mp_Mearth)
    return m2AU((G*(Ms+mp)*P*P / (4*np.pi*np.pi))**(1./3))


def period_sma(a_AU, Ms_Msun, mp_Mearth):
    '''Compute the orbital period in days from Kepler's third law.'''
    a, Ms, mp = AU2m(a_AU), Msun2kg(Ms_Msun), Mearth2kg(mp_Mearth)
    return sec2days(np.sqrt(4*np.pi*np.pi*a**3 / (G*(Ms+mp))))


def projected_sep(SMA_AU, dist_pc):
    '''Compute the projected angular separation in arcseconds of a planet 
    from its host star.'''
    SMA, dist = AU2m(SMA_AU), pc2m(dist_pc)
    return np.rad2deg(SMA / dist) * 3.6e3


def planet_contrast(rp_Rearth, SMA_AU, albedo=.3):
    '''Compute the reflected light contrast of a planet.'''
    rp, SMA = Rearth2m(rp_Rearth), AU2m(SMA_AU)
    return albedo * (rp / SMA)**2


def get_baraffe_Ls(Ms, age=2):
    # Get Baraffe data
    baraffe = np.loadtxt('input_data/BCAH98.dat')
    barmass = baraffe[:,0]    # Msun
    barage = baraffe[:,1]     # Gyrs
    barTeff = baraffe[:,2]    # K
    barL = baraffe[:,4]       # log(L/Lsun)
    # Interpolate to get L
    lint_L = lint(np.array([barmass, barage]).T, barL)
    return 10**(lint_L(Ms, float(age)))   # Lsun
