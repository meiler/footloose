# 4_instruments.py


def is_bass(track):
    """ Checks if it only plays on pitch at a time and the average pitch is deep.
    """
    if any(track.sum(axis=1) > 1):
        return False
    elif np.average(np.nonzero(track)[0]) > 47:
        return False #if the average pitch is below 47, then it may be the bass
    else:
        return True


def is_harmony(track):
    """ Checks if it mostly plays several pitch at a time.
    """
    instrument_present = [nodes for nodes in track.sum(axis=1) if nodes > 0]
    harmonies = [nodes for nodes in instrument_present if nodes > 1]

    harmony_percentage = len(harmonies) / len(instrument_present)

    if harmony_percentage < 0.9: # often (90 percent) two nodes at the same time        
        return False
    else:
        return True
    


def is_lead(track):
    # the lead is mostly 1 pitch at a time
    # and it is above 47 on average
    """ Checks if it mostly plays one pitch at a time and the average pitch is high.
    """
    instrument_present = [nodes for nodes in track.sum(axis=1) if nodes > 0]
    harmonies = [nodes for nodes in instrument_present if nodes > 1]

    harmony_percentage = len(harmonies) / len(instrument_present)

    if harmony_percentage > 0.1 : # often (90 percent) two nodes at the same time        
        return False
    elif np.average(np.nonzero(track)[0]) < 47:
        return False
    else:
        return True





matrix_a = np.array([[ 0.,  1,  0.,  0.,  0.],
       [ 0.,  1.,  1,  1,  0.],
       [ 0.,  0.,  1,  1.,  0.]])


#playes nodes at the same time
print(is_bass(matrix_a) == False)
print(is_harmony(matrix_a) == False)
print(is_lead(matrix_a) == False)




    


