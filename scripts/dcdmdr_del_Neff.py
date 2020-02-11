
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class

Planck2015_par = {'omega_cdm':0.1198,'omega_b':0.02225, 'ln10^{10}A_s': 3.094, '100*theta_s':1.04077, 'tau_reio':0.079, 'n_s':0.9645}

#Lambda CDM Planck2015
LCDM = Class()
LCDM.set(Planck2015_par)
LCDM.compute()


kappa = [0.5, 1., 2., 4.]

DCDMDR = [Class() for i in range(len(kappa))]
for i in range(len(DCDMDR)):
	DCDMDR[i].set(Planck2015_par)
	DCDMDR[i].set({'omega_cdm':1e-10, 'omega_dcdm': 0.1198, 'zeta_dcdm':0.1, 'kappa_dcdm':kappa[i], 'a_t_dcdm': 1e-7})
	DCDMDR[i].compute()



del_Neff_0 = [m.get_current_derived_parameters(['del_Neff_0_dr'])['del_Neff_0_dr']  for m in DCDMDR]
del_Neff_rec = [m.get_current_derived_parameters(['del_Neff_rec_dr'])['del_Neff_rec_dr']  for m in DCDMDR]
a_rec = [1./(1.+m.get_current_derived_parameters(['z_rec'])['z_rec']) for m in DCDMDR]

print(del_Neff_0)
print(del_Neff_rec)

print(a_rec)
