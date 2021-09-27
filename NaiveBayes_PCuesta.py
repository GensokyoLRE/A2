import json
import string

import numpy as np
import os
import email
import pandas as pd

"""
Training set syntax: TRAIN_#.eml, 2500 emails
Test set syntax: TEST_#.eml, 1827 emails
"""


def get_sub_payload(file):
    with open(file, 'r', encoding='latin-1') as inRead:
        parsed = email.message_from_file(inRead)
        # the_load = parsed.get_payload()
        # if isinstance(the_load, list):
        #     the_load = the_load[0]
        # if not isinstance(the_load, type('')):
        #     the_load = str(the_load)
        subj = parsed.get('subject')
        subj = str(subj)
        # bad_sym = ['!', '?', ':', ';', '\'', '\"', '\n', '\t', '']
        # for char in string.punctuation:
        #     subj = subj.replace(char, '')
        # bad_phrase = []
        subj = subj.translate({ord(c): ' ' for c in "!?:;\"\n\t[]{}()<>/,$%^&*#@="})
        subj = subj.replace("...", '')
        subj = subj.replace("-", '')
        subj = subj.replace("..", '')
        return subj.lower()
        # return subj + the_load


if __name__ == '__main__':

    HAM_TR_CT = 1721 # label 1
    SPAM_TR_CT = 779 # label 0
    HAM_TR_RATE = HAM_TR_CT / (HAM_TR_CT + SPAM_TR_CT)
    SPAM_TR_RATE = SPAM_TR_CT / (HAM_TR_CT + SPAM_TR_CT)

    words = {}
    tt_res = []

    cwd = os.getcwd()
    tr_d = cwd + "/TR/TRAIN_"
    tt_d = cwd + "/TT/TEST_"
    tt_d_base = cwd + "/TT/"

    # Training Label Retrieval
    with open('spam-mail.tr.label', 'r') as labelRead:
        labelDataRaw = pd.read_csv(labelRead).to_numpy()
        np.savetxt('labels.csv', labelDataRaw, fmt='%d', delimiter=',')
    labelData = labelDataRaw[:, 1]
    # print(labelDataRaw[:, 1])  # print list of TR labels

    for it, stuff in enumerate(labelData):  # 'it' is iterator num, 'stuff' is label of 'it'
        # print(str(it) + " " + str(stuff))
        inFile = tr_d + str(it+1) + ".eml"
        subj_str = get_sub_payload(inFile).split(' ')
        subj_str_clone = subj_str.copy()
        while '' in subj_str:
            subj_str.remove('')
        for x in subj_str_clone[:]:
            try:
                float(x)
                subj_str.remove(x)
            except ValueError:
                pass
        for y in subj_str:
            if (y.startswith("\'") and y.endswith("\'")) or (y.startswith("\"") and y.endswith("\"")):
                y = y[1:-1]
            if y.endswith('.\n'):
                y = y[0:-1]
            if len(y) == 1:
                subj_str.remove(y)
        # print(subj_str)
        for word in subj_str:
            if word in words:
                words[word]['total_ct'] += 1
            else:
                w = {word: {'total_ct': 1, 'safe_ct': 0, 'spam_ct': 0, 'safe_rt': 0.000, 'spam_rt': 0.000}}
                words.update(w)
            if stuff == 1:
                words[word]['safe_ct'] += 1
            else:
                words[word]['spam_ct'] += 1
    for word in words:
        if word.isdigit():
            words.pop(word)
        words[word]['total_ct'] += 1
        words[word]['safe_ct'] += 1
        words[word]['spam_ct'] += 1
        words[word]['safe_rt'] = words[word]['safe_ct'] / HAM_TR_CT
        words[word]['spam_rt'] = words[word]['spam_ct'] / SPAM_TR_CT
    # Training Set Completed

    # # Write out Training Set for validation
    # with open('spit.json', 'w+') as spitOut:
    #     json.dump(words, spitOut)

    for it2 in range(len([name for name in os.listdir(tt_d_base)])):  # 'it2' is iterator num, 'stuff2' is label of 'it2'
        # print(str(it2) + " " + str(stuff2))
        class_id = 1
        inFile2 = tt_d + str(it2+1) + ".eml"
        subj_str2 = get_sub_payload(inFile2).split(' ')
        subj_str_clone2 = subj_str2.copy()
        while '' in subj_str2:
            subj_str2.remove('')
        for x in subj_str_clone2[:]:
            try:
                float(x)
                subj_str2.remove(x)
            except ValueError:
                pass
        for y in subj_str2:
            if (y.startswith("\'") and y.endswith("\'")) or (y.startswith("\"") and y.endswith("\"")):
                y = y[1:-1]
            if y.endswith('.\n'):
                y = y[0:-1]
            if len(y) == 1:
                subj_str2.remove(y)
        # print(subj_str2)

        tt_word_score_ham = HAM_TR_RATE
        tt_word_score_spam = SPAM_TR_RATE

        for tt_word in subj_str2:
            if tt_word in words:
                tt_word_score_ham *= words[tt_word]['safe_ct']
                tt_word_score_spam *= words[tt_word]['spam_ct']
        if tt_word_score_spam > tt_word_score_ham:
            class_id = 0
        tt_res_child = [it2+1, class_id]
        tt_res.append(tt_res_child)

    # Testing Set complete...?
    # Write out Testing Set for validation
    np.savetxt('spam-mail.tt.csv', tt_res, delimiter=',', fmt='%d', header="Id,Prediction", comments='')

    """
    Dict order:
    Word
    >Total Count
    >Safe Count
    >Spam Count
    >Safe Rate
    >Spam Rate
    """

