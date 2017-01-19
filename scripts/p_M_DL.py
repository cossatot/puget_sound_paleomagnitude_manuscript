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

np.random.seed(69)

n_iters = 1000  # number of monte carlo iterations

# load earthquake data

# rupture offsets and fault geometry
eq_df = pd.read_excel('../data/eq_ages_offsets.xlsx', skiprows=[1])


def row_to_om(row):

    if pd.isnull(row['offset']):
        m_off = row['vert_sep']
        m_off_err = row['vert_sep_err']
        m_comp = 'vert_separation'
    else:
        m_off = row['offset']                      
        m_off_err = row['offset_err']
        m_comp = 'offset'

    om = cp.OffsetMarker(name=str(row['time_pdf_name']),
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

# load rupture length spreadsheet
len_df = pd.read_excel('../data/puget_lowland_rupture_lengths.xlsx')

len_d = {}

for i, row in len_df.iterrows():
    len_d[row['earthquake']] = np.random.uniform(row['min_length'],
                                                 row['max_length'], n_iters)

# set magnitude prior p(M)
M_min = 5.5
M_max = 8.5
M_step = 0.01

Ms = np.arange(M_min, M_max+M_step, M_step)
p_M = Pdf(Ms, np.ones(len(Ms)))

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
ax1.set_xlim([6.0, M_max])

ax01.set_ylim([0,6])

ax01.set_xlabel('Magnitude M')
ax00.set_ylabel('p(M|D)')
ax01.set_ylabel('p(M|D,L)')
ax00.text(5.51, 1.45, 'a', fontsize=12, weight='bold')
ax01.text(5.51, 5.50, 'b', fontsize=12, weight='bold')


ax1.set_xlabel('p(M|D)')
ax1.set_ylabel('p(M|D,L)')

f1.tight_layout()
f0.tight_layout(h_pad=0)
#f0.subplots_adjust(hspace=0)


f0.savefig('../figures/posterior_pdfs.pdf')
f1.savefig('../figures/posterior_scatter.pdf')

# Save results to DF for saving, making table in R

eqdf = eq_df[['fault', 'site_name', 'age_MidPt', 'scarp_hgt', 'vert_sep',
              'vert_sep_err', 'offset', 'offset_err', 'dip', 'dip_err',
              'strike', 'strike_err', 'rake', 'rake_err', 'time_pdf_name']]

eqdf['M_mean'] = res_df.pmdl_mean.values
eqdf.to_csv('../results/eq_table.csv', index=False)

# subsampled results for saving and plotting to table


sns.set_style("whitegrid")
sns.despine()
f2, axs = plt.subplots(len(eq_list)+1, figsize=(6,10), sharex=True)

axs[0].axis('off')
axs[0].annotate('Earthquake Name', xy=(1.02, 0.4), 
                xycoords='axes fraction',
                fontweight='bold',
                )

axs[0].annotate('p(M|D)', xy=(0.4, 0.4), 
                xycoords='axes fraction',
                fontweight='bold',
                )

for i, (eq, pmdl) in enumerate(p_M_DL_dict.items()):

    pmd = list(p_M_D_dict.items())[i][1] 

    i += 1
    axs[i].plot(pmdl.x, pmdl.y)
    axs[i].plot(pmd.x, pmd.y, lw=1., linestyle='--')

    axs[i].set_yticks([])

    axs[i].annotate(eq, xy=(1.02, 0.4), xycoords='axes fraction')

axs[-1].set_xlabel('Moment Magnitude')

f2.subplots_adjust(hspace=0, left=0.02, right=0.6, top=0.98, bottom=0.05)

f2.savefig('../figures/post_magnitude_stack.pdf')

plt.show()
