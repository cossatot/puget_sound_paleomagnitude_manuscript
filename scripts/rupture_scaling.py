import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def M_from_L(L):
    M = 5.08 + 1.16 * np.log10(L)
    return M


def L_from_M(M):
    L = 10**((M - 5.08) / 1.16)
    return L


def M_from_D(D):
    D = 6.94 + 1.14 * np.log10(D)
    return D
    

def D_from_M(M):
    M = 10**((M - 6.94) / 1.14)
    return M


def D_from_L_(L):
    M = M_from_L(L)
    D = D_from_M(M)
    return D

def D_from_L(L):
    log_D = -1.43 + 0.88 * np.log10(L)
    return 10**log_D


Ls = np.linspace(1, 150)
D_Ls = D_from_L(Ls)
D_Ls_ = D_from_L_(Ls)


eq_ds = pd.read_excel('../../puget_sound_eq_history/data/eq_ages_offsets.xlsx',
                      skiprows=[1],
                      )
eq_ls = pd.read_excel('../../puget_lowland_rupture_lengths.xlsx', index_col=0)

eq_ls['L_mean'] = np.mean((eq_ls.min_length, eq_ls.max_length), axis=0)

eq_ls['d'] = 0.

for eq in eq_ls.index:
    try:
        eq_ls.set_value(eq, 'd', eq_ds[eq_ds.time_pdf_name == eq].vert_sep)

    except ValueError:
        print(eq)
        pass

plt.errorbar(eq_ls['L_mean'], eq_ls['d'], 
             xerr=(eq_ls.max_length - eq_ls.L_mean).values,
             fmt='o',
             )

plt.plot(Ls, D_Ls, label='wc')
plt.plot(Ls, D_Ls_, label='eq_prop')
plt.xlabel('Length')
plt.ylabel('Displacement')
plt.legend(loc='best')
plt.show()
