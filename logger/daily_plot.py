import os
import time
import datetime
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.8
plt.rcParams['grid.alpha'] = 0.8
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

dat_path = "/home/hgsensor/Applications/clean_room_monitor/data/"

file_list = [f for f in os.listdir(dat_path) \
            if (os.path.isfile(os.path.join(dat_path, f)) and ('.txt' in f) and ('~' not in f))]
plot_list = [f for f in os.listdir(dat_path) \
             if (os.path.isfile(os.path.join(dat_path, f)) and ('.png' in f))]

for f in sorted(file_list):

    if f[:-4] + '.png' in plot_list:
        continue
    else:
        dat = np.genfromtxt(dat_path + f, comments='#', \
        dtype=[('date', 'S10'), ('time', 'S8'), ('temp', '<f8'), \
               ('hum', '<f8'), ('pres', '<i8'), ('cnt5', '<i8'), ('cnt25', '<i8'), \
               ('iso', '<i8'), ('class', '<i8')])

        nvals = len(dat)
        x = mdates.date2num([datetime.datetime.combine( \
                datetime.datetime.strptime(dat['date'][k], '%Y-%m-%d').date(), \
                datetime.datetime.strptime(dat['time'][k], '%H:%M:%S').time()) \
                for k in range(nvals)])

        j = 0
        fig, axes = plt.subplots(2, 2)
        for key in ['temp', 'hum', 'pres', 'cnt5']:
            y = dat[key]
            axes[j%2, j/2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            axes[j%2, j/2].xaxis.set_major_locator(mdates.HourLocator(interval=4))
            axes[j%2, j/2].plot(x, y, ls=' ', ms=1, marker='o', mfc="k", mec="k")
                                                   
            if (key == 'temp'):
                axes[j%2, j/2].set_ylim([18, 28])
                axes[j%2, j/2].set_ylabel('temperature [C]')
            elif (key == 'hum'):
                axes[j%2, j/2].set_ylim([30, 80])
                axes[j%2, j/2].set_ylabel('humidity [%]')
            elif (key == 'pres'):
                axes[j%2, j/2].set_ylim([90000, 110000])
                axes[j%2, j/2].set_ylabel('pressure [Pa]')
            elif (key == 'cnt5'):
                axes[j%2, j/2].set_ylim([1000, 10000000])
                axes[j%2, j/2].set_ylabel('# particles > 0.5 um / m^3 [-]')
                axes[j%2, j/2].axhline(y=3520000, linewidth=1.5, color='r')
                axes[j%2, j/2].axhline(y=352000, linewidth=1.5, color='b')
                axes[j%2, j/2].axhline(y=35200, linewidth=1.5, color='g')
                axes[j%2, j/2].axhline(y=3520, linewidth=1.5, color='m')
                axes[j%2, j/2].set_yscale('log')
            
            plt.gcf().autofmt_xdate()
            j += 1

        plt.savefig(dat_path + f[:-4] + '.png')
        plt.clf()
