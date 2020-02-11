

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
	DCDMDR[i].set({'omega_cdm':1e-10, 'omega_dcdm': 0.1198, 'zeta_dcdm':0.1, 'kappa_dcdm':kappa[i], 'a_t_dcdm': 1e-3})
	DCDMDR[i].compute()


# 'omega_dcdm':0.1198

ba_LCDM = LCDM.get_background()
ba_DCDMDR = [DCDMDR[i].get_background() for i in range(len(DCDMDR))]

print(ba_DCDMDR[0])

#plt.plot(1/(ba_LCDM['z']+1), ba_LCDM['(.)rho_cdm'], label = 'LCDM', linestyle='--')

rho_dcdm_0 = ba_DCDMDR[0]['(.)rho_dcdm'][-1]

plt.plot(1/(ba_LCDM['z']+1), ba_LCDM['(.)rho_cdm']/(ba_LCDM['z']+1)**3 , label = 'LCDM', linestyle='--')

#plt.axvline(1/(LCDM.get_current_derived_parameters(['z_rec'])['z_rec']+1))
def rho_analytic(a,rho_0,kappa,at,zeta):
	return rho_0/a**3 *(1+zeta*(1-a**kappa)/(1+(a/at)**kappa))

for i in range(len(ba_DCDMDR)):
	#plt.plot(1/(ba_DCDMDR[i]['z']+1), ba_DCDMDR[i]['(.)rho_dcdm']/(ba_DCDMDR[i]['z']+1)**3 /rho_dcdm_0, label = '$\kappa$ = ' + str(kappa[i]) )
	a = 1/(ba_DCDMDR[i]['z']+1)
	l = plt.plot(a, ba_DCDMDR[i]['(.)rho_dcdm']*a**3, label = '$\kappa$ = ' + str(kappa[i]) )
	plt.plot(a,rho_analytic(1/(ba_DCDMDR[i]['z']+1),rho_dcdm_0,kappa[i],1e-3,0.1)*a**3, linestyle='-.', color = l[0].get_color())

plt.legend(); plt.xscale('log');
plt.xlim(left=1e-7); plt.grid()
plt.yscale('log')

plt.figure()

for i in range(len(ba_DCDMDR)):
	plt.plot(1/(ba_DCDMDR[i]['z']+1), ba_DCDMDR[i]['(.)rho_dr']/(ba_DCDMDR[i]['z']+1)**4 /rho_dcdm_0, label = '$\kappa$ = ' + str(kappa[i]))

plt.legend(); plt.xscale('log'); plt.yscale('log')
plt.xlim(left=1e-7, right=1); plt.grid(); plt.ylim(bottom=1e-9, top=1e-2)

plt.show()
# In[ ]:


