# -*- coding: utf-8 -*-
# importing the required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import r2_score

# loading the required columns from csv file to c_df dataframe
c_df = pd.read_csv('./report_3.csv', sep=';', usecols=['calldate', 'clid', 'src', 'dst', 'dcontext',
                                                                 'channel', 'dstchannel', 'lastdata', 'billsec',
                                                                 'disposition'])
# converting 'src' column type to str
c_df['src'] = c_df['src'].astype(str)
# deleting some of incoming calls by the context name
c_df = c_df[(c_df.dcontext != 'incoming_ttk') & 
            (c_df.dcontext != 'enter_ext') & 
            (c_df.dcontext != 'ivr-ic') & 
            (c_df.dcontext != 'ivr-med') & 
            (c_df.dcontext != 'support') & 
            # deleting all unaswered and failed calls
            (c_df.disposition == 'ANSWERED') &
            # deleting all calls which duration less than or equal 0
            (c_df.billsec > 0)
            ]

# all calls to number starting with '8' we are adding to mob_mord object
# so we get all calls to mobile and to other cities
# -mob_mord = (c_df['dst'].str.startswith('892718')) |
# (c_df['dst'].str.startswith('896033')) |
# (c_df['dst'].str.startswith('98769')) |
# (c_df['dst'].str.startswith('7917075'))
mob_mord = (c_df['dst'].str.startswith('8'))
# converting mob_mord object to cmob_df dataframe
cmob_df = c_df.loc[mob_mord]
# adding new column 'rub' to dataframe, converting seconds to minutes and multiply on cost of minute
cmob_df['rub'] = (cmob_df['billsec']//60+1)*2
# groupping by caller id and summing by rub column
cmob_gr = cmob_df.groupby(['clid'], as_index=False)['rub'].sum()
# sorting by rub column
cmob_grs = cmob_gr.sort_values(['rub'])
# -print(cmob_grs)

# all calls to number with lenght less than 6 we are adding to gor_sar object
# so we get all local calls
gor_sar = (c_df['dst'].str.len() == 6)
# converting gor_sar object to cgor_df dataframe
cgor_df = c_df.loc[gor_sar]
# adding new column 'rub' to dataframe, converting seconds to minutes and multiplie on cost of minute
cgor_df['rub'] = (cgor_df['billsec']//60+1)*0.4
# groupping by caller id and summing by rub column
cgor_gr = cgor_df.groupby(['clid'], as_index=False).sum()
# sorting by rub column
cgor_grs = cgor_gr.sort_values(['rub'])
# -print(cgor_grs)

print()
print(cgor_gr.rub.sum())
# -print(cmob_gr.rub.sum())


# r1 - вектор затрат в рублях на абонента
r1 = cmob_gr.rub.values
# переопределяем вектор r1 так, чтобы i-е значение содержало затраты в рублях на всех абонентов от 0-го до i-го
# значение r1[-1] будет равно сумме затрат на всех абонентов
for i in range(1, len(r1)):
    r1[i] = r1[i] + r1[i-1]
u1 = list(range(1, len(r1)+1))

ud = len(r1) // 5
r2 = r1[0:-ud]
u2 = list(range(1, len(r2)+1))

u3 = list(range(1, len(r1)+1+5*ud))


slope, intercept, r_value, p_value, std_err = stats.linregress(u2, r2)
pr1 = []
for i in range(len(u3)):
    pr1.append(intercept + slope*u3[i])
print(r_value ** 2)


p4 = np.poly1d(np.polyfit(u2, r2, 4))
p4r1 = p4(u3)
r2 = r2_score(r1, p4(r1))
print(r2)


plt.clf()
plt.plot(u1, r1, 'o', label='original data')
plt.plot(u3, pr1, 'r', label='fitted line')
plt.plot(u3, p4r1, 'g', label='polyfit')

plt.legend(loc='upper left')
plt.savefig('./r1.png')
