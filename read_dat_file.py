'''The code below pertains to an experiment in which I and a lab partner used a scintillator + PMT to estimate the lifetime of muons.
The code is meant to be used with a run that we used to calibrate the setup.
The first two functions below parse files generated by the detectors and output the relevant numbers from them.
The third function identifies all maxima in the data with a time (where the times that each peak should occur were known beforehand).
The fourth function compares the data fromthe two types of files collected (.dat and .log) to see if they coincide.
'''

'''Parse .dat files and read relevant data into memory'''
def dat2txt():
    infile = input("Input .dat file name (Or type 'q' to bypass): ")
    #loop until user is done inputting .dat files
    if infile != 'q':
        #check if .dat file
        infile = infile.strip()
        if '.' not in infile or infile.split('.')[1] != 'dat' or infile.split('.')[-1] != 'dat':
            print("Please enter a valid .dat file.")
        else: 
            #read out data from .dat file, write into .txt file of same name
            filename = infile.split('.')[0]
            data = []
            try:
                with open(infile, 'r') as d:
                    lines = d.readlines()
                    for i in range(len(lines)):
                        data.append(lines[i])
                with open(filename + ".txt", 'w') as f:
                    i = 1
                    for num in data:
                        f.write(str(i) + ': ' + num)
                        i += 1
            except: print("Please enter a .dat file that exists in this directory.")
    return data

'''Parse .log files and read relevant data into memory'''
def log2txt():
    infile = input("Input .log file name (Or type 'q' to bypass): ")
    if infile != 'q':
        infile = infile.strip()
        if len(infile.split('.')) == 2 and infile.split('.')[1] == 'log':
            try:
                with open(infile, 'r') as f:
                    lines = f.readlines()
                    bins = []
                    for line in lines: 
                        num = int(line, 16) + 1
                        bins.append(num)
                    bins.sort()
                counts = {}
                for i in range(max(bins)):
                    print(i)
                    counts[i+1] = bins.count(i+1)
                print(counts)
                filename = infile.split('.')[0]
                with open(filename + '.txt', 'w') as f:
                    for i in range(len(counts)):
                        f.write(str(i+1) + ': ' + str(counts[i+1]) + '\n')
            except: print("Please enter a .log file that exists in this directory.")
    return counts

'''Scans over a time series of data from a PMT, 
finds and returns maxima using both the local maxima and the average value of the data around the maxima.'''
def calmaxima(write_to_txt = False):
    counts = []
    with open('cali2.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            counts.append(int(line.split(': ')[1]))
    maxima = {}
    avgmaxima = {}
    error = {}
    peak_times = [1.0036, 2.003, 4.004, 6.005, 8.005, 10.0037, 12.002, 14.020, 16.013, 18.014, 19.022]

    n = 1
    for i in range(len(counts)):
        if counts[i] > 1000:
            if counts[i] > counts[i-1] and counts[i] > counts[i+1]:
                maxima[n] = i+1
                sum = 0
                sumsquares = 0
                totcounts = 0
                for k in range(i-6, i+7):
                    sum += counts[k]*(k+1)
                    totcounts += counts[k]
                    sumsquares += counts[k]*(k+1)**2
                avg = sum/totcounts
                avgmaxima[n] = avg
                stderr = (sumsquares/totcounts-avg**2)**(0.5)
                error[n] = stderr
                n += 1
        if i == 8000:
            break
    print(maxima)
    for i in range(len(maxima)):
        print('Peak {} at {}. Error: {}'.format(i + 1, avgmaxima[i+1], error[i+1]))

    if write_to_txt == True:
        with open('calpeaks2.txt', 'w') as f:
            f.write('Using averages:\n\n')
            for i in range(len(maxima)):
                f.write("{} us: {} {} {}".format(peak_times[i], maxima[i+1], avgmaxima[i+1], error[i+1]))
                f.write('\n')

'''Compare two .dat files.'''
def match_dat_log(file1, file2):
    with open(file1, 'r') as f:
        with open(file2, 'r') as g:
            lines1 = f.readlines()
            lines2 = g.readlines()
            files_match = 1
            n = 0
            for i in range(min(len(lines1), len(lines2))):
                print(i)
                if lines1[i].strip() == lines2[i].strip():
                    continue
                else:
                    files_match = 0
                    n = i + 1
                    break
            if files_match == 1: print("Files match!")
            if files_match == 0: print("Mismatch found at line {}".format(n))
            

if __name__ == '__main__':
    dat2txt()
    #log2txt()
    #match_dat_log('cali2hist.txt', 'cali2.txt')
    #calmaxima(True)
