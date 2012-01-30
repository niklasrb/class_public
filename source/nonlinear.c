/** @file cl.c Documented nonlinear module
 *
 * Benjamin Audren and Julien Lesgourgues, 21.12.2010    
 *
 */

#include "nonlinear.h"

int nonlinear_pk_at_z(
		      struct nonlinear * pnl,
		      double z,
		      double * pz_density,
		      double * pz_velocity,
		      double * pz_cross,
		      int * k_size_at_z
		      ) {

  int last_index;
  int index_z;

  class_test(pnl->method == nl_none,
	     pnl->error_message,
	     "No non-linear spectra requested. You cannot call the function non_linear_pk_at_z()");

  class_call(array_interpolate_spline(pnl->z,
				      pnl->z_size,
				      pnl->p_density,
				      pnl->ddp_density,
				      pnl->k_size[0],
				      z,
				      &last_index,
				      pz_density,
				      pnl->k_size[0],
				      pnl->error_message),
	     pnl->error_message,
	     pnl->error_message);

  if ((pnl->method >= nl_trg_linear) && (pnl->method <= nl_trg)) {

    class_call(array_interpolate_spline(pnl->z,
					pnl->z_size,
					pnl->p_velocity,
					pnl->ddp_velocity,
					pnl->k_size[0],
					z,
					&last_index,
					pz_velocity,
					pnl->k_size[0],
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);
    
    class_call(array_interpolate_spline(pnl->z,
					pnl->z_size,
					pnl->p_cross,
					pnl->ddp_cross,
					pnl->k_size[0],
					z,
					&last_index,
					pz_cross,
					pnl->k_size[0],
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);

  }

  for (index_z=0; pnl->z[index_z] > z; index_z++);
  * k_size_at_z = pnl->k_size[index_z];

  return _SUCCESS_;
}

int nonlinear_pk_at_k_and_z(
			    struct nonlinear * pnl,
			    double k,
			    double z,
			    double * pk_density,
			    double * pk_velocity,
			    double * pk_cross,
			    int * k_size_at_z
			    ) {
  
  double * pz_density;
  double * pz_velocity;
  double * pz_cross;
  double * ddpz_density;
  double * ddpz_velocity;
  double * ddpz_cross;
  int last_index;

  class_test(pnl->method == nl_none,
	     pnl->error_message,
	     "No non-linear spectra requested. You cannot call the function non_linear_pk_at_z()");

  class_alloc(pz_density,pnl->k_size[0]*sizeof(double),pnl->error_message);
  class_alloc(ddpz_density,pnl->k_size[0]*sizeof(double),pnl->error_message);

  if ((pnl->method >= nl_trg_linear) && (pnl->method <= nl_trg)) {

    class_alloc(pz_velocity,pnl->k_size[0]*sizeof(double),pnl->error_message);
    class_alloc(pz_cross,pnl->k_size[0]*sizeof(double),pnl->error_message);
    class_alloc(ddpz_velocity,pnl->k_size[0]*sizeof(double),pnl->error_message);
    class_alloc(ddpz_cross,pnl->k_size[0]*sizeof(double),pnl->error_message);

  }

  class_call(nonlinear_pk_at_z(pnl,z,pz_density,pz_velocity,pz_cross,k_size_at_z),
	     pnl->error_message,
	     pnl->error_message);

  class_call(array_spline_table_lines(pnl->k,
				      *k_size_at_z,
				      pz_density,
				      1,
				      ddpz_density,
				      _SPLINE_NATURAL_,
				      pnl->error_message),
	     pnl->error_message,
	     pnl->error_message);
      
  class_call(array_interpolate_spline(pnl->k,
				      *k_size_at_z,
				      pz_density,
				      ddpz_density,
				      1,
				      k,
				      &last_index,
				      pk_density,
				      1,
				      pnl->error_message),
	     pnl->error_message,
	     pnl->error_message);

  if ((pnl->method >= nl_trg_linear) && (pnl->method <= nl_trg)) {

    class_call(array_spline_table_lines(pnl->k,
					*k_size_at_z,
					pz_velocity,
					1,
					ddpz_velocity,
					_SPLINE_NATURAL_,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);
    
    class_call(array_interpolate_spline(pnl->k,
					*k_size_at_z,
					pz_velocity,
					ddpz_velocity,
					1,
					k,
					&last_index,
					pk_velocity,
					1,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);

    class_call(array_spline_table_lines(pnl->k,
					*k_size_at_z,
					pz_cross,
					1,
					ddpz_cross,
					_SPLINE_NATURAL_,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);
    
    class_call(array_interpolate_spline(pnl->k,
					*k_size_at_z,
					pz_cross,
					ddpz_cross,
					1,
					k,
					&last_index,
					pk_cross,
					1,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);

    free(pz_velocity);
    free(pz_cross);
    free(ddpz_velocity);
    free(ddpz_cross);
  }

  free(pz_density);
  free(ddpz_density);

  return _SUCCESS_;
}

int nonlinear_init(
		   struct precision *ppr,
		   struct background *pba,
		   struct thermo *pth,
		   struct primordial *ppm,
		   struct spectra *psp,
		   struct nonlinear *pnl
		   ) {

  int index_z,index_k;
  int last_density;
  int last_cross;
  int last_velocity;
  double z;
  double * pk_ic=NULL;  /* array with argument 
		      pk_ic[index_k * psp->ic_ic_size[index_mode] + index_ic1_ic2] */

  double * pk_tot; /* array with argument 
		      pk_tot[index_k] */

  /** (a) if non non-linear corrections requested */

  if (pnl->method == nl_none) {
    if (pnl->nonlinear_verbose > 0)
      printf("No non-linear spectra requested. Nonlinear module skipped.\n");
  }

  /** (b) for HALOFIT non-linear spectrum */

  else if (pnl->method == nl_halofit) {
    if (pnl->nonlinear_verbose > 0)
      printf("Computing non-linear matter power spectrum with Halofit (including update by Bird et al 2011)\n");

    /** - define values of z */

    pnl->z_size = (int)(psp->z_max_pk/ppr->halofit_dz)+1;

    class_alloc(pnl->z,
		pnl->z_size*sizeof(double),
		pnl->error_message);

    if (pnl->z_size == 1) {
      pnl->z[0]=0;
    }
    else {
      for (index_z=0; index_z < pnl->z_size; index_z++) {
	pnl->z[index_z]=(double)(pnl->z_size-1-index_z)/(double)(pnl->z_size-1)*psp->z_max_pk;  /* z stored in decreasing order */
      }
    }

    /** - define values of k */

    class_alloc(pnl->k_size,
		pnl->z_size*sizeof(int),
		pnl->error_message);
    
    for (index_z=0; index_z < pnl->z_size; index_z++) {
      pnl->k_size[index_z] = psp->ln_k_size;
    }

    class_alloc(pnl->k,
		pnl->k_size[0]*sizeof(double),
		pnl->error_message);

    for (index_k=0; index_k < pnl->k_size[0]; index_k++) {
      pnl->k[index_k] = exp(psp->ln_k[index_k]);
    }

    /** - allocate p_density (= pk_nonlinear) and fill it with linear power spectrum */

    class_alloc(pnl->p_density,
		pnl->k_size[0]*pnl->z_size*sizeof(double),
		pnl->error_message);

    class_alloc(pk_tot,
		psp->ln_k_size*sizeof(double),
		pnl->error_message);

    if (psp->ic_size[psp->index_md_scalars] > 1) {

      class_alloc(pk_ic,
		  psp->ln_k_size*psp->ic_ic_size[psp->index_md_scalars]*sizeof(double),
		  pnl->error_message);

    }

    for (index_z=0; index_z < pnl->z_size; index_z++) {

      class_call(spectra_pk_at_z(pba,
				 psp,
				 linear,
				 pnl->z[index_z],
				 pk_tot,
				 pk_ic),
		 psp->error_message,
		 pnl->error_message);

      for (index_k=0; index_k < pnl->k_size[index_z]; index_k++) {
	
	pnl->p_density[index_z*pnl->k_size[index_z]+index_k] = pk_tot[index_k];

      }      
    }

    free(pk_tot);
    free(pk_ic);

    /** - apply non-linear corrections */

    class_call(nonlinear_halofit(ppr,pba,ppm,psp,pnl),
	       pnl->error_message,
	       pnl->error_message);

    /** - take second derivative w.r.t z in view of spline inteprolation */

    class_alloc(pnl->ddp_density,
		pnl->k_size[0]*pnl->z_size*sizeof(double),
		pnl->error_message);

    class_call(array_spline_table_lines(pnl->z,
					pnl->z_size,
					pnl->p_density,
					pnl->k_size[0],
					pnl->ddp_density,
					_SPLINE_EST_DERIV_,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);
    
  }

  /** (c) for TRG non-linear spectrum */

  else if ((pnl->method >= nl_trg_linear) && (pnl->method <= nl_trg)) {
    if (pnl->nonlinear_verbose > 0)
      printf("Computing non-linear matter power spectrum with trg module\n");

    struct spectra_nl trg;

    if (pnl->method == nl_trg_linear)
      trg.mode = 0;
    if (pnl->method == nl_trg_one_loop)
      trg.mode = 1;
    if (pnl->method == nl_trg)
      trg.mode = 2;

    trg.k_max = exp(psp->ln_k[psp->ln_k_size-1]) * pba->h - 1.;

    trg.double_escape = ppr->double_escape;
    trg.z_ini = ppr->z_ini;
    trg.eta_size = ppr->eta_size;
    trg.k_L = ppr->k_L;
    trg.k_min = ppr->k_min;
    trg.logstepx_min = ppr->logstepx_min;
    trg.k_growth_factor = ppr->k_growth_factor;
    trg.ic = pnl->ic;

    trg.spectra_nl_verbose = pnl->nonlinear_verbose;

    class_call(trg_init(ppr,pba,pth,ppm,psp,&trg),
	       trg.error_message,
	       pnl->error_message);

    /* copy non-linear spectrum in pnl */
    
    pnl->z_size = (trg.eta_size-1)/2+1;

    class_calloc(pnl->k_size,
		 pnl->z_size,
		 sizeof(int),
		 pnl->error_message);

    for (index_z=0; index_z < pnl->z_size; index_z++) {
      pnl->k_size[index_z] = trg.k_size-4*trg.double_escape*index_z;
    }

    class_calloc(pnl->k,
		 pnl->k_size[0],
		 sizeof(double),
		 pnl->error_message);

    class_calloc(pnl->z,
		 pnl->z_size,
		 sizeof(double),
		 pnl->error_message);

    class_calloc(pnl->p_density,
		 pnl->k_size[0]*pnl->z_size,
		 sizeof(double),
		 pnl->error_message);
    class_calloc(pnl->p_cross,
		 pnl->k_size[0]*pnl->z_size,
		 sizeof(double),
		 pnl->error_message);
    class_calloc(pnl->p_velocity,
		 pnl->k_size[0]*pnl->z_size,
		 sizeof(double),
		 pnl->error_message);

    class_calloc(pnl->ddp_density,
		 pnl->k_size[0]*pnl->z_size,
		 sizeof(double),
		 pnl->error_message);
    class_calloc(pnl->ddp_cross,
		 pnl->k_size[0]*pnl->z_size,
		 sizeof(double),
		 pnl->error_message);
    class_calloc(pnl->ddp_velocity,
		 pnl->k_size[0]*pnl->z_size,
		 sizeof(double),
		 pnl->error_message);

    for (index_k=0; index_k<pnl->k_size[0]; index_k++) {

      pnl->k[index_k] = trg.k[index_k];

    }

    for (index_z=0; index_z<pnl->z_size; index_z++) {
      
      pnl->z[index_z] = trg.z[2*index_z];

      for (index_k=0; index_k<pnl->k_size[0]; index_k++) {

	pnl->p_density[index_z*pnl->k_size[0]+index_k]=trg.p_11_nl[2*index_z*pnl->k_size[0]+index_k];
	pnl->p_cross[index_z*pnl->k_size[0]+index_k]=trg.p_12_nl[2*index_z*pnl->k_size[0]+index_k];
	pnl->p_velocity[index_z*pnl->k_size[0]+index_k]=trg.p_22_nl[2*index_z*pnl->k_size[0]+index_k];

      }
    }

    /* for non-computed values: instead oif leaving zeros, leave last
       computed value: the result is more smooth and will not fool the
       interpolation routine; but these values are not outputed at the
       end. In order to have an even better intrpolation, would be
       better to extrapolate with a parabola rather than a
       constant. */
 
    for (index_k=0; index_k<pnl->k_size[0]; index_k++) {

      last_density = pnl->p_density[index_k];
      last_cross = pnl->p_cross[index_k];
      last_velocity = pnl->p_velocity[index_k];

      for (index_z=0; index_z<pnl->z_size; index_z++) {

	if (pnl->p_density[index_z*pnl->k_size[0]+index_k] == 0.)
	  pnl->p_density[index_z*pnl->k_size[0]+index_k] = last_density;
	else
	  last_density = pnl->p_density[index_z*pnl->k_size[0]+index_k];

	if (pnl->p_cross[index_z*pnl->k_size[0]+index_k] == 0.)
	  pnl->p_cross[index_z*pnl->k_size[0]+index_k] = last_cross;
	else
	  last_cross = pnl->p_cross[index_z*pnl->k_size[0]+index_k];
	
	if (pnl->p_velocity[index_z*pnl->k_size[0]+index_k] == 0.)
	  pnl->p_velocity[index_z*pnl->k_size[0]+index_k] = last_velocity;
	else
	  last_velocity = pnl->p_velocity[index_z*pnl->k_size[0]+index_k];
      }
    }


    class_call(trg_free(&trg),
	       trg.error_message,
	       pnl->error_message);

    class_call(array_spline_table_lines(pnl->z,
					pnl->z_size,
					pnl->p_density,
					pnl->k_size[0],
					pnl->ddp_density,
					_SPLINE_EST_DERIV_,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);

    class_call(array_spline_table_lines(pnl->z,
					pnl->z_size,
					pnl->p_cross,
					pnl->k_size[0],
					pnl->ddp_cross,
					_SPLINE_EST_DERIV_,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);

    class_call(array_spline_table_lines(pnl->z,
					pnl->z_size,
					pnl->p_velocity,
					pnl->k_size[0],
					pnl->ddp_velocity,
					_SPLINE_EST_DERIV_,
					pnl->error_message),
	       pnl->error_message,
	       pnl->error_message);

  }

  else {
    class_stop(pnl->error_message,
		"Your non-linear method variable is set to %d, out of the range defined in nonlinear.h",pnl->method);
  }
  
  return _SUCCESS_;
}

int nonlinear_free(
		   struct nonlinear *pnl
		   ) {

  if (pnl->method > nl_none) {

    free(pnl->k);
    free(pnl->z);
    free(pnl->p_density);
    free(pnl->ddp_density);

    if ((pnl->method >= nl_trg_linear) && (pnl->method <= nl_trg)) {
      free(pnl->p_cross);
      free(pnl->p_velocity);
      free(pnl->ddp_cross);
      free(pnl->ddp_velocity);
    }
  }

  return _SUCCESS_;

}

int nonlinear_halofit(
		      struct precision *ppr,
		      struct background *pba,
		      struct primordial *ppm,
		      struct spectra *psp,
		      struct nonlinear *pnl
		      ) {

  int index_z;
  int index_k;

  for (index_z=0; index_z < pnl->z_size; index_z++) {
    for (index_k=0; index_k < pnl->k_size[index_z]; index_k++) {
      
      /** formule fantaisiste a remplacer par le vrai HALOFIT !! */
      pnl->p_density[index_z*pnl->k_size[index_z]+index_k] *= (1.+pow(pnl->k[index_k]/0.1,2));
      
    }      
  }
  
  return _SUCCESS_;
}
