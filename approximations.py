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
    ap17, ap18, ap19, ap20, ap21, ap22, ap23, ap24, ap25, ap26]
    print(round_aprox)
    return round_aprox
