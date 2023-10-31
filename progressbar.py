#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print a progress bar
"""

#!!
# Need to disable the interactive mode plt.ioff()
# otherwise plots will pop up and disappear
# OR : close all plots at the end
#!!

def progress_bar (iteration, total, prefix = 'Progress:', suffix = '', decimals = 1, length = 40, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    iteration+=1
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r{!s} |{!s}| {!s}% {!s}'.format(prefix, bar, percent,suffix), end='')
    # Print New Line on Complete
    if iteration == total: 
        print
    return 0