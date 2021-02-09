"""
This program evolves the following coupled ODEs with dichotomous noise, using predictor-corrector method:
dx1/dt = ...
dx2/dt = ...
@author:	Shailendra K Rathor
			Department of Physics,
			Indian Institute of Technology, Kanpur (India)
@Note: If you find it useful please do use, modify or distribute it.
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
#~ from statsmodels.tsa import stattools

def generate_DN(state1, state2, tau, stepsize, boxsize = 1):
	a = float(state1)		# state_1
	b = float(state2)		# state_2
	mu_a = a/(a-b) * (1/tau)
	mu_b = (-1.0)* b * mu_a / a
	#~ print(mu_a, mu_b)
	#~ tau = 1/(mu_a + mu_b)
# 	print("tau = ", tau)
# 	Q = (-1) * a * b * tau
# 	print("Q = ", Q)
	#~ numerator = 10**(np.floor(np.log10(tau)))
	#~ dt = numerator/100.0
	dt = stepsize
# 	print("dt = ", dt)
	x0 = a
	X = [x0]		# Sequence generated by random variable eta(t)
	length = int(float(boxsize)/stepsize) 
	for _ in range(length):
		if(X[-1] == x0):
			P_aa = tau*mu_b + tau*mu_a*np.exp(-dt/tau)
			R = np.random.uniform(0.0,1.0,size=1)
			if(R < P_aa):
				x1 = a
				X.append(x1)
			else:
				x1 = b
				X.append(x1)
		else:		
			P_ab = tau*mu_b - tau*mu_b*np.exp(-dt/tau)
			R = np.random.uniform(0.0,1.0,size=1)
			if(R < P_ab):
				x1 = a
				X.append(x1)
			else:
				x1 = b
				X.append(x1)
		
	X = np.array(X)
	T = dt*np.arange(len(X))

	return (T,X)

def statistics_of_DN():
	T, X = generate_DN()
	
			#~ m = np.mean(X) 
		#~ print(j,m)
		#~ # ===========
		#~ xp = X-m
		#~ f = np.fft.fft(xp)
		#~ p = np.array([np.real(v)**2+np.imag(v)**2 for v in f])
		#~ pi = np.fft.ifft(p)
		#~ C = np.real(pi)[:X.size/2]/np.sum(xp**2)
		#~ T = np.arange(len(C))
		#~ plt.plot(T[:1000]*dt,C[:1000])
		#~ z = np.polyfit(T[:100],np.log(C[:100]),1)
		#~ lamda += z[0]
		#~ print(tau, -z[0]**(-1)*dt)
		
		# x = 1-D array
		# Yield normalized autocorrelation function of number lags
		#~ autocorr = stattools.acf( X,nlags=200)

		# Get autocorrelation coefficient at lag = 1
		#~ autocorr_coeff = autocorr[1]
		#~ T = np.arange(len(autocorr))/100.0
		#~ plt.plot(T, autocorr,'g--o')
		#~ z = np.polyfit(T[:], np.log(autocorr[:]), 1, cov=False)
		#~ lamda += z[0]
		#~ print(tau, -z[0]**(-1))
		#============
		#~ plt.acorr(X, maxlags = 50)
		#~ plt.show()  
		#~ mean += m 
	#~ print(mean/sample_paths)
	#~ print("avg tau: ",(-dt * sample_paths)/lamda)
	#~ plt.show()
	
	#~ T = dt*np.arange(len(X))
	plt.plot(T,X)
	#~ plt.ylim(b-1, a+1)
	#~ plt.title(r"$\tau = $" + str(tau))
	#~ plt.xlabel(r"$t$")
	#~ plt.ylabel(r"$\xi(t)$")
	#~ plt.tight_layout()
	# plt.savefig("sample_dn_2.pdf")
	plt.show()
	return 0

def autocorrelation (x) :
    """
    Compute the autocorrelation of the signal, based on the properties of the
    power spectral density of the signal.
    """
    xp = x-np.mean(x)
    f = np.fft.fft(xp)
    p = np.array([np.real(v)**2+np.imag(v)**2 for v in f])
    pi = np.fft.ifft(p)
    return np.real(pi)[:x.size/2]/np.sum(xp**2)	

def rhs(t, x, y, stiffness = 2, xi = 0, epsilon = 1, Amp = 1, freq = 2*np.pi):
	return epsilon * y + Amp*np.sin(freq * t) - (stiffness + xi) * x 
	
def predictor_corrector(t0,x0,y0, dt, stiffness = 2, xi = 0, epsilon = 1, Amp = 1, freq = 2*np.pi):
	f0 = epsilon * y0 + Amp*np.sin(freq * t0) - (stiffness + xi) * x0  #rhs(t0, x0, y0)
	predicted_x1 = x0 + dt * f0
	t1 = t0+dt
	#~ f1 = rhs(t1, predicted_x1, y0)
	#~ predicted_x1 = x0 + 0.5*dt*(f0 + f1)
	f1 = epsilon * y0 + Amp*np.sin(freq * t1) - (stiffness + xi) * predicted_x1  #rhs(t1, predicted_x1, y0)
	corrected_x1 = x0 + 0.5*dt*(f0 + f1)
	return corrected_x1

def V_effective(x1, x2, t, stiffness = 2, xi_1 = 0, xi_2 = 0, Amp = 1, freq = 2*np.pi, epsilon = 1):
	V1 = 0.5*(stiffness + xi_1)*x1**2 + x1*Amp*np.sin(freq * t) 	
	V2 = 0.5*(stiffness + xi_2)*x2**2 + x2*Amp*np.sin(freq * t) 	
	Vint = (-1)*epsilon * x1 * x2
	return V1 + V2 + Vint

def evolution():
	""" This evolves the equations with noise.
	Parameter
	---------
	
	Returns
	------
		
	"""
	attempt = input("Attempt number for evolution: ", ) # Return a string
	f = open("run_history-"+str(attempt)+".txt", "a")
	now = datetime.datetime.now().strftime("%H:%M:%S, %d/%m/%Y")
	f.writelines(["\nRun attempt: ", str(attempt), "\n"])
	f.writelines(["Start time: ", str(now), "\n"])

	# ==== Input for noise generation ==================================
	T = 100.0										# Domain size
	f.writelines(["\t Domain size: ", str(T), "\n"])
	sigma_1 = 2.5										# state 1
	f.writelines(["\t State 1: ", str(sigma_1), "\n"])
	sigma_2 = 0.8 * sigma_1							# state 2
	f.writelines(["\t State 2: ", str(sigma_2), "\n"])
	tau_1 = 2.5										# typical time of autocorrelation for x_1
	f.writelines(["\t tau_1: ", str(tau_1), "\n"])
	tau_2 = 2.5										# typical time of autocorrelation for x_2
	f.writelines(["\t tau_2: ", str(tau_2), "\n"])
	tau = np.min([tau_1, tau_2])
	numerator = 10**(np.floor(np.log10(tau))) 		# order of tau
	dt = numerator/100.0							# time step s.t. dt << tau
	f.writelines(["\t stepsize: ", str(dt), "\n"])
	
	# ==== Input for the set of equations ==============================
	#~ dt = 0.01									# stepsize
	N = int(T/dt)									# Number of steps
	eps = 1										# coupling strength
	f.writelines(["\t epsilon: ", str(eps), "\n"])
	a = 3.0											# Stiffness
	f.writelines(["\t stiffness: ", str(a), "\n"])
	A = 0.5											# Forcing amplitude
	f.writelines(["\t amplitude: ", str(A), "\n"])
	omega = 0.4										# Forcing frequency
	f.writelines(["\t frequency: ", str(omega), "\n"])
	f.close()
    # =========== Loop for ensemble averaging ==========================
	X_total = 0
	Y_total = 0
	ensemble_size = 1000
	for ic in range(ensemble_size):
		print(ic)
		t0 = 0											# initial time
		x0 = 0											# initial condition on x_1
		y0 = 0											# initial condition on x_2
		X = [x0]										# Sequence of x_1 to evolve
		Y = [y0]										# Sequence of x_2 to evolve
		Veff = []
		v = V_effective(x0, y0, t0, stiffness = a, xi_1 = 0, xi_2 = 0, Amp = A, freq = omega, epsilon = eps)
		Veff.append(v)
		_, xi_1 = generate_DN(sigma_1,-sigma_1, tau_1, dt, boxsize=T) 	# generate noise for x_1
		_, xi_2 = generate_DN(sigma_2,-sigma_2, tau_2, dt, boxsize=T) 	# generate noise for x_2
		# =========== Loop for evolution ===================================
		for i in range(1,N+1):
			t0 = i*dt
			x = predictor_corrector(t0, x0, y0, dt, stiffness = a, xi = xi_1[i], epsilon = eps, Amp = A, freq = omega)
			y = predictor_corrector(t0, y0, x0, dt, stiffness = a, xi = xi_2[i], epsilon = eps, Amp = A, freq = omega)
			#~ x = predictor_corrector(t0, x0, y0, dt,a = 2, xi = 0, epsilon = 1, A = 1, omega = 2*np.pi)
			#~ y = predictor_corrector(t0, y0, x0, dt,a = 2, xi = 0, epsilon = 1, A = 1, omega = 2*np.pi)
			x0 = x
			y0 = y
			X.append(x)
			Y.append(y)
			#~ v = V_effective(x0, y0, t0, stiffness = a, xi_1 = xi_1[i], xi_2 = xi_2[i], Amp = A, freq = omega, epsilon = eps)
			#~ Veff.append(v)
			#~ print(i)
		#~ print(X)
	
		X_total += np.array(X)
		Y_total += np.array(Y)
		#~ Veff = np.array(Veff)
	X_mean = X_total / ensemble_size
	Y_mean = Y_total / ensemble_size
	t = dt * np.arange(N+1)
	np.savetxt("data/xy_t-"+str(attempt)+".txt", np.column_stack((t, X_mean, Y_mean)))
	
	now = datetime.datetime.now().strftime("%H:%M:%S, %d/%m/%Y")
	
	f = open("run_history-"+str(attempt)+".txt", "a")
	f.writelines(["End time: ", str(now), "\n"])
	f.writelines(["\n-----------------------------\n"])
	f.close()
	# ============== Plotting ==========================================
	#~ plt.plot(t, X_mean, label=r"$x_1$")
	#~ plt.plot(t, Y_mean, label=r"$x_2$")
	#~ plt.plot(t, Veff,'--o', label=r"$x$")
	#~ plt.plot(t, Veff, label=r"$y$")
	#~ plt.xlabel(r"$t$")
	#~ plt.ylabel(r"$x_1, x_2$")
	#~ plt.legend(loc="best")
	#~ plt.tight_layout()
	#~ plt.show()
	return 0
	
def plotting():
	attempt = input("Attempt number for plotting: ", ) # Return a string
	data = np.loadtxt("data/xy_t-"+str(attempt)+".txt")
	t = data[:,0]
	X = data[:,1]
	Y = data[:,2]
	# ============== Plotting ==========================================
	plt.plot(t, X, label=r"$x_1$")
	plt.plot(t, Y, label=r"$x_2$")
	#~ plt.plot(t, Veff,'--o', label=r"$x$")
	#~ plt.plot(t, Veff, label=r"$y$")
	plt.xlabel(r"$t$")
	plt.ylabel(r"$x_1, x_2$")
	plt.legend(loc="best")
	plt.tight_layout()
	plt.show()

if __name__ == '__main__':
	#~ generate_DN()
	#~ statistics_of_DN()
	#~ evolution()
	plotting()
	print ("Check if any function is selected otherwise it is Successful !")
