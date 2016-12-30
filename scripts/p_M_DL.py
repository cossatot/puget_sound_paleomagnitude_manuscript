import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys; sys.path.append('/Users/itchy/research/culpable/')
import culpable as cp
from culpable.stats import Pdf

np.random.seed(69)

n_iters = 1000 # number of monte carlo iterations

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
len_df = pd.read_excel('../../puget_lowland_rupture_lengths.xlsx')

len_d = {}

for i, row in len_df.iterrows():
    len_d[row['earthquake']] = np.random.uniform(row['min_length'],
                                                 row['max_length'], n_iters)

# set magnitude prior p(M)
M_min = 5.5
M_max = 8.5
M_step = 0.05

Ms = np.arange(M_min, M_max+M_step, M_step)

p_M = Pdf(Ms, np.ones(len(Ms)))

# do inversion

p_M_DL_dict = {}

for eq in eq_list:
    try:
        p_M_DL_dict[eq.name] = cp.magnitudes.p_M_DL(eq.sample_offsets(n_iters),
                                                    len_d[eq.name],
                                                    p_M)
    except:
        print(eq.name)


plt.figure()

tot_px = np.zeros(1000)

for eq, pm in p_M_DL_dict.items():
    plt.plot(pm.x, pm.y)

    tot_px += pm.y

#plt.plot(pm.x, tot_px)

plt.xlim([M_min, M_max])

plt.show()
