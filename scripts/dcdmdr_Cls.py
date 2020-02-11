
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class


# In[ ]:

Planck2015_par = {'omega_cdm':0.1198,'omega_b':0.02225, 'ln10^{10}A_s': 3.094, '100*theta_s':1.04077, 'tau_reio':0.079, 'n_s':0.9645,'output' :'tCl ,pCl ,lCl ,mPk','lensing':'yes'}
#    , 'gauge':'newtonian' 'h':0.67   'back_integration_stepsize':5e-5
#Lambda CDM Planck2015
LCDM = Class()
LCDM.set(Planck2015_par)
LCDM.compute()

LCDMNeff  = Class()
LCDMNeff.set(Planck2015_par)
LCDMNeff.set({'N_ur':3.046 + 0.42})
LCDMNeff.compute()



DCDMDR = [Class() for i in range(6)]

DCDMDR[0].set({'zeta_dcdm':0.2, 'kappa_dcdm':2., 'a_t_dcdm': 5e-2})
DCDMDR[1].set({'zeta_dcdm':0.2, 'kappa_dcdm':0.5, 'a_t_dcdm': 5e-2})
DCDMDR[2].set({'zeta_dcdm':0.1, 'kappa_dcdm':2., 'a_t_dcdm': 5e-4})
DCDMDR[3].set({'zeta_dcdm':0.1, 'kappa_dcdm':0.5, 'a_t_dcdm': 5e-4})
DCDMDR[4].set({'zeta_dcdm':2.5, 'kappa_dcdm':2., 'a_t_dcdm': 5e-6})
DCDMDR[5].set({'zeta_dcdm':2.5, 'kappa_dcdm':0.5, 'a_t_dcdm': 5e-6})

style = [('-.', 'green', '$\zeta=0.2, a_t=5\cdot10^{-2}$'), ('-.', 'red', ''), 
				('--', 'green', '$\zeta=0.1, a_t=5\cdot10^{-4}$'), ('--', 'red', ''), 
				('-', 'green', '$\zeta=2.5, a_t=5\cdot10^{-6}$'), ('-', 'red', '')]


for i in range(len(DCDMDR)):
	DCDMDR[i].set(Planck2015_par)
	DCDMDR[i].set({'omega_cdm':1e-10, 'omega_dcdm_at_rec': 0.1198})
	DCDMDR[i].compute()



cls = LCDM.lensed_cl(2500)
Neff_cls = LCDMNeff.lensed_cl(2500)
dcdmdr_cls = [DCDMDR[i].lensed_cl(2500) for i in range(len(DCDMDR))]

T_cmb = LCDM.T_cmb()

print(cls)
ll = cls['ell'][2:]
clTT = cls['tt'][2:]

fig = plt.figure(figsize=(12, 9))
ax1= fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.subplots_adjust(wspace=0)

ax1.plot(ll, clTT*ll*(ll+1)*T_cmb**2 /2./np.pi, label = '$\Lambda$CDM', color='black')
ax1.plot(ll, Neff_cls['tt'][2:]*ll*(ll+1)*T_cmb**2  /2./np.pi, label = '$\Lambda$CDM + $\Delta N_{eff}$', color='black', linestyle='--')
ax2.plot(ll, [0.]*len(ll), color='black')
ax2.plot(ll, (Neff_cls['tt'][2:] / clTT -1), color='black', linestyle='--')

print("LCDM: Omega0_Lambda = " + str(LCDM.get_current_derived_parameters (['Omega0_lambda'])))

for i in range(len(dcdmdr_cls)):
	print("DCDMDR " + str(i) + ": Omega0_Lambda = " + str(DCDMDR[i].get_current_derived_parameters(['Omega0_lambda'])))
	dcdmdr_ll = dcdmdr_cls[i]['ell'][2:]
	dcdmdr_clTT = dcdmdr_cls[i]['tt'][2:]
	ax1.plot(ll, dcdmdr_clTT*ll*(ll+1)*T_cmb**2 /2./np.pi, color = style[i][1], linestyle = style[i][0], label = style[i][2])
	ax2.plot(ll, (dcdmdr_clTT/clTT -1), color = style[i][1], linestyle = style[i][0], label = style[i][2])

ax1.legend(loc='upper left'); ax1.set_xscale('log'); ax1.set_xlim(left = 2, right=2500)
ax1.grid();

ax2.grid(); ax2.set_xscale('log');
ax2.set_xlim(left=2, right=2500); ax2.set_ylim(bottom=-0.3, top = 0.3)

#plt.tight_layout()
#plt.subplots_adjust(right = 0.8)


kk = np.logspace(-3, 0., 700)# k in h/Mpc

#for k in kk:
Pk = np.array([LCDM.pk(k*LCDM.h(),0.)*LCDM.h()**3 for k in kk]) # 

fig = plt.figure(figsize=(12, 9))
ax1= fig.add_subplot(211)
ax2 = fig.add_subplot(212)
fig.subplots_adjust(wspace=0)

ax1.plot(kk, Pk, color='black', label='$\Lambda$CDM')
ax2.plot(kk, [0.]*len(Pk), color='black')

Pk_Neff = np.array([LCDMNeff.pk(k*LCDMNeff.h(),0.)*LCDMNeff.h()**3 for k in kk])
ax1.plot(kk, Pk_Neff, color='black', linestyle='--', label='$\Lambda$CDM + $\Delta N_{eff}$')
ax2.plot(kk, Pk_Neff/Pk - 1, color='black', linestyle='--')

for i in range(len(DCDMDR)):
	Pk_dcdmdr = np.array([DCDMDR[i].pk(k*DCDMDR[i].h(),0.)*DCDMDR[i].h()**3 for k in kk])
	ax1.plot(kk, Pk_dcdmdr, color = style[i][1], linestyle = style[i][0], label = style[i][2])
	ax2.plot(kk, Pk_dcdmdr/Pk -1., color = style[i][1], linestyle = style[i][0], label = style[i][2])

ax1.set_yscale('log'); ax1.set_xscale('log');
ax1.grid(); ax1.set_xlim(left=1e-3, right = 1) 
ax1.legend(loc='lower left');
ax2.set_xlim(left = 1e-3, right = 1)
ax2.grid(); ax2.set_xscale('log');
ax2.set_ylim(bottom=-0.3, top=0.7)



plt.show()
# In[ ]:


