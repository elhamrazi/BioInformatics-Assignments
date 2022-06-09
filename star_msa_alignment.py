import copy

def global_align(x, y, s_match, s_mismatch, s_gap):
    added_gaps = []
    A = []
    for i in range(len(y) + 1):
        A.append([0] * (len(x) + 1))
    for i in range(len(y) + 1):
        A[i][0] = s_gap * i
    for i in range(len(x) + 1):
        A[0][i] = s_gap * i

    for i in range(1, len(y) + 1):
        for j in range(1, len(x) + 1):
            A[i][j] = max(
                A[i][j - 1] + s_gap,
                A[i - 1][j] + s_gap,
                A[i - 1][j - 1] + (s_match if (y[i - 1] == x[j - 1] and y[i - 1] != '-') else 0) + (
                    s_mismatch if (y[i - 1] != x[j - 1] and y[i - 1] != '-' and x[j - 1] != '-') else 0) + (
                    s_gap if (y[i - 1] == '-' or x[j - 1] == '-') else 0)

            )
    align_X = ""
    align_Y = ""
    i = len(x)
    j = len(y)
    while i > 0 or j > 0:

        current_score = A[j][i]
        if i > 0 and j > 0 and (
                ((x[i - 1] == y[j - 1] and y[j - 1] != '-') and current_score == A[j - 1][i - 1] + s_match) or
                ((y[j - 1] != x[i - 1] and y[j - 1] != '-' and x[i - 1] != '-') and current_score == A[j - 1][

                    i - 1] + s_mismatch) or

                ((y[j - 1] == '-' or x[i - 1] == '-') and current_score == A[j - 1][i - 1] + s_gap)

        ):

            align_X = x[i - 1] + align_X
            align_Y = y[j - 1] + align_Y
            i = i - 1
            j = j - 1

        elif i > 0 and (current_score == A[j][i - 1] + s_gap):
            candidate_gap = j
            while True:
                if candidate_gap+1 < len(align_Y) and align_Y[candidate_gap+1] == '-':
                    candidate_gap += 1
                else:
                    break
            
            added_gaps.append(candidate_gap)
            align_X = x[i - 1] + align_X
            align_Y = "-" + align_Y
            i = i - 1

        else:
            
            align_X = "-" + align_X
            align_Y = y[j - 1] + align_Y
            j = j - 1
    added_gaps.reverse()
   
    return align_X, align_Y, A[len(y)][len(x)], added_gaps


def create_score_matrix(seqs, n):
    sp = {}
    sums = {}
    total = 0
    for i in range(n):
        temp_dict = {}
        sum = 0
        for j in range(n):
            if i != j:
                temp_dict[j] = global_align(seqs[i], seqs[j], 3, -1, -2)[2]
                sum += temp_dict[j]
        sp[i] = temp_dict
        sums[i] = sum
        total += sum
    return sp, sums, total


def c_star(init_seqs, n):
    seqs = delete_gaps(init_seqs, n)
    # print(seqs)
    sp, sum, total = create_score_matrix(seqs, n)
    center_index = max(sum, key=sum.get)
    progressive_align_order = {k: v for k, v in sorted(sp[center_index].items(), key=lambda item: item[1], reverse=True)}
  
    star_align = copy.deepcopy(seqs)
    for i in progressive_align_order.keys():
        temp_center = star_align[center_index]
        align_o, align_c, _, gaps = global_align(star_align[i], temp_center, 3, -1, -2)
       
        star_align[center_index] = align_c
        star_align[i] = align_o
        # gaps_ = find_gaps(align_c, temp_center)
        for i in range(len(gaps)-1):
            if gaps[i]+1 < len(temp_center):
                if temp_center[gaps[i]+1] == '-':
                    gaps[i] += 1
        print(align_c, align_o)
        # print(gaps_)
        star_align = insert_gaps(progressive_align_order, star_align, gaps, i)
    return get_score(star_align), star_align
    


def insert_gaps(dict, seq, gaps, i):        
    for j in dict.keys():
        if j == i:
            return seq
        for k in range(len(gaps)):
            temp = seq[j]
            temp = temp[:gaps[k]] + '-' + temp[gaps[k]:]     
            seq[j] = temp
            if k != len(gaps) - 1:
                # seq[j] = seq[j][:gaps[k + 1]] + '-' + seq[j][gaps[k + 1]:]
                gaps[k+1] += 1   
    return seq

def find_gaps(s1, s2):
    gaps = []
    for i in range(len(s1)):
        if i < len(s2) and s1[i] != s2[i]:
        # if s1[i] != s2[i]:
            if s1[i] == '-':
                gaps.append(i)
                s2 = s2[:i] + '-' + s2[i:]
            
                # print("gap: ", i)
            
    return gaps

def get_score(seqs):
    scores = 0
    for i in range(len(seqs)):
        for j in range(len(seqs)):
            if i != j:
                s = 0
                # print(seqs[i], seqs[j])
                for k in range(len(seqs[i])):
                    if seqs[i][k] == seqs[j][k]:
                        if seqs[i][k] != '-':
                            s += 3
                    elif seqs[i][k] != seqs[j][k]:
                        if seqs[i][k] == '-' or seqs[j][k] == '-':
                            s += -2
                        else:
                            s += -1
                scores += s
    return int(scores / 2)


def find_all_matches_index(seqs, n):
    all_match = [-1]
    for i in range(1):
        for k in range(len(seqs[i])):
            count = 0
            for j in range(n):
                if i != j:
                    if seqs[i][k] == seqs[j][k]:
                        count += 1
                    if count == n - 1:
                        if seqs[i][k] != '-' and seqs[j][k] != '-':
                            if k not in all_match:
                                all_match.append(k) 
    all_match.append(len(seqs[0]))
    return all_match


def find_blocks(seqs, matches_index, n):
    blocks = {}
    if len(matches_index) == 0:
        return -1
    if len(matches_index) == 1:
        temp = []
        for j in range(n):
                temp.append(seqs[j][matches_index[0]+1:])
        blocks[(matches_index[0]+1, n-1)] = temp
    else:
        for i in range(len(matches_index)-1):
            temp = []
            if matches_index[i + 1] - matches_index[i] > 2:
                for j in range(n):
                    temp.append(seqs[j][matches_index[i]+1:matches_index[i + 1]])
                blocks[(matches_index[i]+1, matches_index[i + 1])] = temp
    return blocks

def improve_cstar(seqs, n):
    score, cstar = c_star(seqs, n)
    # for cs in cstar:
    #     print(cs)
    while True:
        indexes = find_all_matches_index(cstar, n)
        # print(indexes)
        if len(indexes) == 0:
            return get_score(cstar), cstar
        blocks = find_blocks(cstar, indexes, n)
        done = 0
        for key in blocks.keys():
            score = get_score(blocks[key])
            blocks[key] = delete_gaps(blocks[key], n)
            
            new_score, new_cstar = c_star(blocks[key], n)
            if new_score > score:
                for i in range(n):
                    # print("before ", cstar[i])
                    temp = ""
                    temp = cstar[i][: key[0]] + new_cstar[i] + cstar[i][key[1]:]
                    cstar[i] = temp
                    # print(cstar[i])
                score = get_score(cstar)
                break
            done += 1
        if done == len(blocks):
            break

    return get_score(cstar), cstar

def delete_gaps(seqs, n):
    for i in range(n):
            temp = seqs[i].replace("-", "")
            seqs[i] = temp
    return seqs 


def main():
    n = int(input())
    seqs = []
    for i in range(n):
        seqs.append(input())
    s, cstar = improve_cstar(seqs, n)
    print(s)
    for i in range(n):
        print(cstar[i])


if __name__ == "__main__":
    main()
