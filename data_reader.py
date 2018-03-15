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
    def __init__(self, path):
        self.path = path
        self.bridge = {}
        self.bridge_len = {}
        self.bridge_wid = {}
        self.bridge_z = {}
    def book_files(self, output = True):
        files = os.listdir(self.path)
        i = 0
        for file in files:
            get_dt(self.path + "\\" + file)
            if(output):
                print(str(i) + "\t" + file)
            i += 1
    def add_bridge(self, name, l, w, z):
        self.bridge[name] = l/w/z
        self.bridge_len[name] = l
        self.bridge_wid[name] = w
        self.bridge_z[name] = z
    def b(self, name):
        return self.bridge[name]
    def bl(self, name):
        return self.bridge_len[name]
    def bw(self, name):
        return self.bridge_wid[name]
    def bz(self, name):
        return self.bridge_z[name]
    def get_dat(self, num):
        files = os.listdir(self.path)
        return get_data(self.path + "\\" + files[num]), files[num]
    def get_file(self, fname):
        return get_data(self.path + "\\" + fname)

    # def get_seq(self, seq):
    #     files = os.listdir(self.path)
    #     data = []
    #     for s in seq:
    #         data.append(get_data(self.path + "\\" + files[s]))
    #     return data
    # def plot_rvt(self, seq, lat = 'a'):
    #     if (lat == 'a'):
    #         v = self.a + 'x'
    #     else:
    #         v = self.c + 'x'
    #     data = self.get_seq(seq)
    #     fig, ax = plt.subplots(figsize = (14,8))
    #     for dat in data:
    #         plt.plot(dat['TA'], dat[v]/dat['I'])
    #     plt.show()
