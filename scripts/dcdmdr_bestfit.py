from classy import Class
import numpy as np
import matplotlib.pyplot as plt



LCDM = Class()
Planck2018_par = {'omega_b':0.02236, 'omega_cdm':0.1202, 'h':0.6727, 'tau_reio':0.0544, 'ln10^{10}A_s':3.045, 'n_s':0.9649, 'output' :'tCl ,pCl ,lCl ,mPk','lensing':'yes'}
#'100*theta_s': 1.0409
LCDM.set(Planck2018_par)
LCDM.compute()

'''
DCDMDR_bestfit = [Class() for i in xrange(5)]
Labels = ['$a_t = 10^{-1.5}$, $\kappa = 1$, $\zeta=0.06$', '$\kappa = 0.5$', '$\kappa = 1$', '$\kappa = 2$', '$\kappa = 4$']
for DCDMDR in DCDMDR_bestfit:
	DCDMDR.set(Planck2018_par)
DCDMDR_bestfit[0].set({'omega_b':0.022178, 'omega_cdm':1e-10, 'omega_dcdm':0.113522, 'h':0.7150, 'tau_reio':0.055282, 'ln10^{10}A_s':3.045337, 'n_s':0.96153, 'kappa_dcdm':1., 'a_t_dcdm':10**(-1.5), 'zeta_dcdm':0.06})
DCDMDR_bestfit[1].set({'omega_b':0.02239935, 'omega_cdm':1e-10, 'omega_dcdm':0.1198801, 'h':0.68054, 'tau_reio':0.04884694, 'ln10^{10}A_s':3.032332, 'n_s':0.9626247, 'kappa_dcdm':0.5, 'a_t_dcdm':10**(-6.109745), 'zeta_dcdm':10**(-1.594968)})
DCDMDR_bestfit[2].set({'omega_b':0.02232575, 'omega_cdm':1e-10, 'omega_dcdm':0.1204204, 'h':0.677151, 'tau_reio':0.055385, 'ln10^{10}A_s':3.041202, 'n_s':0.963461, 'kappa_dcdm':1., 'a_t_dcdm':10**(-5.715253), 'zeta_dcdm':10**(-5.067891)})
DCDMDR_bestfit[3].set({'omega_b':0.02240707, 'omega_cdm':1e-10, 'omega_dcdm':0.1201736, 'h':0.67872, 'tau_reio':0.05736339, 'ln10^{10}A_s':3.050465, 'n_s':0.9640579, 'kappa_dcdm':2., 'a_t_dcdm':10**(-6.3868), 'zeta_dcdm':10**(-4.9829)})
DCDMDR_bestfit[4].empty()
DCDMDR_bestfit[4].set({'omega_b':0.02234595, 'omega_cdm':1e-10, 'omega_dcdm':0.1193118, '100*theta_s':1.041790, 'tau_reio':0.05257339, 'ln10^{10}A_s':3.03597, 'n_s':0.967664, 'kappa_dcdm':4., 'a_t_dcdm':10**(-1.10002), 'zeta_dcdm':10**(-9.473855), 'output' :'tCl ,pCl ,lCl ,mPk','lensing':'yes'})
'''
DCDMDR_bestfit = [Class() for i in xrange(1)]
Labels = ['Planck+HST+SZ']
DCDMDR_bestfit[0].set(Planck2018_par)
DCDMDR_bestfit[0].set({'omega_b':0.022434, 'omega_cdm':1e-10, 'h':0.7136, 'a_t_dcdm':10**(-2.4316), 'zeta_dcdm':0.0289, 'omega_dcdm':0.11468})

for DCDMDR in DCDMDR_bestfit:
	DCDMDR.compute()

print(DCDMDR_bestfit[0].h())

LCDM_cls = LCDM.lensed_cl(2500)
ll = LCDM_cls['ell'][2:]


fig = plt.figure()
ax1= fig.add_subplot(211)
ax2 = fig.add_subplot(212)

T_cmb = LCDM.T_cmb()
ax1.plot(ll, LCDM_cls['tt'][2:]*ll*(ll+1)*T_cmb**2 /2./np.pi, label = '$\Lambda$CDM', color='black')


for DCDMDR in DCDMDR_bestfit:
	DCDMDR_cls = DCDMDR.lensed_cl(2500)
	DCDMDR_ll = DCDMDR_cls['ell'][2:]
	l = ax1.plot(DCDMDR_ll, DCDMDR_cls['tt'][2:]*DCDMDR_ll*(DCDMDR_ll+1)*T_cmb**2 /2./np.pi, label = Labels[DCDMDR_bestfit.index(DCDMDR)])
	print(ll - DCDMDR_ll)
	ax2.plot(ll, (DCDMDR_cls['tt'][2:] - LCDM_cls['tt'][2:])/LCDM_cls['tt'][2:], color = l[0].get_c())
	

ax1.grid()
ax2.grid()
ax1.set_xlim(1, 2500); ax1.set_xscale('log')
ax2.set_xlim(1, 2500); ax2.set_xscale('log')

ax1.legend()
plt.title("Fit to Planck Data")
plt.show()
