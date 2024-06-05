import csv
import json
import re

def calcPosition(_parentState):
    positions = {"Left":0, "Front":1, "Right":2}
    isEarlyExit = False
    if(len(_parentState.split('_')) > 1):
        currentPosition = _parentState.split('_')[0]
        targetPosition = _parentState.split('_')[1]
    else:
        currentPosition = _parentState
        targetPosition = _parentState
    position = positions.get(currentPosition)
    targetPosition = positions.get(targetPosition)

    return position, targetPosition

def getsequenceName(_seq):
    pass

def remove_duplicates(list_of_lists):
    seen = set()
    result = []
    for sublist in list_of_lists:
        unique_sublist = []
        for item in sublist:
            if item not in seen:
                unique_sublist.append(item)
                seen.add(item)
        result.append(unique_sublist)
    return result

def parseBirdLogic(file, _dataToAppend):
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

                # jumpsInSequence.append(name)
                # sequence.append(list(set(jumpsInSequence)))
                # jumpsInSequence.append(name)
                sequence.append(jumpsInSequence)

                isActive = False
                for active in actives:
                    if(active == chapter):
                        isActive = True
                sequence.append(isActive)
            sequencesParsed.append(sequence)
            # print(sequence)

        jumpsToComp = []
        _sequencesParsed = sequencesParsed.copy()
        position = 0
        for _sequence in sequencesParsed:
            jumpsChecked = set()
            name, startTime, endTime = sequence[0].split(' ')
            jumpsInSequence = _sequence[1]
            print(_sequence)
            for _sequenceComp in sequencesParsed:
                if(_sequenceComp != sequence):
                    _name, _startTime, _endTime = _sequenceComp[0].split(' ')
                    if(name in jumpsInSequence and name not in jumpsChecked):
                        for j in jumpsInSequence:
                            jumpsChecked.add(j)
                        position += 1
                        print(name, position)


            

        # groups = []
        # for n in jumpsToComp:
        #     for j in jumpsToComp:
        #         if(n[-1] in j):


            # print(n)
            # isInSet = True
        

        
        # for i in jumpsToComp_sorted:
        #     for j in jumpsToComp_sorted:
        #         if (i != j):

        #             # transitions = list(set(i) - set(j))
        #             if(len(transitions) < len(i)):
        #                 print(transitions)





    #common_jumps_to_compare = []
    #for sequence in sequencesParsed:
    #    name, startTime, endTime = sequence[0].split(' ')
    #    chapter, clip = name.split('.')
    #    if((name) and (startTime) and (endTime)):
    #        for sequenceComp in sequencesParsed:
    #            nameComp, startTimeComp, endTimeComp = sequenceComp[0].split(' ')
    #            chapterComp, clipComp = nameComp.split('.')
    #            if(nameComp != name):
    #                common_jumps = list(set(sequence[1]) & set(sequenceComp[1]))
    #                if(len(common_jumps) > 0):
    #                    # common_jumps_to_compare.append((name, nameComp, common_jumps))
    #                    common_jumps_to_compare.append(common_jumps)
    #                    # print(common_jumps)
    
    
    # unique_lists = set(tuple(lst) for lst in common_jumps_to_compare)
    # common_jumps_to_compare = [list(tpl) for tpl in unique_lists]
    
    # common_jumps_comp_list = []
    # for common_jump in common_jumps_to_compare:
    #     for common_jump_to_compare in common_jumps_to_compare:
    #         common_jumps_comp = list(set(common_jump) & set(common_jump_to_compare))
    #         if(len(common_jumps_comp) >= (len(common_jump) -1)):
    #             common_jumps_comp_list.append(common_jumps_comp)
    
    # unique_lists = set(tuple(lst) for lst in common_jumps_comp_list)
    # common_jumps_comp_list = [list(tpl) for tpl in unique_lists]

    # sorted_list_of_lists = sorted(common_jumps_comp_list, key=len)
    # for i in sorted_list_of_lists:
    #     print(i)
    


                


# Replace 'inputcsv' and 'output.json' with the actual file names
parsedBirdFile = []
parseBirdLogic("280223_Atlas_0_0_5.txt", parsedBirdFile)

# csv_to_json('SM.csv', 'Video_SM.csv', 'video_states.json')