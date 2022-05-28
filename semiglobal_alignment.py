import numpy as np
import copy

PAM250 = {
'A': {'A':  2, 'C': -2, 'D':  0, 'E': 0, 'F': -3, 'G':  1, 'H': -1, 'I': -1, 'K': -1, 'L': -2, 'M': -1, 'N':  0, 'P':  1, 'Q':  0, 'R': -2, 'S':  1, 'T':  1, 'V':  0, 'W': -6, 'Y': -3},
'C': {'A': -2, 'C': 12, 'D': -5, 'E':-5, 'F': -4, 'G': -3, 'H': -3, 'I': -2, 'K': -5, 'L': -6, 'M': -5, 'N': -4, 'P': -3, 'Q': -5, 'R': -4, 'S':  0, 'T': -2, 'V': -2, 'W': -8, 'Y':  0},
'D': {'A':  0, 'C': -5, 'D':  4, 'E': 3, 'F': -6, 'G':  1, 'H':  1, 'I': -2, 'K':  0, 'L': -4, 'M': -3, 'N':  2, 'P': -1, 'Q':  2, 'R': -1, 'S':  0, 'T':  0, 'V': -2, 'W': -7, 'Y': -4},
'E': {'A':  0, 'C': -5, 'D':  3, 'E': 4, 'F': -5, 'G':  0, 'H':  1, 'I': -2, 'K':  0, 'L': -3, 'M': -2, 'N':  1, 'P': -1, 'Q':  2, 'R': -1, 'S':  0, 'T':  0, 'V': -2, 'W': -7, 'Y': -4},
'F': {'A': -3, 'C': -4, 'D': -6, 'E':-5, 'F':  9, 'G': -5, 'H': -2, 'I':  1, 'K': -5, 'L':  2, 'M':  0, 'N': -3, 'P': -5, 'Q': -5, 'R': -4, 'S': -3, 'T': -3, 'V': -1, 'W':  0, 'Y':  7},
'G': {'A':  1, 'C': -3, 'D':  1, 'E': 0, 'F': -5, 'G':  5, 'H': -2, 'I': -3, 'K': -2, 'L': -4, 'M': -3, 'N':  0, 'P':  0, 'Q': -1, 'R': -3, 'S':  1, 'T':  0, 'V': -1, 'W': -7, 'Y': -5},
'H': {'A': -1, 'C': -3, 'D':  1, 'E': 1, 'F': -2, 'G': -2, 'H':  6, 'I': -2, 'K':  0, 'L': -2, 'M': -2, 'N':  2, 'P':  0, 'Q':  3, 'R':  2, 'S': -1, 'T': -1, 'V': -2, 'W': -3, 'Y':  0},
'I': {'A': -1, 'C': -2, 'D': -2, 'E':-2, 'F':  1, 'G': -3, 'H': -2, 'I':  5, 'K': -2, 'L':  2, 'M':  2, 'N': -2, 'P': -2, 'Q': -2, 'R': -2, 'S': -1, 'T':  0, 'V':  4, 'W': -5, 'Y': -1},
'K': {'A': -1, 'C': -5, 'D':  0, 'E': 0, 'F': -5, 'G': -2, 'H':  0, 'I': -2, 'K':  5, 'L': -3, 'M':  0, 'N':  1, 'P': -1, 'Q':  1, 'R':  3, 'S':  0, 'T':  0, 'V': -2, 'W': -3, 'Y': -4},
'L': {'A': -2, 'C': -6, 'D': -4, 'E':-3, 'F':  2, 'G': -4, 'H': -2, 'I':  2, 'K': -3, 'L':  6, 'M':  4, 'N': -3, 'P': -3, 'Q': -2, 'R': -3, 'S': -3, 'T': -2, 'V':  2, 'W': -2, 'Y': -1},
'M': {'A': -1, 'C': -5, 'D': -3, 'E':-2, 'F':  0, 'G': -3, 'H': -2, 'I':  2, 'K':  0, 'L':  4, 'M':  6, 'N': -2, 'P': -2, 'Q': -1, 'R':  0, 'S': -2, 'T': -1, 'V':  2, 'W': -4, 'Y': -2},
'N': {'A':  0, 'C': -4, 'D':  2, 'E': 1, 'F': -3, 'G':  0, 'H':  2, 'I': -2, 'K':  1, 'L': -3, 'M': -2, 'N':  2, 'P':  0, 'Q':  1, 'R':  0, 'S':  1, 'T':  0, 'V': -2, 'W': -4, 'Y': -2},
'P': {'A':  1, 'C': -3, 'D': -1, 'E':-1, 'F': -5, 'G':  0, 'H':  0, 'I': -2, 'K': -1, 'L': -3, 'M': -2, 'N':  0, 'P':  6, 'Q':  0, 'R':  0, 'S':  1, 'T':  0, 'V': -1, 'W': -6, 'Y': -5},
'Q': {'A':  0, 'C': -5, 'D':  2, 'E': 2, 'F': -5, 'G': -1, 'H':  3, 'I': -2, 'K':  1, 'L': -2, 'M': -1, 'N':  1, 'P':  0, 'Q':  4, 'R':  1, 'S': -1, 'T': -1, 'V': -2, 'W': -5, 'Y': -4},
'R': {'A': -2, 'C': -4, 'D': -1, 'E':-1, 'F': -4, 'G': -3, 'H':  2, 'I': -2, 'K':  3, 'L': -3, 'M':  0, 'N':  0, 'P':  0, 'Q':  1, 'R':  6, 'S':  0, 'T': -1, 'V': -2, 'W':  2, 'Y': -4},
'S': {'A':  1, 'C':  0, 'D':  0, 'E': 0, 'F': -3, 'G':  1, 'H': -1, 'I': -1, 'K':  0, 'L': -3, 'M': -2, 'N':  1, 'P':  1, 'Q': -1, 'R':  0, 'S':  2, 'T':  1, 'V': -1, 'W': -2, 'Y': -3},
'T': {'A':  1, 'C': -2, 'D':  0, 'E': 0, 'F': -3, 'G':  0, 'H': -1, 'I':  0, 'K':  0, 'L': -2, 'M': -1, 'N':  0, 'P':  0, 'Q': -1, 'R': -1, 'S':  1, 'T':  3, 'V':  0, 'W': -5, 'Y': -3},
'V': {'A':  0, 'C': -2, 'D': -2, 'E':-2, 'F': -1, 'G': -1, 'H': -2, 'I':  4, 'K': -2, 'L':  2, 'M':  2, 'N': -2, 'P': -1, 'Q': -2, 'R': -2, 'S': -1, 'T':  0, 'V':  4, 'W': -6, 'Y': -2},
'W': {'A': -6, 'C': -8, 'D': -7, 'E':-7, 'F':  0, 'G': -7, 'H': -3, 'I': -5, 'K': -3, 'L': -2, 'M': -4, 'N': -4, 'P': -6, 'Q': -5, 'R':  2, 'S': -2, 'T': -5, 'V': -6, 'W': 17, 'Y':  0},
'Y': {'A': -3, 'C':  0, 'D': -4, 'E':-4, 'F':  7, 'G': -5, 'H':  0, 'I': -1, 'K': -4, 'L': -1, 'M': -2, 'N': -2, 'P': -5, 'Q': -4, 'R': -4, 'S': -3, 'T': -3, 'V': -2, 'W':  0, 'Y': 10}
}

def count_alphabets(s):
    """
    Counts the number of alphabets in a string.
    """
    count = 0
    for i in s:
        if i.isalpha():
            count += 1
    return count

def create_matrix(x, y, gap_penalty):
    """
    Creates a n x n matrix of zeros.
    """
    matrix =  np.zeros((x+1, y+1))
    return matrix

def traceback_matrix(x, y):
    """
    Creates a traceback matrix.
    """
    T_matrix = {}
    for i in range(x+1):
        for j in range(y+1):
            t = (i, j)
            
            if i == 0 and j == 0:
                T_matrix[t] = ['Done']
            elif i == 0 and j != 0:
                T_matrix[t] = ['Left']
            elif i != 0 and j == 0:
                T_matrix[t] = ['Up']
            else:
                T_matrix[t] = []

            
                
    return T_matrix

def get_max_index(m, x, y):
    """
    Returns the index of the maximum value in a matrix.
    """
    max_col = matrix[:, -1].max()
    max_row = matrix[-1, :].max()
    max_value = max(max_col, max_row)
    print(int(max_value))
   # max_index = np.where(m == max_value)
    maxe_index = []
    for i in range(x):
        for j in range(y):
            if m[i][j] == max_value:
                if j == y-1 or i == x-1:
                    maxe_index.append((i, j))
                    #print(i, j)

    return maxe_index

def fill_matrix(s1, s2, matrix, T_matrix, gap_penalty):
    """
    Fills the matrix with the values of the scoring matrix.
    """
    x = len(s1)
    y = len(s2)
    for i in range(1, x+1):
        for j in range(1, y+1):
            t = (i, j)
            horizantal = matrix[i][j-1] + gap_penalty
            vertical = matrix[i-1][j] + gap_penalty
            diagonal = matrix[i-1][j-1] + PAM250[s1[i-1]][s2[j-1]]
            matrix[i][j] = max(horizantal, vertical, diagonal)
            #print(matrix[i][j])
            if matrix[i][j] == horizantal:
                T_matrix[t].append('Left')
            if matrix[i][j] == vertical:
                T_matrix[t].append('Up')
            if matrix[i][j] == diagonal:
                T_matrix[t].append('Diag') # diagonal
    return matrix, T_matrix

def traceback(s1, s2, T_matrix):
    """
    Tracesback the matrix to find the optimal alignment.
    """
    x = len(s1)
    y = len(s2)
    i = x
    j = y
    alignment1 = ''
    alignment2 = ''

    while i > 0 or j > 0:
        print(i, j)
        if (i, j) in T_matrix:
            temp = copy.deepcopy(T_matrix[(i, j)])
            direction = temp.pop()
            print(direction)
            
            if direction == 'Diag':
                alignment1 += s1[i-1]
                alignment2 += s2[j-1]
                i -= 1
                j -= 1
            elif direction == 'Left':
                alignment1 += s1[i-1]
                alignment2 += '-'
                j -= 1
            elif direction == 'Up':
                alignment1 += '-'
                alignment2 += s2[j-1]
                i -= 1
            else:
                break
        else:
            break
    return alignment1[::-1], alignment2[::-1]
Seq = []
def recursive_traceback(ix, jx, s1, s2, T_matrix, alignment1, alignment2):
    """
    Recursive traceback.
    """
    global Seq

    if (ix, jx) in T_matrix:
        temp = copy.deepcopy(T_matrix[(ix, jx)])
        if ix == 0 and jx == 0:
                Seq.append((alignment1[::-1], alignment2[::-1]))
        while len(temp) > 0: 
            direction = temp.pop()
            at = copy.deepcopy(alignment1)
            bt = copy.deepcopy(alignment2)
            if direction == 'Diag':

                recursive_traceback(ix-1, jx-1, s1, s2, T_matrix, alignment1 + s1[ix-1], alignment2+s2[jx-1])
                alignment1 = at
                alignment2 = bt
            elif direction == 'Left':

                recursive_traceback(ix, jx-1, s1, s2, T_matrix, alignment1+'-', alignment2+ s2[jx-1])
                alignment1 = at
                alignment2 = bt
            elif direction == 'Up':

                recursive_traceback(ix-1, jx, s1, s2, T_matrix, alignment1 + s1[ix-1], alignment2+'-' )
                
            alignment1 = at
            alignment2 = bt

def get_all_alignments(max_index, s1, s2, matrix, T_matrix, gap_penalty):
    """
    Returns all the alignments.
    """
    for i in max_index:
        ix = i[0]
        jx = i[1]
        recursive_traceback(ix, jx, s1, s2, T_matrix, '', '')

    seq = []
    for s in Seq:

        for i in max_index:
            i1 = len(s1)
            j1 = len(s2)
            m = max(i1, j1)
            #print(m)
            alignment1 = s[0]
            alignment2 = s[1]
            a2 = ""
            a1 = ""
            #print(i)
            if i1-i[0]:
                while i1 > i[0]:
                    a2 += '-'
                    a1 += s1[i1-1]
                    i1 -= 1
            if j1-i[1]:
                while j1 > i[1]:
                    a1 += '-'
                    a2 += s2[j1-1]
                    j1 -= 1
            
            alignment1 += a1[::-1]
            alignment2 += a2[::-1]

            if count_alphabets(alignment1) == len(s1) and count_alphabets(alignment2) == len(s2):
                seq.append((alignment2, alignment1))
                
    return seq




if __name__ == "__main__":

    y = input()
    x = input()

    gap_penalty = -9
    matrix = create_matrix(len(x), len(y), gap_penalty)
    T_matrix = traceback_matrix(len(x), len(y))

    a, b = fill_matrix(x, y, matrix, T_matrix, gap_penalty)
    g = get_max_index(a, len(x)+1, len(y)+1)
    g.reverse()
 
    ix = g[0][0]
    jx = g[0][1]
    seq = get_all_alignments(g, x, y, a, b, gap_penalty)
    sortedSeq = [i[0]+i[1] for i in seq]
    sortedSeq.sort()
    for i in sortedSeq:
        print(i[0:int(len(i)/2)])
        print(i[int(len(i)/2):])
