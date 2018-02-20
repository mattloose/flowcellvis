import pandas
import sys
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import argparse

def get_coords(channel,flowcellsize):
    if flowcellsize==3000:
        #find which block of 12 we are in:
        block=(channel-1)//250
        remainder=(channel-1)%250
        row=remainder//10
        column=remainder%10+block*10
        return(column,row)
    if flowcellsize==128:
        return (channel//8, channel%8)
    else:
        return minION_flowcell_layout(channel)

def minION_flowcell_layout(channel):
    chanlookup = {1: (31, 0), 2: (31, 1), 3: (31, 2), 4: (31, 3), 5: (31, 4), 6: (31, 5), 7: (31, 6), 8: (31, 7),
                  9: (30, 0), 10: (30, 1), 11: (30, 2), 12: (30, 3), 13: (30, 4), 14: (30, 5), 15: (30, 6), 16: (30, 7),
                  17: (29, 0), 18: (29, 1), 19: (29, 2), 20: (29, 3), 21: (29, 4), 22: (29, 5), 23: (29, 6),
                  24: (29, 7), 25: (28, 0), 26: (28, 1), 27: (28, 2), 28: (28, 3), 29: (28, 4), 30: (28, 5),
                  31: (28, 6), 32: (28, 7), 33: (31, 15), 34: (31, 14), 35: (31, 13), 36: (31, 12), 37: (31, 11),
                  38: (31, 10), 39: (31, 9), 40: (31, 8), 41: (30, 15), 42: (30, 14), 43: (30, 13), 44: (30, 12),
                  45: (30, 11), 46: (30, 10), 47: (30, 9), 48: (30, 8), 49: (29, 15), 50: (29, 14), 51: (29, 13),
                  52: (29, 12), 53: (29, 11), 54: (29, 10), 55: (29, 9), 56: (29, 8), 57: (28, 15), 58: (28, 14),
                  59: (28, 13), 60: (28, 12), 61: (28, 11), 62: (28, 10), 63: (28, 9), 64: (28, 8), 65: (3, 0),
                  66: (3, 1), 67: (3, 2), 68: (3, 3), 69: (3, 4), 70: (3, 5), 71: (3, 6), 72: (3, 7), 73: (2, 0),
                  74: (2, 1), 75: (2, 2), 76: (2, 3), 77: (2, 4), 78: (2, 5), 79: (2, 6), 80: (2, 7), 81: (1, 0),
                  82: (1, 1), 83: (1, 2), 84: (1, 3), 85: (1, 4), 86: (1, 5), 87: (1, 6), 88: (1, 7), 89: (0, 0),
                  90: (0, 1), 91: (0, 2), 92: (0, 3), 93: (0, 4), 94: (0, 5), 95: (0, 6), 96: (0, 7), 97: (3, 15),
                  98: (3, 14), 99: (3, 13), 100: (3, 12), 101: (3, 11), 102: (3, 10), 103: (3, 9), 104: (3, 8),
                  105: (2, 15), 106: (2, 14), 107: (2, 13), 108: (2, 12), 109: (2, 11), 110: (2, 10), 111: (2, 9),
                  112: (2, 8), 113: (1, 15), 114: (1, 14), 115: (1, 13), 116: (1, 12), 117: (1, 11), 118: (1, 10),
                  119: (1, 9), 120: (1, 8), 121: (0, 15), 122: (0, 14), 123: (0, 13), 124: (0, 12), 125: (0, 11),
                  126: (0, 10), 127: (0, 9), 128: (0, 8), 129: (7, 0), 130: (7, 1), 131: (7, 2), 132: (7, 3),
                  133: (7, 4), 134: (7, 5), 135: (7, 6), 136: (7, 7), 137: (6, 0), 138: (6, 1), 139: (6, 2),
                  140: (6, 3), 141: (6, 4), 142: (6, 5), 143: (6, 6), 144: (6, 7), 145: (5, 0), 146: (5, 1),
                  147: (5, 2), 148: (5, 3), 149: (5, 4), 150: (5, 5), 151: (5, 6), 152: (5, 7), 153: (4, 0),
                  154: (4, 1), 155: (4, 2), 156: (4, 3), 157: (4, 4), 158: (4, 5), 159: (4, 6), 160: (4, 7),
                  161: (7, 15), 162: (7, 14), 163: (7, 13), 164: (7, 12), 165: (7, 11), 166: (7, 10), 167: (7, 9),
                  168: (7, 8), 169: (6, 15), 170: (6, 14), 171: (6, 13), 172: (6, 12), 173: (6, 11), 174: (6, 10),
                  175: (6, 9), 176: (6, 8), 177: (5, 15), 178: (5, 14), 179: (5, 13), 180: (5, 12), 181: (5, 11),
                  182: (5, 10), 183: (5, 9), 184: (5, 8), 185: (4, 15), 186: (4, 14), 187: (4, 13), 188: (4, 12),
                  189: (4, 11), 190: (4, 10), 191: (4, 9), 192: (4, 8), 193: (11, 0), 194: (11, 1), 195: (11, 2),
                  196: (11, 3), 197: (11, 4), 198: (11, 5), 199: (11, 6), 200: (11, 7), 201: (10, 0), 202: (10, 1),
                  203: (10, 2), 204: (10, 3), 205: (10, 4), 206: (10, 5), 207: (10, 6), 208: (10, 7), 209: (9, 0),
                  210: (9, 1), 211: (9, 2), 212: (9, 3), 213: (9, 4), 214: (9, 5), 215: (9, 6), 216: (9, 7),
                  217: (8, 0), 218: (8, 1), 219: (8, 2), 220: (8, 3), 221: (8, 4), 222: (8, 5), 223: (8, 6),
                  224: (8, 7), 225: (11, 15), 226: (11, 14), 227: (11, 13), 228: (11, 12), 229: (11, 11), 230: (11, 10),
                  231: (11, 9), 232: (11, 8), 233: (10, 15), 234: (10, 14), 235: (10, 13), 236: (10, 12), 237: (10, 11),
                  238: (10, 10), 239: (10, 9), 240: (10, 8), 241: (9, 15), 242: (9, 14), 243: (9, 13), 244: (9, 12),
                  245: (9, 11), 246: (9, 10), 247: (9, 9), 248: (9, 8), 249: (8, 15), 250: (8, 14), 251: (8, 13),
                  252: (8, 12), 253: (8, 11), 254: (8, 10), 255: (8, 9), 256: (8, 8), 257: (15, 0), 258: (15, 1),
                  259: (15, 2), 260: (15, 3), 261: (15, 4), 262: (15, 5), 263: (15, 6), 264: (15, 7), 265: (14, 0),
                  266: (14, 1), 267: (14, 2), 268: (14, 3), 269: (14, 4), 270: (14, 5), 271: (14, 6), 272: (14, 7),
                  273: (13, 0), 274: (13, 1), 275: (13, 2), 276: (13, 3), 277: (13, 4), 278: (13, 5), 279: (13, 6),
                  280: (13, 7), 281: (12, 0), 282: (12, 1), 283: (12, 2), 284: (12, 3), 285: (12, 4), 286: (12, 5),
                  287: (12, 6), 288: (12, 7), 289: (15, 15), 290: (15, 14), 291: (15, 13), 292: (15, 12), 293: (15, 11),
                  294: (15, 10), 295: (15, 9), 296: (15, 8), 297: (14, 15), 298: (14, 14), 299: (14, 13), 300: (14, 12),
                  301: (14, 11), 302: (14, 10), 303: (14, 9), 304: (14, 8), 305: (13, 15), 306: (13, 14), 307: (13, 13),
                  308: (13, 12), 309: (13, 11), 310: (13, 10), 311: (13, 9), 312: (13, 8), 313: (12, 15), 314: (12, 14),
                  315: (12, 13), 316: (12, 12), 317: (12, 11), 318: (12, 10), 319: (12, 9), 320: (12, 8), 321: (19, 0),
                  322: (19, 1), 323: (19, 2), 324: (19, 3), 325: (19, 4), 326: (19, 5), 327: (19, 6), 328: (19, 7),
                  329: (18, 0), 330: (18, 1), 331: (18, 2), 332: (18, 3), 333: (18, 4), 334: (18, 5), 335: (18, 6),
                  336: (18, 7), 337: (17, 0), 338: (17, 1), 339: (17, 2), 340: (17, 3), 341: (17, 4), 342: (17, 5),
                  343: (17, 6), 344: (17, 7), 345: (16, 0), 346: (16, 1), 347: (16, 2), 348: (16, 3), 349: (16, 4),
                  350: (16, 5), 351: (16, 6), 352: (16, 7), 353: (19, 15), 354: (19, 14), 355: (19, 13), 356: (19, 12),
                  357: (19, 11), 358: (19, 10), 359: (19, 9), 360: (19, 8), 361: (18, 15), 362: (18, 14), 363: (18, 13),
                  364: (18, 12), 365: (18, 11), 366: (18, 10), 367: (18, 9), 368: (18, 8), 369: (17, 15), 370: (17, 14),
                  371: (17, 13), 372: (17, 12), 373: (17, 11), 374: (17, 10), 375: (17, 9), 376: (17, 8), 377: (16, 15),
                  378: (16, 14), 379: (16, 13), 380: (16, 12), 381: (16, 11), 382: (16, 10), 383: (16, 9), 384: (16, 8),
                  385: (23, 0), 386: (23, 1), 387: (23, 2), 388: (23, 3), 389: (23, 4), 390: (23, 5), 391: (23, 6),
                  392: (23, 7), 393: (22, 0), 394: (22, 1), 395: (22, 2), 396: (22, 3), 397: (22, 4), 398: (22, 5),
                  399: (22, 6), 400: (22, 7), 401: (21, 0), 402: (21, 1), 403: (21, 2), 404: (21, 3), 405: (21, 4),
                  406: (21, 5), 407: (21, 6), 408: (21, 7), 409: (20, 0), 410: (20, 1), 411: (20, 2), 412: (20, 3),
                  413: (20, 4), 414: (20, 5), 415: (20, 6), 416: (20, 7), 417: (23, 15), 418: (23, 14), 419: (23, 13),
                  420: (23, 12), 421: (23, 11), 422: (23, 10), 423: (23, 9), 424: (23, 8), 425: (22, 15), 426: (22, 14),
                  427: (22, 13), 428: (22, 12), 429: (22, 11), 430: (22, 10), 431: (22, 9), 432: (22, 8), 433: (21, 15),
                  434: (21, 14), 435: (21, 13), 436: (21, 12), 437: (21, 11), 438: (21, 10), 439: (21, 9), 440: (21, 8),
                  441: (20, 15), 442: (20, 14), 443: (20, 13), 444: (20, 12), 445: (20, 11), 446: (20, 10),
                  447: (20, 9), 448: (20, 8), 449: (27, 0), 450: (27, 1), 451: (27, 2), 452: (27, 3), 453: (27, 4),
                  454: (27, 5), 455: (27, 6), 456: (27, 7), 457: (26, 0), 458: (26, 1), 459: (26, 2), 460: (26, 3),
                  461: (26, 4), 462: (26, 5), 463: (26, 6), 464: (26, 7), 465: (25, 0), 466: (25, 1), 467: (25, 2),
                  468: (25, 3), 469: (25, 4), 470: (25, 5), 471: (25, 6), 472: (25, 7), 473: (24, 0), 474: (24, 1),
                  475: (24, 2), 476: (24, 3), 477: (24, 4), 478: (24, 5), 479: (24, 6), 480: (24, 7), 481: (27, 15),
                  482: (27, 14), 483: (27, 13), 484: (27, 12), 485: (27, 11), 486: (27, 10), 487: (27, 9), 488: (27, 8),
                  489: (26, 15), 490: (26, 14), 491: (26, 13), 492: (26, 12), 493: (26, 11), 494: (26, 10),
                  495: (26, 9), 496: (26, 8), 497: (25, 15), 498: (25, 14), 499: (25, 13), 500: (25, 12), 501: (25, 11),
                  502: (25, 10), 503: (25, 9), 504: (25, 8), 505: (24, 15), 506: (24, 14), 507: (24, 13), 508: (24, 12),
                  509: (24, 11), 510: (24, 10), 511: (24, 9), 512: (24, 8)}
    return chanlookup[channel]

def map_bin(x,bins):
    x=float(x)
    kwargs= {}
    if x == max(bins):
        kwargs['right']=True
    bin = bins[np.digitize([x], bins, **kwargs)[0]]
    bin_lower = bins[np.digitize([x], bins, **kwargs)[0]-1]
    return (bin_lower+bin)/2

def animate(data, im):
    im.set_data(data)
    #ax.set_title('Frame {}'.format(i))

def step():
    for i in range(0, len(masterlist)):
        minutes = (((i*bin_width)+bin_width)/60)
        ax.set_title('Minutes {}'.format(minutes))
        data = plotimage(masterlist[i],flowcellsize)
        print (i)
        yield data

def plotimage(chancounts,flowcellsize):
    x=[]
    y=[]
    z=list(chancounts.values())
    for channel in chancounts.keys():
        x_,y_=get_coords(channel,flowcellsize)
        x.append(x_)
        y.append(y_)
    z_array = np.nan * np.empty((max(y)+1, max(x)+1))
    z_array[y, x] = z
    return z_array

def getmaxbin(x, base=5):
    return int((base * round(float(x)/base))+10*base)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',required=True, help='complete path to sequencing_summary.txt file to process')
    parser.add_argument('--output',required=True, help='filename to write gif image to.')
    args=parser.parse_args()
    sequencing_summary = args.input
    fields=['run_id','channel','start_time']
    print ("Loading file.")
    ss = pandas.read_csv(sequencing_summary, sep='\t', lineterminator='\n',usecols=fields)
    ss = ss.sort_values(by=['start_time'])
    global flowcellsize
    flowcellsize = 512
    print ("Calculating Flowcell Size.")
    if ss.channel.max() > flowcellsize:
        flowcellsize = 3000
    a=np.arange(1,flowcellsize+1)
    zeroedflowcell = dict.fromkeys(a, 0)
    global bin_width
    bin_width = 300
    print ("Calculating Bin Widths.")
    maxbinwidth = getmaxbin(ss.start_time.max(),base=bin_width)
    freq_bins = np.arange(0, maxbinwidth, bin_width)
    print ("Sorting Files.")
    ss['Binned'] = ss['start_time'].apply(map_bin, bins=freq_bins)
    ss = ss.sort_values(by=['Binned'])
    subsetdict = {
        'Binned': ss['Binned'],
        'channel': ss['channel'],
        'run_id': ss['run_id'],
        'start_time': ss['start_time'],
    }
    ss3 = pandas.DataFrame(data=subsetdict)
    g1 = ss3.groupby( [ 'run_id', "Binned", "channel"] ).count()
    g1 = g1.add_suffix('_Count').reset_index()
    runidlist = g1.run_id.drop_duplicates(keep='first').dropna()
    binlist = g1.Binned.drop_duplicates(keep='first').dropna()
    channellist = g1.where(g1.channel==0).dropna()
    global masterlist
    masterlist=[]
    print ("Parsing SeqSummary")
    for run in runidlist:
        print (run)
        for bin in binlist:
            print (bin)
            gsubset = g1.where(g1.run_id==run).where(g1.Binned==bin).dropna()
            if len(gsubset)>0:
                #print (gsubset)
                chandict=dict(zeroedflowcell)
                for index, row in gsubset.iterrows():
                    chandict[int(row['channel'])] = int(row['start_time_Count'])
                masterlist.append(chandict)
    print ("Rendering stuff.")
    global fig, ax
    fig, ax = plt.subplots()
    if flowcellsize <= 512:
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=None, hspace=None)
        fig.suptitle('Flowcell Layout {}'.format(flowcellsize), fontsize=14)
        fig.set_size_inches(11,6,forward=True)
    elif flowcellsize > 512:
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=None, hspace=None)
        fig.suptitle('Flowcell Layout {}'.format(flowcellsize), fontsize=14)
        fig.set_size_inches(9, 2.5, forward=True)
    im = ax.imshow(plotimage(masterlist[0],flowcellsize),cmap='hot', interpolation='nearest')
    ani = animation.FuncAnimation(
        fig, animate, step, interval=100, repeat=False, fargs=(im, ), save_count=len(masterlist))
    print ("Saving the GiF.")
    ani.save(args.output, fps=15, dpi=90,writer='imagemagick')


if __name__ == "__main__":
    # execute only if run as a script
    main()
