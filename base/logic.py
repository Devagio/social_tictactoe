def check(bs):
    if bs[0] == bs[1] == bs[2] != '.': return bs[0]
    if bs[3] == bs[4] == bs[5] != '.': return bs[3]
    if bs[6] == bs[7] == bs[8] != '.': return bs[6]
    if bs[0] == bs[4] == bs[8] != '.': return bs[4]
    if bs[6] == bs[4] == bs[2] != '.': return bs[4]
    if bs[0] == bs[3] == bs[6] != '.': return bs[0]
    if bs[1] == bs[4] == bs[7] != '.': return bs[1]
    if bs[2] == bs[5] == bs[8] != '.': return bs[2]
    if bs.count('.') == 0: return 'D'
    return None