from BitVector import BitVector

def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def calculate_approximations(batch, ID):
    A = batch["A"]
    B = batch["B"]
    C = batch["C"]
    D = batch["D"]
    IDS = batch["IDS"]
    a_ap = ID.hamming_distance(BitVector(bitstring=(A)))
    b_ap = ID.hamming_distance(BitVector(bitstring=(B)))
    c_ap = ID.hamming_distance(BitVector(bitstring=(C)))
    d_ap = ID.hamming_distance(BitVector(bitstring=(D)))
    ids_ap = ID.hamming_distance(BitVector(bitstring=(IDS)))
    ap1 = ID.hamming_distance(BitVector(bitstring=(A ^ B)))
    ap2 = ID.hamming_distance(BitVector(bitstring=(B ^ C)))
    ap3 = ID.hamming_distance(BitVector(bitstring=(C ^ D)))
    ap4 = ID.hamming_distance(BitVector(bitstring=(A ^ C)))
    ap5 = ID.hamming_distance(BitVector(bitstring=(B ^ D)))
    ap6 = ID.hamming_distance(BitVector(bitstring=(A ^ D)))
    ap7 = ID.hamming_distance(BitVector(bitstring=(IDS ^ A)))
    ap8 = ID.hamming_distance(BitVector(bitstring=(IDS ^ B)))
    ap9 = ID.hamming_distance(BitVector(bitstring=(IDS ^ C)))
    ap10 = ID.hamming_distance(BitVector(bitstring=(IDS ^ D)))
    ap11 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ C)))
    ap12 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ D)))
    ap13 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ IDS)))
    ap14 = ID.hamming_distance(BitVector(bitstring=(A ^ C ^ D)))
    ap15 = ID.hamming_distance(BitVector(bitstring=(A ^ C ^ IDS)))
    ap16 = ID.hamming_distance(BitVector(bitstring=(A ^ D ^ IDS)))
    ap17 = ID.hamming_distance(BitVector(bitstring=(B ^ C ^ D)))
    ap18 = ID.hamming_distance(BitVector(bitstring=(B ^ D ^ IDS)))
    ap19 = ID.hamming_distance(BitVector(bitstring=(B ^ C ^ IDS)))
    ap20 = ID.hamming_distance(BitVector(bitstring=(C ^ D ^ IDS)))
    ap21 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ C ^ D)))
    ap22 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ C ^ IDS)))
    ap23 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ D ^ IDS)))
    ap24 = ID.hamming_distance(BitVector(bitstring=(A ^ C ^ D ^ IDS)))
    ap25 = ID.hamming_distance(BitVector(bitstring=(B ^ C ^ D ^ IDS)))
    ap26 = ID.hamming_distance(BitVector(bitstring=(A ^ B ^ C ^ D ^ IDS)))
    round_aprox = [ap1, ap2, ap2, ap3, ap4, ap5, ap6, ap7, ap8, ap9, ap10, ap11, ap12, ap13, ap14, ap15, ap16,
    ap17, ap18, ap19, ap20, ap21, ap22, ap23, ap24, ap25, ap26, a_ap, b_ap, c_ap, d_ap, ids_ap]
    return round_aprox



def printer(results, round):
    print('====================================')
    print('====================================')
    print('           Approximations           ')
    print('------------------------------------')
    print('             Round: {}'.format(round))
    print('------------------------------------')
    print('A ^ B:       {} +- {}'.format(results[0][0], results[0][1]))
    print('B ^ C:       {} +- {}'.format(results[1][0], results[1][1]))
    print('C ^ D:       {} +- {}'.format(results[2][0], results[2][1]))
    print('A ^ C:       {} +- {}'.format(results[3][0], results[3][1]))
    print('B ^ D:       {} +- {}'.format(results[4][0], results[4][1]))
    print('A ^ D:       {} +- {}'.format(results[5][0], results[5][1]))
    print('IDS ^ A:     {} +- {}'.format(results[6][0], results[6][1]))
    print('IDS ^ B:     {} +- {}'.format(results[7][0], results[7][1]))
    print('IDS ^ C:     {} +- {}'.format(results[8][0], results[8][1]))
    print('IDS ^ D:     {} +- {}'.format(results[9][0], results[9][1]))
    print('A ^ B ^ C:   {} +- {}'.format(results[10][0], results[10][1]))
    print('A ^ B ^ D:   {} +- {}'.format(results[11][0], results[11][1]))
    print('A ^ B ^ IDS: {} +- {}'.format(results[12][0], results[12][1]))
    print('A ^ C ^ D:   {} +- {}'.format(results[13][0], results[13][1]))
    print('A ^ C ^ IDS: {} +- {}'.format(results[14][0], results[14][1]))
    print('A ^ D ^ IDS: {} +- {}'.format(results[15][0], results[15][1]))
    print('B ^ C ^ D:   {} +- {}'.format(results[16][0], results[16][1]))
    print('B ^ D ^ IDS: {} +- {}'.format(results[17][0], results[17][1]))
    print('B ^ C ^ IDS: {} +- {}'.format(results[18][0], results[18][1]))
    print('C ^ D ^ IDS: {} +- {}'.format(results[19][0], results[19][1]))
    print('A ^ B ^ C ^ D: {} +- {}'.format(results[20][0], results[20][1]))
    print('A ^ B ^ C ^ IDS: {} +- {}'.format(results[21][0], results[21][1]))
    print('A ^ B ^ D ^ IDS: {} +- {}'.format(results[22][0], results[22][1]))
    print('A ^ C ^ D ^ IDS: {} +- {}'.format(results[23][0], results[23][1]))
    print('B ^ C ^ D ^ IDS: {} +- {}'.format(results[24][0], results[24][1]))
    print('A: {} +- {}'.format(results[25][0], results[25][1]))
    print('B: {} +- {}'.format(results[26][0], results[26][1]))
    print('C: {} +- {}'.format(results[27][0], results[27][1]))
    print('D: {} +- {}'.format(results[28][0], results[28][1]))
    print('IDS: {} +- {}'.format(results[29][0], results[29][1]))
