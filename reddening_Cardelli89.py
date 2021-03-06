import numpy as np

#source: https://github.com/astropy/SPISEA/
def derive_cardelli(wavelength, Rv):
        """
        Cardelli extinction law. This produces extinction values expected
        for AKs = 1
        """
        x = 1.0 / np.array(wavelength)

        # check for applicability
        if (np.min(x) < 0.3):
            print( 'wavelength is longer than applicable range for Cardelli law')
            return None

        if (np.max(x) > 8.0):
            print( 'wavelength is shorter than applicable range for Cardelli law')
            return None
        
        # Set up some arrays for coefficients that we will need
        a = np.zeros(len(x), dtype=float)
        b = np.zeros(len(x), dtype=float)

        y = x - 1.82

        # Calculate coefficients for long wavelengths (low wavenumber)
        # Wavenumger <= 1.1 (Eq. 2a, 2b)
        idx = np.where(x <= 1.1)[0]
        a[idx] =  0.574 * x[idx] ** 1.61
        b[idx] = -0.527 * x[idx] ** 1.61

        # Calculate coefficients for intermediate wavelengths
        # 1.1 < wavenumber <= 3.3 (Eq. 3a, 3b)
        idx = np.where((x > 1.1) & (x <= 3.3))[0]
        yy = y[idx]
        a[idx] = 1 + (0.17699 * yy) - (0.50447 * yy ** 2) - \
            (0.02427 * yy ** 3) + (0.72085 * yy ** 4) + \
            (0.01979 * yy ** 5) - (0.77530 * yy ** 6) + \
            (0.32999 * yy ** 7)
        b[idx] = (1.41338 * yy) + (2.28305 * yy ** 2) + \
            (1.07233 * yy ** 3) - (5.38434 * yy ** 4) - \
            (0.62251 * yy ** 5) + (5.30260 * yy ** 6) - \
            (2.09002 * yy ** 7)

        # Calculate the long wavelength
        # 3.3 < wavenumber < 5.9 (Eq. 4a, 4b)
        idx = np.where((x > 3.3) & (x < 5.9))[0]
        xx = x[idx]
        a[idx] = 1.752 - (0.316 * xx) - (0.104/((xx - 4.67) ** 2 + 0.341))
        b[idx] = -3.090 + (1.825 * xx) + (1.206/((xx - 4.62) ** 2 + 0.263))

        # Calculate the longest wavelength
        # 5.9 <= wavenumber (Eq. 4a, 4b)
        idx = np.where(x >= 5.9)[0]
        xx = x[idx]
        a[idx] = 1.752 - (0.316 * xx) - (0.104/((xx - 4.67) ** 2 + 0.341)) + \
            (-0.04473 * (xx - 5.9) ** 2) - (0.009779 * (xx - 5.9) ** 3)
        b[idx] = -3.090 + (1.825 * xx) + (1.206/((xx - 4.62) ** 2 + 0.263)) + \
            (0.2130 * (xx - 5.9) ** 2) + (0.1207 * (xx - 5.9) ** 3)

        # A(lam) / A(V), from Eq. 1
        extinction = a + b/Rv

        # Now, want to produce A_lambda / AKs, to match other laws
        k_ind = np.where(abs(x-0.46) == min(abs(x-0.46)))
        Aks_Av = a[k_ind] + b[k_ind]/Rv # Aks / Av
        Av_Aks = 1.0 / Aks_Av # Av / Aks
        
        output = extinction * Av_Aks # (A(lamb) / Av) * (Av / Aks) = (A(lamb) / Aks)

        return output
    
#Setting the wavelengts for the filters: BP, G, RP, J, H and Ks to calculate the A_lambda values
wavelength = ( 0.518258, 0.639021, 0.782508, 1.237560, 1.647602, 2.162075 ) # in micron!
Alambda_Av = ( 1.08337, 0.83627, 0.63439, 0.28665, 0.18082, 0.11675 ) # values provided in the CMD 3.5 output
Alambda = derive_cardelli(wavelength,3.1)
print("")
print("Alambda/A_Ks values from Cardelli+1989:")
print("GAIA [BP, G, RP]:", Alambda[0:3] )
print("2MASS [J, H, Ks:", Alambda[3:6] )
print("")
print("Alambda/A_V values from Cardelli+1989:")
print("GAIA [BP, G, RP]:", Alambda_Av[0:3] )
print("2MASS [J, H, Ks:", Alambda_Av[3:6] )
print("")
print("If Ak=2.5 mag, the A_G is obtained as:")
print("A_lambda = Ak * (A_lambda/Ak) = 2.5 * 7.23344726 = 18.1 mag")
print("")
print("If A_V=1.5 mag, the A_G is obtained as:")
print("A_lambda = A_V * (A_lambda/A_V) = 1.5 * 0.83627 = 1.3 mag")
