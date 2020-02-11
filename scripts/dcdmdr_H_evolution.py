# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from classy import Class


### reference model
Planck2015_par = {'omega_cdm':0.1198,'omega_b':0.02225, 'ln10^{10}A_s': 3.094, 'h':0.6727  , 'tau_reio':0.079, 'n_s':0.9645}
#   '100*theta_s':1.04077 
#Lambda CDM Planck2015
LCDM = Class()
LCDM.set(Planck2015_par)
#LCDM.set({'omega_cdm':1e-10, 'omega_dcdm': 0.1198, 'zeta_dcdm':0., 'kappa_dcdm':0., 'a_t_dcdm': 1e-3})
LCDM.compute()


### DCDMDR models with different kappa
kappa = [0.5, 1., 2., 4.]

DCDMDR = [Class() for i in range(len(kappa))]
for i in range(len(DCDMDR)):
	DCDMDR[i].set(Planck2015_par)
	DCDMDR[i].set({'omega_cdm':1e-10, 'omega_dcdm': 0.1198, 'zeta_dcdm':0.1, 'kappa_dcdm':kappa[i], 'a_t_dcdm': 1e-3})
	DCDMDR[i].compute()


ba_LCDM = LCDM.get_background()
ba_DCDMDR = [DCDMDR[i].get_background() for i in range(len(DCDMDR))]


print(ba_DCDMDR[0])

for i in range(len(ba_DCDMDR)):
	plt.plot(1/(ba_DCDMDR[i]['z']+1), ba_DCDMDR[i]['H [1/Mpc]']/ba_LCDM['H [1/Mpc]'], label = '$\kappa$ = ' + str(kappa[i]))

plt.legend(); plt.xscale('log'); 
plt.xlim(left=1e-7, right=1); plt.grid();


### get DMDR model with different decay rates
a_t = [5e-4, 5e-2, 5e-6]
DCDMDR = [Class() for i in range(len(a_t))]
for i in range(len(DCDMDR)):
	DCDMDR[i].set(Planck2015_par)
	DCDMDR[i].set({'omega_cdm':1e-10, 'omega_dcdm': 0.1198, 'zeta_dcdm':0.1, 'kappa_dcdm':2, 'a_t_dcdm': a_t[i]})
	DCDMDR[i].compute()


ba_LCDM = LCDM.get_background()
ba_DCDMDR = [DCDMDR[i].get_background() for i in range(len(DCDMDR))]

#### get LCDM model with N_eff
N_eff = [8./7.  * (11./4)**(4./3.) * ba_DCDMDR[2]['(.)rho_dr'][-40:]/ba_DCDMDR[2]['(.)rho_ur'][-40:] ]
print N_eff
LCDMN_eff = Class()
LCDMN_eff.set(Planck2015_par)
LCDMN_eff.set({'N_ur':3.046 + np.mean(N_eff)})
LCDMN_eff.compute()
ba_LCDMN_eff = LCDMN_eff.get_background()

### interpolate H 
H_LCDM = interp1d(ba_LCDM['z'], ba_LCDM['H [1/Mpc]'], kind='linear')
rho_crit_LCDM = interp1d(ba_LCDM['z'], ba_LCDM['(.)rho_crit'], kind='linear')

'''
plt.figure()
plt.plot(ba_LCDM['z'], ba_LCDM['H [1/Mpc]'], 'o')
plt.plot(ba_LCDM['z'], H_ba_LCDM(ba_LCDM['z']), '--')
plt.xscale('log'); plt.yscale('log')
plt.grid();
plt.gca().invert_xaxis()
'''

### plot 
plt.figure()
plt.plot(1/(ba_LCDMN_eff['z']+1), ba_LCDMN_eff['H [1/Mpc]']/H_LCDM(ba_LCDMN_eff['z']) - 1, label = '$\Lambda$CDM + $\Delta N_eff$', linestyle = '--', color='black')
#plt.plot(1/(ba_LCDMN_eff['z']+1), ba_LCDMN_eff['(.)rho_ur']/rho_crit_LCDM(ba_LCDMN_eff['z']), label = '$\Lambda$CDM + $\Delta N_eff$', linestyle = '--', color='black')

for i in range(len(ba_DCDMDR)):
	#l = plt.plot(1/(ba_DCDMDR[i]['z']+1), (ba_DCDMDR[i]['(.)rho_crit']/rho_crit_LCDM(ba_DCDMDR[i]['z'])) -1., label = '$a_t$ = ' + str(a_t[i]))
	l = plt.plot(1/(ba_DCDMDR[i]['z']+1), (ba_DCDMDR[i]['H [1/Mpc]']/H_LCDM(ba_DCDMDR[i]['z']))  - 1., label = '$a_t$ = ' + str(a_t[i]))
	plt.plot(1/(ba_DCDMDR[i]['z']+1), (ba_DCDMDR[i]['(.)rho_dr']/H_LCDM(ba_DCDMDR[i]['z'])**2), linestyle = '-.', color = l[0].get_color())
	plt.plot(1/(ba_DCDMDR[i]['z']+1), (ba_DCDMDR[i]['(.)rho_dr']/ba_DCDMDR[i]['(.)rho_crit']), linestyle = '--', color = l[0].get_color())
	#plt.plot(1/(ba_DCDMDR[i]['z']+1), (ba_DCDMDR[i]['(.)rho_crit']/H_LCDM(ba_DCDMDR[i]['z'])**2) - 1., linestyle = '-.', color = l[0].get_color())

plt.legend(loc = 'upper left'); plt.xscale('log');  plt.yscale('log')
plt.xlim(left=1e-7, right=1.); plt.ylim(bottom=1e-5, top=1); plt.grid();
plt.gca().get_yaxis().tick_right();

plt.show()
# In[ ]:


