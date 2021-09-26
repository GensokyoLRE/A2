import json
import numpy as np
import os
import email
import pandas as pd

"""
Training set syntax: TRAIN_#.eml, 2500 emails
Test set syntax: TEST_#.eml, 1827 emails
"""

if __name__ == '__main__':

    words = {}

    cwd = os.getcwd()
    tr_d = cwd + "/TR"
    tt_d = cwd + "/TT"
    test = tr_d + "/TEST_1.eml"

    # len(os.listdir(tr_d)) finds length of tr_d
    with open(tr_d + "/TRAIN_1.eml", 'r') as inRead:
        parsed = email.message_from_file(inRead)
    print(parsed['subject'])

    # # Training Label Retrieval
    # with open('spam-mail.tr.label', 'r') as labelRead:
    #     labelDataRaw = pd.read_csv(labelRead).to_numpy()
    # labelData = labelDataRaw[:, 1]

    # safe, spam = 0, 0
    # for x in labelData:
    #     if x == 0:
    #         safe += 1
    #     else:
    #         spam += 1
    # print("Safe: ", safe) # Count: 779
    # print("Spam: ", spam) # Count: 1721


    # print(labelDataRaw[:,1])
    # print(len(labelDataRaw[:,1])) # 2nd col 2500

