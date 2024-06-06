import json
import re




def combineSameValuesInListIsListContainsSameValues(inLists):
    result = []
    resultOutOut = []
    for k in inLists:
        resultComp = k
        for m in inLists:
            isIn = False
            for t in m:
                if(t in k):
                    isIn = True
                    break
            if(isIn):
                in_first = set(k)
                in_second = set(m)
                in_second_but_not_in_first = in_second - in_first
                result = k + list(in_second_but_not_in_first)
                if(len(result) > len(resultComp)):
                    resultComp = result

        uniques = list(set(resultComp))
        sortedResult = tuple(sorted(uniques))
        if(sortedResult not in resultOutOut):
            resultOutOut.append(sortedResult)
    return resultOutOut


def parseBirdLogic(file):
    with open(file, 'r') as _data:
        data = _data.read()
        data = data.split('\n')

        generals = []
        
        sequencePattern = r"\[sequence(\d+)\]"
        # sequence = 
        sequences = []  

        activePattern = r"\[active(\d+)\]"
        active = []
        actives = []

        idles = []
        
        jumps = []

        for line in data:
            
            if(len(re.findall(sequencePattern, line))):
                section = "sequence"
                sequenceNumber = re.findall(sequencePattern, line)
                continue
            
            elif(len(re.findall(activePattern, line))):
                section = "active"
                activeNumber = re.findall(activePattern, line)
                continue
            
            elif(line == "[general]"):
                section = "general"
                continue
            elif(line == "[idle]"):
                section = "idle"
                continue
            elif(line == "[active1]"):
                section = "active"
                continue
            elif(line == "[active2]"):
                section = "active"
                continue
            elif(line == "[jump]"):
                section = "jump"
                continue
            elif(line.startswith("#")):
                continue
            elif(line == ""):
                continue


            if(section == "general"):
                generals.append(line)

            elif(section == "idle"):
                idles.append(line)
                
            elif(section == "sequence"):
                sequences.append(re.sub(r'\]$', '', line))  #remove trailing "]" from extractor

            elif(section == "active"):
                actives.append(line)

            elif(section == "jump"):
                jumps.append(line)
    


        # sequences = list(set(sequences))
        sequencesParsed = []
        for sequence in sequences:
            name, startTime, endTime = sequence.split(' ')
            chapter, clip = name.split('.')
            sequence = [sequence]
            if((name) and (startTime) and (endTime)):
                jumpsInSequence = []
                for jump in jumps:
                    if(len(jump.split(' ')) > 2):
                        nameComp, jumpName, _= jump.split(' ')    #thers a trailing " " on some files
                    else:
                        nameComp, jumpName = jump.split(' ')
                    if(nameComp == name):
                        jumpsInSequence.append(jumpName)

                sequence.append(jumpsInSequence)

                isActive = False
                for active in actives:
                    if(active == chapter):
                        isActive = True
                sequence.append(isActive)
            sequencesParsed.append(sequence)
        

        jumps = []
        for _sequence in sequencesParsed:
            jumps.append(_sequence[1])
        
        stateList = combineSameValuesInListIsListContainsSameValues(jumps)

        animations = []
        for _sequence in sequencesParsed:
            clipName, startTime, endTime = _sequence[0].split(' ')
            jumps = _sequence[1]
            isActive = _sequence[2]
            position = -1
            targetPosition = -1

            for i in range(len(stateList)):
                if(clipName in stateList[i]):
                    position = i
                
                for n in jumps:
                    if(n in stateList[i]):
                        targetPosition = i


            animation = ({'name':clipName, 
                        'startTime':startTime, 
                        'endTime':endTime,
                        'transitionFromParent': None,
                        'parentAnimation' : None,
                        'parentState':stateList[position][0],
                        'position':position,
                        'targetPosition':targetPosition,
                        'isEarlyExit':False,
                        'isActive':isActive})
            
            animations.append(animation)
    
    # Write the data to a JSON file
    json_file = "video_states.json"
    with open(json_file, 'w') as file:
        json.dump(animations, file, indent=4)
        
parseBirdLogic("280223_Atlas_0_0_5.txt")
        