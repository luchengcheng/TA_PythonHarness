import json
import utils
import pydicom


def readJsonFile(JsonFile):
    with open(JsonFile) as f:
        interestedFieldsDict = json.load(f)
    f.close()
    return interestedFieldsDict

'''
Method 'parseInterestedFieldsDict':
1. if tag which is in file 'InterestedFields' doesn't exist in DCM
2. if tag which is in file 'InterestedFields' exists in DCM,
    1) Tag is basic element
    2) Tag is sequence
'''
def parseInterestedFieldsDict(dict, DCMFile):
    keys = dict.keys()
    new_ChildItemsList = []
    for key in keys:
        index = 0
        if utils.tagExist(DCMFile, key):
            if not utils.tagVrIsSQ(DCMFile, key):
                '''
                It's basic element. 
                Example: "0010,0020": {"vr": "LO","keyword":"PatientID"},
                '''
                formatTag = "0x" + key.replace(",", "")  # formatTag should be 0x300A0070.
                tagValue = utils.getValueFromDCMTag(DCMFile, formatTag)
                dict = utils.addKeyValueToDict(dict, key,
                                               utils.addKeyValueToDict(dict.get(key), "valueInDCM", tagValue))
            else:
                sq = utils.getSequenceFromKey(DCMFile, key)
                '''
                It's a sequence.
                Example: 
                "300A,0010": {
                        "vr": "SQ",
                        "keyword":"DoseReferenceSequence",
                        "element": [{
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        },
                        {
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        }]
                    }
                '''
                childDict = dict.get(key)
                '''
                 @ childDict
                 {
                        "vr": "SQ",
                        "keyword":"DoseReferenceSequence",
                        "element": [{
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        },
                        {
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        }]
                    }
                '''
                childItemsList = childDict.get("element")
                '''
                @childItemsList
                [{
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        },
                        {
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        }]
                '''
                for childItemDict in childItemsList:
                    '''
                    @childItemDict
                    {
                            "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                        }
                    '''
                    childItem_Keys = childItemDict.keys()
                    for childItem_Key in childItem_Keys:
                        '''
                        @childItem_Key
                        300A,0026
                        '''
                        if utils.tagExist(DCMFile, childItem_Key):
                            if not utils.tagVrIsSQ(DCMFile, childItem_Key):
                                tagValue = utils.getValueFromSequence(sq, index, childItem_Key)
                                temp_dict0 = utils.addKeyValueToDict(childItemDict.get(childItem_Key), "valueInDCM",
                                                                     tagValue)
                                temp_dict1 = utils.addKeyValueToDict(childItemDict, childItem_Key,
                                                                     temp_dict0)
                                '''
                                @temp_dict1
                                {
                                    "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose", "ValueInDCM":"2.2"}
                                     }
                                '''
                                new_ChildItemsList.append(temp_dict1)
                                '''
                                @childItemsList
                                [{
                                        "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose", "ValueInDCM":"2.2"}
                                    },
                                    {
                                        "300A,0026": {"vr": "DS","keyword":"TargetPrescriptionDose"}
                                    }]
                                '''
                    index = index + 1
                    temp_dict2 = utils.addKeyValueToDict(dict.get(key), 'element', new_ChildItemsList)
                    new_ChildItemsList = []

            dict = utils.addKeyValueToDict(dict, key, temp_dict2)
    return dict


def main():
    JsonFile = "C:\\Users\\clue09776\\PycharmProjects\\pythonProject\\interestedFields.json"
    DCMFile = "C:\\Users\\clue09776\\PycharmProjects\\pythonProject\\test.dcm"
    NewJsonFile = "C:\\Users\\clue09776\\PycharmProjects\\pythonProject\\interestedFieldsWithData.json"
    interestedDict = readJsonFile(JsonFile)
    interestedDictWithDCMData = parseInterestedFieldsDict(interestedDict, DCMFile)
    utils.JsonFileWithData(interestedDictWithDCMData, NewJsonFile)


if __name__ == '__main__':
    main()
