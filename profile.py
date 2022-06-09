import numpy as np
import itertools

def count_sum(seqs):
    sum = {}
    for i in seqs:
        for j in i:
            if j in sum:
                sum[j] += 1
            else:
                sum[j] = 1
    return sum

def create_pssm(msa):
    sum_ = count_sum(msa)
    pssm = {}
    for i in sum_.keys():
        pssm[i] = []
        for j in range(len(msa[0])):
            pssm[i].append(0)
    for i in range(len(msa[0])):
        for j in range(len(msa)):
            pssm[msa[j][i]][i] += 1

    for i in pssm.keys():
        for j in range(len(pssm[i])):
            pssm[i][j] += 2

    for i in pssm.keys():
        for j in range(len(pssm[i])):
            pssm[i][j] = int(pssm[i][j]/(len(list(sum_.keys())) * 2 + len(msa)) * 1000)
            pssm[i][j] = pssm[i][j]/1000
    
    for i in pssm.keys():
        row_sum = sum(pssm[i])
        for j in range(len(pssm[i])):
            pssm[i][j] = round(pssm[i][j]/(row_sum / 5), 3)

    for i in pssm.keys():
        pssm[i] = np.log2(pssm[i])
    
    for i in pssm.keys():
        for j in range(len(pssm[i])):
            pssm[i][j] = round(pssm[i][j], 3)
    return pssm 

def add_pseudocount(pssm, pseudocount):
    for i in pssm.keys():
        for j in range(len(pssm[i])):
            pssm[i][j] += pseudocount
    return pssm


def get_all_substrings(string, l):
    substrings = []
    for i in range(len(string)):
        for j in range(i, len(string)):
            if len(string[i:j+1]) <= l and string[i:j+1] not in substrings:
                substrings.append(string[i:j+1])
    return substrings

def insert_gaps(string, n):
    result = []
    t = ""
    itter = []
    for i in range(n):
        t += "-"
        itter.append(i)
    for i in itertools.combinations(itter, len(string)):
        idx = 0
        temp = t
        for j in i:
            temp = temp[:j] + string[idx] + temp[j+1:]
            # temp[j] = string[idx]
            idx += 1
        result.append(temp)
    return result

def calculate_score(seq, pssm):
    score = 0
    for i in range(len(seq)):
        score += pssm[seq[i]][i]
    return score

def get_best_seq(pssm, st, n):
    score = -1000
    best = ""
    all_subs = get_all_substrings(st, len(st))
    for s in all_subs:
        with_gaps = insert_gaps(s, n)
        for g in with_gaps:
            g_score = calculate_score(g, pssm)
            if g_score > score:
                score = g_score
                best = g

    return best
        
    
    
if __name__ == "__main__":
    n = int(input())
    msa = []
    for i in range(n):
        s = input()
        msa.append(s)
    st = input()

    pssm = create_pssm(msa)
    print(get_best_seq(pssm, st, len(msa[0])))


