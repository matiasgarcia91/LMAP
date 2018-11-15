from BitVector import BitVector
import math

def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def calculate_round_approximations(batch, ID):
    A = batch["A"]
    B = batch["B"]
    C = batch["C"]
    D = batch["D"]
    IDS = batch["IDS"]
    a_ap = A
    b_ap = B
    c_ap = C
    d_ap = D
    ids_ap = IDS
    ap1 = A ^ B
    ap2 = B ^ C
    ap3 = C ^ D
    ap4 = A ^ C
    ap5 = B ^ D
    ap6 = A ^ D
    ap7 = IDS ^ A
    ap8 = IDS ^ B
    ap9 = IDS ^ C
    ap10 = IDS ^ D
    ap11 = A ^ B ^ C
    ap12 = A ^ B ^ D
    ap13 = A ^ B ^ IDS
    ap14 = A ^ C ^ D
    ap15 = A ^ C ^ IDS
    ap16 = A ^ D ^ IDS
    ap17 = B ^ C ^ D
    ap18 = B ^ D ^ IDS
    ap19 = B ^ C ^ IDS
    ap20 = C ^ D ^ IDS
    ap21 = A ^ B ^ C ^ D
    ap22 = A ^ B ^ C ^ IDS
    ap23 = A ^ B ^ D ^ IDS
    ap24 = A ^ C ^ D ^ IDS
    ap25 = B ^ C ^ D ^ IDS
    ap26 = A ^ B ^ C ^ D ^ IDS
    round_aprox = [ap1, ap2, ap3, ap4, ap5, ap6, ap7, ap8, ap9, ap10, ap11, ap12, ap13, ap14, ap15, ap16,
    ap17, ap18, ap19, ap20, ap21, ap22, ap23, ap24, ap25, ap26, a_ap, b_ap, c_ap, d_ap, ids_ap]
    return round_aprox



def printer(results, round):
    print('========================================================================')
    print('========================================================================')
    print('                            Approximations           ')
    print('------------------------------------------------------------------------')
    print('                               Round: {}'.format(round))
    print('------------------------------------------------------------------------')
    print('A ^ B:           {}'.format(results[0]))
    print('B ^ C:           {}'.format(results[1]))
    print('C ^ D:           {}'.format(results[2]))
    print('A ^ C:           {}'.format(results[3]))
    print('B ^ D:           {}'.format(results[4]))
    print('A ^ D:           {}'.format(results[5]))
    print('IDS ^ A:         {}'.format(results[6]))
    print('IDS ^ B:         {}'.format(results[7]))
    print('IDS ^ C:         {}'.format(results[8]))
    print('IDS ^ D:         {}'.format(results[9]))
    print('A ^ B ^ C:       {}'.format(results[10]))
    print('A ^ B ^ D:       {}'.format(results[11]))
    print('A ^ B ^ IDS:     {}'.format(results[12]))
    print('A ^ C ^ D:       {}'.format(results[13]))
    print('A ^ C ^ IDS:     {}'.format(results[14]))
    print('A ^ D ^ IDS:     {}'.format(results[15]))
    print('B ^ C ^ D:       {}'.format(results[16]))
    print('B ^ D ^ IDS:     {}'.format(results[17]))
    print('B ^ C ^ IDS:     {}'.format(results[18]))
    print('C ^ D ^ IDS:     {}'.format(results[19]))
    print('A ^ B ^ C ^ D:   {}'.format(results[20]))
    print('A ^ B ^ C ^ IDS: {}'.format(results[21]))
    print('A ^ B ^ D ^ IDS: {}'.format(results[22]))
    print('A ^ C ^ D ^ IDS: {}'.format(results[23]))
    print('B ^ C ^ D ^ IDS: {}'.format(results[24]))
    print('A ^ B ^ C ^ D ^ IDS: {}'.format(results[25]))
    print('A:               {}'.format(results[26]))
    print('B:               {}'.format(results[27]))
    print('C:               {}'.format(results[28]))
    print('D:               {}'.format(results[29]))
    print('IDS:             {}'.format(results[30]))

def convertToBitChain(num):
    M = 96
    chain = [0] * 96
    i = 0
    while i < M:
        chain[M - 1 - i] += num % 2
        i += 1
        num = num >> 1
    return chain

def accumulate_current(values):
    acum_result = []
    for i in range(0, 96):
        temp = 0
        for round in values:
            temp += round[i]
        acum = temp / (len(values) / 2)
        if acum > 1: acum = 1
        acum_result.append(str(math.trunc(acum)))
    return ''.join(acum_result)

def hamming_dist(approximations, ID):
    distances = []
    for approx in approximations:
        distances.append(ID.hamming_distance(BitVector(bitstring=approx)))
