# 4_instruments.py


def is_drums(track):


def is_bass(track):
    if any(track.sum(axis=1) > 1):
        return False
    elif track.sum()/len(np.nonzero(track)[0]) > 47:
        return False #if the average pitch is below 47, then it may be the bass
    else:
        return True


def is_harmony(track):
    instument_present = [number for number in track.sum(axis=1) if number > 0]
    harmonies = [number for number in instument_present.sum(axis=1) if number > 1]
    
    harmony_percentage = float(len(harmonies)) / float(len(instument_present))
    
    if harmony_percentage < 0.9: # often (90 percent) two nodes at the same time        
        return False
    else:
        return True    
    


def is_lead(track):
    # the lead is mostly 1 pitch at a time
    # and it is above 47 on average
    
    instument_present = [number for number in track.sum(axis=1) if number > 0]
    harmonies = [number for number in instument_present.sum(axis=1) if number > 1]
    
    harmony_percentage = float(len(harmonies)) / float(len(instument_present))    
    
    if harmony_percentage > 0.1 : # often (90 percent) two nodes at the same time        
        return False
    elif track.sum()/len(np.nonzero(track)[0]) < 47:
        return False
    else:
        return True
