import numpy as np
import matplotlib.pyplot as plt
import csv

with open('D:\ML\Calls\report3.csv') as f:
    reader = csv.reader(f, delimiter=';')
    cdt=[]
    ccid=[]
    cfrom=[]
    cto=[]
    cdur=[]
    for row in reader:
        cdt.append(row[0])
        ccid.append(row[1])
        cfrom.append(row[2])
        cto.append(row[3])
        cdur.append(row[4])

d_arr=np.array(cdur, dtype=int)
d_mean=np.mean(d_arr)
d_med=np.median(d_arr)
d_std=np.std(d_arr)
d_var=np.var(d_arr)
d_pr90=np.percentile(d_arr, 90)
d_pr95=np.percentile(d_arr, 95)
d_pr99=np.percentile(d_arr, 99)


sd_arr=np.sort(d_arr)
lda=len(sd_arr)

print('              Mean: ', d_mean)
print('            Median: ', d_med)
print('Standard deviation: ', d_std)
print('          Variance: ', d_var)
print()
print('     90-percentile: ', d_pr90, ' (', int(0.9*lda), ' calls)')
print('     95-percentile: ', d_pr95, ' (', int(0.95*lda), ' calls)')
print('     99-percentile: ', d_pr99, ' (', int(0.99*lda), ' calls)')


z=[]
for i in range(len(cfrom)):
    if d_arr[i] > d_pr90:#d_mean:
        if int(cto[i])>999999:
            z.append(int(cfrom[i]))

zc = np.array([[x,z.count(x)] for x in set(z)])
print(zc[np.argsort(zc[:, 1])])
#s = np.random.normal(d_mean, d_std, 2000)

#calls = np.sort(calls.view('i8,i8,i8'), order=['f1'], axis=0).view(np.int)
#print(calls)
#print()
#call_ext = calls[db_arr>600,:]
#call_dur_arr=calls[:,2]
#dbmn = np.mean(db_arr)
#d_mean_arr = [d_mean for i in d_arr]
#dbmd=np.median(db_arr)
#d_med_arr = [d_med for i in d_arr]
#call_data2 = call_data[db_arr>600,:]
#db_arr2=call_data2[:,4]

i_mean=np.where(sd_arr > d_mean)[0][0]

#plt.hist(d_arr>106,50)
#plt.plot(d_arr)
plt.plot(sd_arr)
plt.plot((0,lda), (d_mean, d_mean))
plt.plot((i_mean,i_mean), (0, np.max(sd_arr)))
#plt.plot(d_mean_arr)
#plt.plot(d_med_arr)
plt.savefig('bill.png')

#for i in range(np.shape(call_data)[0]):
#    if db_arr[i]>600:
#        print(str(int(call_data[i,1])) + '-->' + str(int(call_data[i,2])))
