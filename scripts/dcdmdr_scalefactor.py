
# coding: utf-8

# In[ ]:

# import necessary modules
# uncomment to get plots displayed in notebook
#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class


# In[ ]:

font = {'size'   : 20, 'family':'STIXGeneral'}
axislabelfontsize='large'
matplotlib.rc('font', **font)
matplotlib.mathtext.rcParams['legend.fontsize']='medium'


# In[ ]:

Planck2015_par = {'omega_cdm':0.1198,'omega_b':0.02225, 'ln10^{10}A_s': 3.094, '100*theta_s':1.04077, 'tau_reio':0.079, 'n_s':0.9645}

#Lambda CDM Planck2015
LCDM = Class()
LCDM.set(Planck2015_par)
LCDM.compute()


kappa = [0.5, 1., 2., 4.]

DCDMDR = [Class() for i in range(len(kappa))]
for i in range(len(DCDMDR)):
	DCDMDR[i].set(Planck2015_par)
	DCDMDR[i].set({'omega_cdm':1e-10, 'omega_dcdm': 0.1198, 'zeta_dcdm':0.1, 'kappa_dcdm':kappa[i], 'a_t_dcdm': 1e-3})
	DCDMDR[i].compute()


ba_LCDM = LCDM.get_background()
ba_DCDMDR = [DCDMDR[i].get_background() for i in range(len(DCDMDR))]

ba_LCDM.viewkeys()
ba_DCDMDR[0].viewkeys()

print(ba_DCDMDR[0])

rho_dcdm_0 = ba_DCDMDR[0]['(.)rho_dcdm'][-1]

for i in range(len(ba_DCDMDR)):
	plt.plot(1/(ba_DCDMDR[i]['z']+1), ba_DCDMDR[i]['(.)rho_dcdm']/(ba_DCDMDR[i]['z']+1)**3 /rho_dcdm_0, label = '$\kappa$ = ' + str(kappa[i]) )

plt.legend(); plt.xscale('log');
plt.xlim(left=1e-7); plt.grid()

plt.figure()

for i in range(len(ba_DCDMDR)):
	plt.plot(1/(ba_DCDMDR[i]['z']+1), ba_DCDMDR[i]['(.)rho_dr']/(ba_DCDMDR[i]['z']+1)**4 /rho_dcdm_0, label = '$\kappa$ = ' + str(kappa[i]))

plt.legend(); plt.xscale('log'); plt.yscale('log')
plt.xlim(left=1e-7, right=1); plt.grid(); plt.ylim(bottom=1e-9, top=1e-2)

plt.show()
# In[ ]:


