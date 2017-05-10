#print(c_df.dtypes)
#print(calls_df)
#print(calls_df[calls_df.src<9999][calls_df.dst>999999].groupby(['clid'])['calldate'].count().sort_values())
#calls_dur_df = calls_df[calls_df.src<9999][calls_df.dst>999999].groupby(['clid'])['billsec'].sum().sort_values()
#calls_dur_df['rub'] = calls_dur_df[1] / 60 * 1.5
#print(calls_dur_df)
#cd_df = calls_df[calls_df.src<9999]
#cd_df = cd_df[cd_df.dst>999999]
#cd_df = calls_df[calls_df.dst>999999]
#cd_df['rub'] = cd_df['billsec']/60*1.5*1.18
#cd2_df = cd_df.groupby(['clid'])['rub'].sum().sort_values()
#cd2_df = cd2_df.to_frame()
#print(cd2_df['rub'].sum())

def predict(x):
    return slope * x + intercept

fitline = predict(u1)
print(len(fitline))














ud = 40

r1 = cmob_gr.rub.values
for i in range(1,len(r1)):
    r1[i]=r1[i]+r1[i-1]
u1 = list(range(1,len(r1)+1))
u2 = list(range(1,len(u1)+ud))



slope, intercept, r_value, p_value, std_err = stats.linregress(u1, r1)
pr1=[]
for i in range(len(u2)):
    pr1.append(intercept + slope*u2[i])
print(r_value ** 2)
print((pr1[-1]-r1[-1])+300*1.18*ud)




p4 = np.poly1d(np.polyfit(u1, r1, 4))
p4r1 = p4(u2)
r2 = r2_score(r1,p4(r1))
print(r2)




plt.clf()
plt.plot(u1, r1, 'o', label='original data')
plt.plot(u2, pr1, 'r', label='fitted line')

plt.plot(u2, p4r1, 'g', label='polyfit')

plt.legend(loc='upper left')
plt.savefig('D:/ML/Calls/r1.png')

