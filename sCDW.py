import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

# Formats a numpy datatype for a given file. If the file, or one like it, has not been seen before, it inquires
# the user for details about the format.
def get_dt(fname):
    if (os.path.isfile("chart.p")):
        chart = pickle.load(open("chart.p", "rb"))
    else:
        chart = dict()

    header = ""
    with open(fname) as f:
        for line in f:
            header = line
            break

    if header in chart:
        return chart[header]

    else:
        hlist = header.split("\t")
        hlist[-1] = hlist[-1][0:-1]

        print("This file is in a format that has not been seen before.")

        datatp = [('time1', '|S10'), ('time2', '|S10')]
        for hl in hlist[1:]:
            datatp.append((input(hl + "?\t"), '<f8'))
        dt = np.dtype(datatp)

        chart[header] = dt
        pickle.dump(chart, open("chart.p", "wb"))
        return dt

# Gets data, uses the get_dt interface to prepare data type
def get_data(fname):
    return np.genfromtxt(fname, skip_header = True, dtype = get_dt(fname))

# Houses relevant information about a sample: data folder path, sample dimensions (in microns), and
# lockin voltage setup (assumes right-angle geometry).
class sample:
    def __init__(self, name = "", path = "", ax = 100, ay = 10, bx = 100, by = 10, z = 1, a = "A", c = "B"):
        self.name = name
        self.path = "C:\\Users\\Scott Reid\\Documents\\Data\\" + path
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.z = z
        self.a = a
        self.c = c
    def book_files(self):
        files = os.listdir(self.path)
        i = 0
        for file in files:
            get_dt(self.path + "\\" + file)
            print(str(i) + "\t" + file)
            i += 1
    def get_dat(self, num):
        files = os.listdir(self.path)
        return get_data(self.path + "\\" + files[num]), files[num]
    def get_seq(self, seq):
        files = os.listdir(self.path)
        data = []
        for s in seq:
            data.append(get_data(self.path + "\\" + files[s]))
        return data
    def plot_rvt(self, seq, lat = 'a'):
        if (lat == 'a'):
            v = self.a + 'x'
        else:
            v = self.c + 'x'
        data = self.get_seq(seq)
        fig, ax = plt.subplots(figsize = (14,8))
        for dat in data:
            plt.plot(dat['TA'], dat[v]/dat['I'])
        plt.show()



# Sample Collection
samp0 = sample(name = "AA2", path = "FIB_ErTe30", \
ax = 128, ay = 3.7, bx = 130, by = 5.7, z = 1.58, a = "A", c = "B")

samp1 = sample(name = "TmTe3", path = 'TmTe3', ax = 166, ay = 18, bx = 160,
by = 20, z = 0.5, a = "a", c = "b")


################################################################################
#     PLOTS  PLOTS  PLOTS  PLOTS  PLOTS  PLOTS  PLOTS  PLOTS  PLOTS  PLOTS
################################################################################

###PLOT RvsT
def crackRvT(plot = True):
    rvt = samp1.get_dat(2)
    pf = np.polyfit(rvt['TA'][0:100], rvt['ax'][0:100], 1)
    if (plot):
        fig, ax = plt.subplots(figsize = (14,8))
        plt.plot(rvt['TA'], rvt['bx']/rvt['bx'][0], label = 'Rc')
        plt.plot(rvt['TA'], (rvt['ax'] - pf[1])/(rvt['ax'][0] - pf[1]), label = 'Ra with Crack Resistance Subtracted')
        plt.xlabel('Temperature (K)', fontsize = 18)
        plt.ylabel('R/R(295 K)', fontsize = 18)
        plt.legend(fontsize = 18)
        plt.show()
    return pf[1]

def sliding():
    #Sliding at 230K
    dat = samp1.get_dat(0)
    fig, ax = plt.subplots(figsize = (14,8))
    plt.title('TmTe3 Sliding at 230 K', fontsize = 18)

    plt.plot(dat['Offset']*1e3, dat['bx']/dat['bx'][50], label = 'C Axis')
    plt.ylabel('R/R[0]', fontsize = 13)
    plt.xlabel('Offset Current (mA)', fontsize = 15)
    plt.plot(dat['Offset']*1e3, dat['ax']/dat['ax'][50], label = 'A Axis, with Crack Reistance Included')
    plt.plot(dat['Offset']*1e3, (dat['ax'] - crack_v/2)/(dat['ax'][50] - crack_v/2), label = 'A Axis, with Crack Resistance Subtracted')
    plt.legend(fontsize = 14)
    plt.show()

    ###2 Channel SLIDING at 200 K
    dat = samp1.get_dat(17)
    fig, ax = plt.subplots(figsize = (14,8))
    plt.title('TmTe3 Sliding at 200 K', fontsize = 18)

    plt.plot(dat['Offset']*1e3, dat['bx']/dat['bx'][50], label = 'C Axis')
    plt.ylabel('R/R[0]', fontsize = 13)
    # plt.title(i)
    plt.xlabel('Offset Current (mA)', fontsize = 15)
    poly = np.polyfit(dat['Offset'][np.fabs(dat['Offset'])> 0.005], dat['ax'][np.fabs(dat['Offset'])> 0.005], 2)
    varesid = dat['ax'] - crack_v/2 - poly[0]*dat['Offset']*dat['Offset']
    plt.plot(dat['Offset']*1e3, dat['ax']/dat['ax'][50], label = 'A Axis, with Crack Resistance Included')
    plt.plot(dat['Offset']*1e3, (dat['ax'] - crack_v/2)/(dat['ax'][50] - crack_v/2), label = 'A Axis, with Crack Resistance Subtracted')
    plt.plot(dat['Offset']*1e3, varesid/varesid[50], label = 'A Axis, with Crack Resistance and Heating Subtracted')
    plt.legend(fontsize = 14)
    plt.show()

    ###180K Sliding
    dat = samp1.get_dat(38)
    fig, ax = plt.subplots(figsize = (14,8))
    plt.title('TmTe3 Sliding at 180 K', fontsize = 18)
    pf = np.polyfit(dat['Offset'][np.fabs(dat['Offset']) < 0.007], dat['bx'][np.fabs(dat['Offset']) < 0.007], 2)
    vresid = dat['bx'] - pf[0]*dat['Offset']*dat['Offset']
    plt.plot(dat['Offset']*1e3, dat['bx']/dat['bx'][50], label = 'C Axis')
    plt.plot(dat['Offset']*1e3, vresid/vresid[50], label = 'C Axis (heating subtracted)')
    plt.ylabel('R/R[0]', fontsize = 13)
    plt.xlabel('Offset Current (mA)', fontsize = 15)
    # plt.plot(dat['Offset']*1e3, dat['ax']/dat['ax'][50], label = 'A Axis, with Crack Reistance Included')
    # plt.plot(dat['Offset']*1e3, (dat['ax'] - crack_v/2)/(dat['ax'][50] - crack_v/2), label = 'A Axis, with Crack Resistance Subtracted')
    plt.legend(fontsize = 14)
    plt.show()

#Returns time in seconds
def toTime(times):
    time = []
    tp = 0
    for t in times:
        tn = float(t[:2])*60*60 + float(t[3:5])*60 + float(t[6:])
        while(tn < tp):
            tn += 60*60*24
        time.append(tn)
        tp = tn
    return np.array(time)


def slidingstrain180():
    dat = samp1.get_dat(46)
    n = 20
    quadrad = 0
    fig, ax = plt.subplots(figsize = (14,8))
    time = toTime(dat['time2'][:50*20])/60
    plt.plot(time - time[0], dat['TA'][:50*20])
    plt.xlabel('Time (minutes)')
    plt.ylabel('TA (K)')
    plt.title('Janis Temperature Stability at 180K')
    plt.show()
    for i in range(n):
        of = dat['Offset'][i*50:(i+1)*50]
        v = dat['bx'][i*50:(i+1)*50]

        pf = np.polyfit(of[0:20], v[0:20], 2)
        quadrad += pf[0]
    quadrad = quadrad/n
    # for i in range(n):
    #     of = dat['Offset'][i*50:(i+1)*50]
    #     v = dat['bx'][i*50:(i+1)*50]
    #     sgv = dat['sgv'][i*50:(i+1)*50]
    #     sgx = dat['sgx'][i*50:(i+1)*50]
    #
    #     vresid = v - quadrad * of * of
    #
    #     plt.plot(of*1e3, v*2e3)
    of = dat['Offset'][0:50*20]
    v = dat['bx'][0:50*20]
    vresid = v - pf[0]*of*of
    of = of*1e3
    v = v*2e3
    vresid = vresid*2e3
    sgx = dat['sgx'][0:50*20]*1e6
    sgx = sgx - sgx[0]

    fig, ax = plt.subplots(figsize = (14,8))
    im = plt.scatter(of, v, c = sgx, cmap = 'rainbow')
    cbar = plt.colorbar(im)
    cbar.ax.set_ylabel('Strain Proxy', fontsize = 18)
    plt.xlabel('Offset Current (mA)', fontsize = 18)
    plt.ylabel(r'R$_c$ ($\Omega$)', fontsize = 18)
    plt.title('180K Sliding Under Applied Strain', fontsize = 18)
    plt.show()

    fig, ax = plt.subplots(figsize = (14,8))
    im = plt.scatter(of, vresid, c = sgx, cmap = 'rainbow')
    cbar = plt.colorbar(im)
    cbar.ax.set_ylabel('Strain Proxy', fontsize = 18)
    plt.xlabel('Offset Current (mA)', fontsize = 18)
    plt.ylabel(r'R$_c$ ($\Omega$)', fontsize = 18)
    plt.title('180K Sliding Under Applied Strain (Heating Subtracted)', fontsize = 18)
    plt.show()


    #Create color map:
    dx = 3.5/20
    dy = 1.5/50
    y, x = np.mgrid[slice(-1, -1 + (n)*dx, dx),
                    slice(0, 1.5, dy)]
    z = np.ndarray((n, 50))
    dz = np.zeros((n, 50))
    zresid = np.ndarray((n, 50))
    zrn = np.ndarray((n, 50))
    dzresid = np.zeros((n, 50))
    for i in range(n):
        zo = dat['bx'][i*50]
        for j in range(50):
            z[i][j] = dat['bx'][i*50 + j]
            zresid[i][j] = z[i][j] - quadrad * dat['Offset'][i*50 + j]*dat['Offset'][i*50 + j]
            zrn[i][j] = zresid[i][j]/zo
            if (j > 0):
                dz[i][j] = (z[i][j] - z[i][j-1])/dy
                dzresid[i][j] = (zresid[i][j] - zresid[i][j-1])/dy

    # fig, ax = plt.subplots(figsize = (14,10))
    # strain = dat['sgx'][0:50*20]*1e6/350
    # offset = dat['Offset'][0:50*20]*1e3
    # im = plt.scatter(offset, strain, c = dz.flatten(), cmap = 'Spectral', marker = 'o', s = 400, alpha = 0.8)
    # cbar = plt.colorbar(im)
    # cbar.ax.set_ylabel('R/R[0] (C axes only)', fontsize = 18)
    # plt.xlim(min(offset), max(offset))
    # plt.ylim(min(strain), max(strain))
    # plt.xlabel('Offset Current (mA)', fontsize = 18)
    # plt.ylabel('Strain Proxy', fontsize = 18)
    # plt.title('Sliding CDW under Strain at 180K (TmTe3)', fontsize = 18)
    # plt.show()

    # fig, ax = plt.subplots(figsize = (14,8))
    # im = plt.pcolormesh(x, y, zrn, cmap = 'Spectral')
    # fig.colorbar(im)
    #
    # plt.show()

###DO ssCDW Plots between 180K and 220K
# dat = samp1.get_dat(49)
# dat1 = samp1.get_dat(46)
# sgv = 1.5
# dat = dat[dat['sgv'] == sgv]
# dat1 = dat1[np.fabs(dat1['sgv'] - sgv) < 0.1]
# dat = np.concatenate([dat1, dat])
# ofs = []
# vs = []
# of = []
# v = []
# ts = []
# for i in range(len(dat)):
#     if ((i > 0) & (dat['Offset'][i] == 0)):
#         ofs.append(np.array(of))
#         of = []
#         vs.append(np.array(v))
#         v = []
#         ts.append(str(dat['TA'][i])[0:3] + " K")
#     of.append(dat['Offset'][i])
#     v.append(dat['bx'][i])
#
# fig, ax = plt.subplots(figsize = (14,8))
# # plt.plot(dat1['Offset']*1e3, dat1['bx']*1e3, label = str(dat1['TA'][0]))
# for j in range(len(ofs)):
#     pf = np.polyfit(ofs[j], vs[j], 2)
#     vr = vs[j] - pf[0]*ofs[j]*ofs[j]
#     plt.plot(ofs[j]*1e3, vs[j]*1e3, label = ts[j])
# # plt.plot(dat1['Offset'], dat1['bx'])
# # plt.plot(dat['Offset'], dat['bx'])
# plt.legend(fontsize = 15)
# plt.xlabel('Offset Current (mA)', fontsize = 15)
# plt.ylabel('C Axis Voltage (mV)', fontsize = 15)
# plt.title('Sliding CDW with Strain Voltage = ' + str(sgv*50) + ' V', fontsize = 18)
# plt.show()

### ELASTORESIStance
# dat = samp1.get_dat(36)
# # print(dat['TA'][0])
# fig, ax = plt.subplots(figsize = (14,8))
# plt.plot(dat['sgx'], dat['bx'])
# plt.show()

########################################################################################
#MAIN
#######################################

# samp1.book_files()
# crack_v = crackRvT(plot = True)
# sliding()
slidingstrain180()
