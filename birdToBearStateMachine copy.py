import csv
import json
import re
from itertools import combinations
from collections import defaultdict

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
    unique_lists = []
    indexList = []
    index = 0
    for sublist in list_of_lists:
        sorted_tuple = tuple(sorted(sublist))
        if(sorted_tuple not in seen):
            seen.add(sorted_tuple)
            unique_lists.append(sublist)
            indexList.append(index)
        index +=1
    return unique_lists, indexList

def find_unique_values(pair):
    set1, set2 = set(pair[0]), set(pair[1])
    common = set1 & set2
    unique1 = set1 - common
    unique2 = set2 - common
    return list(unique1), list(unique2)

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

def removeCombinedDuplicatesInListOfLists(inLists):
    result = []
    resultOut = []
    for n in inLists:
        result = []
        for p in inLists:
            hit = False
            for j in p:
                if(j in n):
                    hit = True
            if(hit):
                resultOut.append(result)
    return resultOut


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

                sequence.append(jumpsInSequence)

                isActive = False
                for active in actives:
                    if(active == chapter):
                        isActive = True
                sequence.append(isActive)
            sequencesParsed.append(sequence)
        

        jumps = []
        for _sequence in sequencesParsed:
            name, start, end = _sequence[0].split(' ')
            jumps.append(_sequence[1])
        
        states = combineSameValuesInListIsListContainsSameValues(jumps)
        # pop = removeCombinedDuplicatesInListOfLists(pop)

        
        for n in states:
            print(n)
        

parsedBirdFile = []
parseBirdLogic("280223_Atlas_0_0_5.txt", parsedBirdFile)
        # pop = remove_duplicates
            









        # jumpsNotIncludingSelfList, _ = remove_duplicates(jumpsNotIncludingSelfList)
        # jumpsIncludingSelfListCopy = jumpsIncludingSelfList.copy() #remove self from ordered list to extract transition
        # jumpsIncludingSelfList, _indexes = remove_duplicates(jumpsIncludingSelfList)    
        

        # for n in range(len(jumpsIncludingSelfListCopy)):
        #     if(n in _indexes):
        #         jumpsIncludingSelfListCopy[n] = []


        # stateList = []
        # for i in jumpsIncludingSelfListCopy:
        #     for j in jumpsNotIncludingSelfList:
        #         listComp = i[:-1] #remove self from list
        #         if(listComp == j):
        #             selfT = i[-1]
        #             # j.append(selfT)
        #             stateList.append(j) #this should find common jumps i.e position
        
        # stateList, _ = remove_duplicates(stateList)

        # stateListNarrowed = []
        # transitionListNarrowed = []
        # for s in stateList:
        #     print(s)
        
        
        #     _stateList = []
        #     _transitionList = []
        #     for findTransitions in stateList:
        #         if(findTransitions != s):
        #             # _transitionList = []
        #             isMatchingSet = False
        #             for transition in findTransitions:
        #                 if(transition in s):
        #                     isMatchingSet = True

        #             isFullState = True
        #             if(isMatchingSet):
        #                 _transitionList = []
        #                 for transition in findTransitions:
        #                     if(transition not in s):
        #                         isFullState = False
        #                         _transitionList.append(transition)
        #                 if(isFullState):
        #                     stateListNarrowed.append(s)

                
        #     if(len(_transitionList) > 0):
        #         transitionListNarrowed.append(_transitionList)
    

        # for s in stateListNarrowed:
        #     print(s)
        # print("^^StateList")

        # for i in transitionListNarrowed:
        #     print(i)
        # print("^^Transitisons")
        
            


        # for _sequence in sequencesParsed:
        #     name, start, end = _sequence[0].split(' ')
        # # Convert each list to a set
        # sets = [set(lst) for lst in all_lists]

        # # Find all unique elements
        # all_unique_elements = set.union(*sets)

        # # Find the common elements across all sets
        # common_elements = set.intersection(*sets)

        # # Find unique elements in each set
        # unique_elements_in_each_list = [list(s - common_elements) for s in sets]

        # # Print the unique elements in each list
        # for i, unique_elements in enumerate(unique_elements_in_each_list):


            

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


        # pairs_with_common_elements = []

        # for (list1, list2) in combinations(stateList, 2):
        #     common_elements = set(list1) & set(list2)
        #     if common_elements:
        #         pairs_with_common_elements.append((list1, list2, common_elements))

        # # Process each pair to find unique values
        # result = []

        # for list1, list2, common_elements in pairs_with_common_elements:
        #     if len(list1) >= len(list2):
        #         longest_list, other_list = list1, list2
        #     else:
        #         longest_list, other_list = list2, list1

        #     unique_in_longest = set(longest_list) - common_elements
        #     unique_in_other = set(other_list) - common_elements

        #     result.append((longest_list, unique_in_longest, unique_in_other))

        # # Output the result
        # for longest, unique_longest, unique_other in result:
        #     print(f"Longest list: {longest}")
        #     print(f"Unique values in longest list: {unique_longest}")
        #     print(f"Unique values in other list: {unique_other}")
        #     print()



        # for p in stateList:
        #     print(p)
    #     print(i)
    


                


# Replace 'inputcsv' and 'output.json' with the actual file names

# csv_to_json('SM.csv', 'Video_SM.csv', 'video_states.json')