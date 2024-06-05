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


def parseBirdLogic(file, _dataToAppend):
    with open(file, 'r') as _data:
        data = _data.read()
        data = data.split('\n')

        current_sequence = ""
        sequences = []
        jumps = []
        jumpSet = set()
        
        pattern = r"\[sequence(\d+)\]"
        section = ""
        stateName = ""
        for line in data:
            sequence = re.findall(pattern, line)
            if(sequence):
                currentSequenceNumber = int(sequence[0])
                stateName = line
                # state = (line, sequence)
                section = "sequence"
            if(line == "[general]"):
                section = "general"
            elif(line == "[idle]"):
                section = "idle"
            elif(line == "[active1]"):
                section = "active"
            elif(line == "[active2]"):
                section = "active"
            elif(line == "[jump]"):
                section = "jump"
            elif(line.startswith("#")):
                continue
            # elif(line.startswith(r'\r\n') and (section != "jump")):
            #     section = ""
            elif(line == "" and (section != "jump")):
                section = ""

            if(section == "sequence"):
                clip = line.split(" ")
                if(len(clip) > 2):
                    clipName = clip[0]
                    startTime = clip[1]
                    endTime = clip[2]
                    parentState = stateName


                    position = currentSequenceNumber

                    animation = ({'name':clipName, 
                                'startTime':startTime, 
                                'endTime':endTime,
                                'transitionFromParent': None,
                                'parentAnimation' : None,
                                'parentState':parentState,
                                'position':position,
                                'targetPosition':None,
                                'isEarlyExit':False,
                                'isActive':None})
                    # print(animation)
                    sequences.append(animation)

            if(section == "jump"):
                if(line.startswith('#') or not line.strip()):
                    if(len(jumpSet) > 0):
                        jumps.append(jumpSet)
                        jumpSet = set()
                    
                else:
                    clip = line.split(' ')
                    if(len(clip) > 1):
                       clipIs = clip[0]
                       clipCanjumpTo = clip[1]
                       jumpSet.add((clipIs, clipCanjumpTo))
                    else:
                        continue
            # print(jumps)
            
        # for jump in states:
        #     for stateComp in states:
        #         if(stateComp == state):
        #             states.remove(state)
        # _jumpSet = list(set(frozenset(item) for item in jumps))

        animationsAndJumps = []
        for animation in sequences:
            for _jumps in jumps:
                if(len(_jumps) > 1):
                    rootAnim, fisrJump = list(_jumps)[0]
                    if(animation['name'] == rootAnim):
                        animationsAndJumps.append((animation, _jumps))
        
        # print(animationsAndJumps)
        for anims_jumps in animationsAndJumps:
            for comp_anims_jumps in animationsAndJumps:
                if()



            
        
        
        # for stateComp in states:
        #     for anim in stateComp:
        #         for clip in sequences:
        #             if(clip['name'] == anim):
        #                 print(state, anim)
        #                 # print(anim)

        # print(states)
                
                
                


            
        # json_data = json.dumps(sequences, indent=4)
        # print(json_data)


# def csv_to_json(sm_file, videoSM_file, json_file):
#     sm_data = []
#     videoSM_data = []
#     output_data = []
    
#     # Read the CSV file
#     with open(sm_file, 'r') as file1:
#         sm_reader = csv.DictReader(file1)
#         for row in sm_reader:
#             sm_data.append(row)
    
#     with open(videoSM_file, 'r') as file2:
#         videoSM_reader = csv.DictReader(file2)
#         for row in videoSM_reader:
#             videoSM_data.append(row)
    
#     for sm_anim in sm_data:
#         for vid_anim in videoSM_data:
#             if(vid_anim['Clip Name'] == sm_anim['Clip Name']):
#                 clipName = vid_anim['Clip Name']
#                 startTime = int(vid_anim['From'])
#                 endTime = int(vid_anim['To'])
#                 parentState = sm_anim['Parents']
#                 transitionTime = 0
            
#                 isEarlyExit = False
#                 if(len(parentState.split('/')) > 1):
#                     parentAnimation = parentState.split('/')[1]
#                     parentState = parentState.split('/')[0]
#                     isEarlyExit = True

#                     parentStateSM = getDataFromClipName(parentAnimation,sm_data)
#                     parentStateVid = getDataFromClipName(parentAnimation,videoSM_data)
#                     stateSM = getDataFromClipName(clipName,sm_data)
                    
#                     transitionOffset = int(stateSM['Transition Frame']) - int(parentStateSM['From'])
#                     transitionOffset *= 2
#                     transitionTime = int(parentStateVid['From']) + transitionOffset

#                 else:
#                     parentAnimation = "None"

                
#                 if(sm_anim['IsActive'] == "TRUE"):
#                     isActive = True
#                 else: isActive = False

#                 position, targetPosition = calcPosition(parentState)
                
#                 output_data.append({'name':clipName, 
#                                     'startTime':startTime, 
#                                     'endTime':endTime,
#                                     'transitionFromParent': transitionTime,
#                                     'parentAnimation' : parentAnimation,
#                                     'parentState':parentState,
#                                     'position':position,
#                                     'targetPosition':targetPosition,
#                                     'isEarlyExit':isEarlyExit,
#                                     'isActive':isActive})
#     # Write the data to a JSON file
#     with open(json_file, 'w') as file:
#         json.dump(output_data, file, indent=4)
        
        




    
        
    
# Replace 'inputcsv' and 'output.json' with the actual file names
parsedBirdFile = []
parseBirdLogic("280223_Atlas_0_0_5.txt", parsedBirdFile)

# csv_to_json('SM.csv', 'Video_SM.csv', 'video_states.json')