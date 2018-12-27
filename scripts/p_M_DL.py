#!/usr/bin/env python

from collections import OrderedDict
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys; sys.path.append('/Users/itchy/research/culpable/')
import culpable as cp
from culpable.stats import Pdf

import seaborn as sns
#sns.set_palette('dark')


save_results = True


np.random.seed(69)

n_iters = 1000  # number of monte carlo iterations

# load earthquake data

with open('../gis/puget_lowland_ruptures.geojson', 'r') as f:
    r = json.load(f)

rs = r['features']

eq_names = sorted(list(set(rr['properties']['event'] for rr in rs)))

eq_df = pd.DataFrame(index=eq_names, 
                     columns=['fault', 'offset', 'offset_err',
                              'vert_sep', 'vert_sep_err', 'dip', 'dip_err',
                              'rake', 'rake_err', 'min_length', 'max_length'])

def ruptures_to_row(row, ruptures=rs):
    r_name = row.name

    vals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    cols = ['fault', 'offset', 'offset_err', 'vert_sep', 'vert_sep_err', 'dip',
            'dip_err', 'rake', 'rake_err', 'length']

    for rr in ruptures:
        if rr['properties']['rupture_name'] == r_name + '_min':

            for i, col in enumerate(cols[:-1]):
                try:
                    vals[i] = rr['properties'][col]
                except KeyError:
                    vals[i] = np.nan

            vals[9] = rr['properties']['length']

        elif rr['properties']['rupture_name'] == r_name + '_max':
            vals[10] = rr['properties']['length']

    return vals


for i, eq in enumerate(eq_names):
    eq_df.iloc[i] = ruptures_to_row(eq_df.iloc[i])


# Process earthquake data to Pandas DataFrame

def row_to_om(row):

    if pd.isnull(row['offset']):
        m_off = row['vert_sep']
        m_off_err = row['vert_sep_err']
        m_comp = 'vert_separation'
    else:
        m_off = row['offset']                      
        m_off_err = row['offset_err']
        m_comp = 'offset'

    om = cp.OffsetMarker(name=str(row.name),
                         measured_offset=m_off,
                         measured_offset_err=m_off_err,
                         measured_offset_component=m_comp,
                         measured_offset_dist_type='uniform',
                         dip=row['dip'],
                         dip_err=row['dip_err'],
                         dip_dist_type='uniform',
                         rake=row['rake'],
                         rake_err=row['rake_err'],
                         rake_dist_type='uniform')
    om.init()
    return om

eq_list = [row_to_om(row) for i, row in eq_df.iterrows()]

len_d = {}

for i, row in eq_df.iterrows():
    len_d[row.name] = np.random.uniform(row['min_length'],
                                        row['max_length'], n_iters)


# set magnitude prior p(M)
M_min = 5.5
M_max = 8.5
M_step = 0.01

Ms = np.arange(M_min, M_max+M_step, M_step)
p_M = cp.magnitudes.make_p_M(p_M_type='uniform',
                             #p_M_type='GR_surface_break', 
                             p_M_min=M_min, p_M_max=M_max, M_step=M_step)

# do inversion
p_M_D_dict = OrderedDict()
p_M_DL_dict = OrderedDict()

for eq in eq_list:
    offs = eq.sample_offsets(n_iters)
    p_M_DL_dict[eq.name] = cp.magnitudes.p_M_DL(offs, len_d[eq.name], p_M)
    p_M_D_dict[eq.name] = cp.magnitudes.p_M_D(offs, p_M)


# plotting
f0, (ax00, ax01) = plt.subplots(2, sharex=True, figsize=(7,3.5))

f1, ax1 = plt.subplots(1, figsize=(4,4))
ax1.plot([6.0, M_max],[6.0, M_max], 'k--', lw=0.5)
plt.axis('equal')

df_cols = ['pmd_mean', 'pmd_med', 'pmd_25', 'pmd_75',
           'pmdl_mean', 'pmdl_med', 'pmdl_25', 'pmdl_75']

res_df = pd.DataFrame(data=np.zeros((len(eq_list), 8)),
                      index=[eq.name for eq in eq_list],
                      columns=df_cols)

for i, (eq, pmdl) in enumerate(p_M_DL_dict.items()):
    pmd = list(p_M_D_dict.items())[i][1] 

    ax00.plot(pmd.x, pmd.y, lw=0.75)
    ax01.plot(pmdl.x, pmdl.y, lw=0.75)

    # scatter plot
    p25d = pmd.x[np.argmin(np.abs(np.cumsum(pmd.y / np.sum(pmd.y))-0.25))]
    p50d = pmd.x[np.argmin(np.abs(np.cumsum(pmd.y / np.sum(pmd.y))-0.50))]
    p75d = pmd.x[np.argmin(np.abs(np.cumsum(pmd.y / np.sum(pmd.y))-0.75))]
    
    p25dl = pmdl.x[np.argmin(np.abs(np.cumsum(pmdl.y / np.sum(pmdl.y))-0.25))]
    p50dl = pmdl.x[np.argmin(np.abs(np.cumsum(pmdl.y / np.sum(pmdl.y))-0.50))]
    p75dl = pmdl.x[np.argmin(np.abs(np.cumsum(pmdl.y / np.sum(pmdl.y))-0.75))]
    
    y_err = np.array([[p50dl-p25dl, p75dl-p50dl]]).T
    x_err = np.array([[p50d-p25d, p75d-p50d]]).T

    ax1.errorbar(p50d, p50dl, 
                 xerr=x_err,
                 yerr=y_err,
                 lw=0.75,
                 fmt='.',
                 )

    # saving quantiles for analysis
    res_df.loc[eq] = (cp.stats.pdf_mean(pmd.x, pmd.y),
                      p50d, p25d, p75d,
                      cp.stats.pdf_mean(pmdl.x, pmdl.y),
                      p50dl, p25dl, p75dl)


ax00.set_xlim([M_min, M_max])
ax1.set_xlim([M_min, M_max])

ax01.set_ylim([0,5.5])

ax01.set_xlabel('Magnitude M')
ax00.set_ylabel('Probability p(M|D)')
ax01.set_ylabel('Probability p(M|D,L)')
ax00.text(5.51, 1.45, 'a', fontsize=12, weight='bold')
ax01.text(5.51, 5.50, 'b', fontsize=12, weight='bold')


ax1.set_xlabel('p(M|D)')
ax1.set_ylabel('p(M|D,L)')

f1.tight_layout()
f0.tight_layout(h_pad=0)
#f0.subplots_adjust(hspace=0)

if save_results:
    f0.savefig('../figures/posterior_pdfs.pdf')
    f1.savefig('../figures/posterior_scatter.pdf')

# Save results to DF
eq_df['M_mean'] = res_df.pmdl_mean.values
eq_df = eq_df.sort_values('M_mean', ascending=False)
eq_df['eq_name'] = list(eq_df.index)

if save_results:
    eq_df.to_csv('../results/eq_table.csv', index=False)




# Slip vs. length scaling
def D_from_L_w08(L):
    return 0.06 * L

def D_from_L_wc94(L):
    return np.float_(10**(- 1.43 + 0.88 * np.log10(L)))

f2, ax2 = plt.subplots(1, figsize=(4,4))

ll = np.array([0.01, 200.])

off_mean = [np.abs(eq.sample_offsets(n_iters).mean()) for eq in eq_list]
off_err = [off_mean[i] - np.abs(eq.sample_offsets(n_iters).min()) 
           for i, eq in enumerate(eq_list)]

l_mean = eq_df[['min_length', 'max_length']].mean(axis=1)
l_err = l_mean - eq_df.min_length


for i in range(len(eq_list)):
    ax2.errorbar(l_mean.iloc[i], off_mean[i], 
                 yerr=off_err[i], xerr=l_err.iloc[i],
                 lw=0.5, fmt='.')

ax2.plot(ll, D_from_L_wc94(ll), 'k:', lw=0.5, label='WC94')
ax2.plot(ll, D_from_L_w08(ll), 'k--', lw=0.5, label='W08')
plt.xlabel('Rupture Length (km)')
plt.ylabel('Rupture Offset (m)')
plt.legend(loc='lower right')
f2.subplots_adjust(bottom=0.12)

if save_results:
    f2.savefig('../figures/l_d_scaling.pdf')


# Magnitude PDFs for each earthquake
sns.set_style("whitegrid")
sns.despine()
f3, axs = plt.subplots(len(eq_list)+1, figsize=(6,10), sharex=True)

axs[0].axis('off')
axs[0].annotate('Earthquake Name', xy=(1.02, 0.4), 
                xycoords='axes fraction',
                fontweight='bold',
                )

axs[0].annotate('p(M|D)', xy=(0.4, 0.4), 
                xycoords='axes fraction',
                fontweight='bold',
                )

M_sort = np.argsort(eq_df.M_mean.values)

for i, (eq, pmdl) in enumerate(p_M_DL_dict.items()):

    pmd = list(p_M_D_dict.items())[i][1]

    axs_i = eq_df.index[M_sort][::-1].tolist().index(eq) +1

    #i += 1
    axs[axs_i].plot(pmdl.x, pmdl.y)
    axs[axs_i].plot(pmd.x, pmd.y, lw=1.5, linestyle='--')

    axs[axs_i].set_yticks([])

    axs[axs_i].annotate(eq, xy=(1.02, 0.4), xycoords='axes fraction')

axs[-1].set_xlabel('Moment Magnitude')

f3.subplots_adjust(hspace=0, left=0.02, right=0.6, top=0.98, bottom=0.05)

if save_results:
    f3.savefig('../figures/post_magnitude_stack.pdf')


# results to json
res_dict = {}
for i, (eq, pmdl) in enumerate(p_M_DL_dict.items()):
    
    pmd = list(p_M_D_dict.items())[i][1]
    
    res_dict[eq] = {'M': pmdl.x.tolist(),
                    'p_M_D': pmd.y.tolist(),
                    'p_M_DL': pmdl.y.tolist()}

if save_results:
    with open('../results/magnitude_posteriors.json', 'w') as f:
        json.dump(res_dict, f)


plt.show()
