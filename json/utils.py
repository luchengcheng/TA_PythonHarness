import json
import pydicom
import os


def tagExist(dcmfile, tag):
    tag_list = []
    ds = pydicom.dcmread(dcmfile)
    for elem in ds.elements():
        if pydicom.datadict.dictionary_VR(elem.tag) != 'SQ':
            tag_list.append(str(elem.tag).replace(" ", "").replace("(", "").replace(")", ""))
        else:
            tag_list.append(str(elem.tag).replace(" ", "").replace("(", "").replace(")", ""))
            sq = pydicom.values.convert_SQ(elem.value, True, True)
            sqList = sq._list
            for eachItem in sqList:
                for basicElem in eachItem:  # list[0] is ds
                    tag_list.append(str(basicElem.tag).replace(" ", "").replace("(", "").replace(")", ""))
    if tag.lower() in tag_list:
        return True
    else:
        return False


def tagVrIsSQ(dcmFile, tag):
    ds = pydicom.dcmread(dcmFile)
    for elem in ds.elements():
        if str(elem.tag).replace(" ", "").replace("(", "").replace(")", "") == tag.lower():
            if pydicom.datadict.dictionary_VR(elem.tag) == 'SQ':
                return True
            else:
                return False


def getValueFromDCMTag(DCMFile, formattedTag):
    ds = pydicom.dcmread(DCMFile)
    elem = ds[formattedTag]
    return str(elem.value)


def addKeyValueToDict(dict, key, value):
    dict[key] = value
    return dict


def JsonFileWithData(dict, NewJsonFile):
    if os.path.exists(NewJsonFile):
        os.remove(NewJsonFile)
    with open(NewJsonFile, "w+") as f:
        json.dump(dict, f, indent=4, sort_keys=True)
    f.close()


def getValueFromSequence(sq, index, tag):
    sqList = sq._list
    for eachItem in sqList[index]:
        if str(eachItem.tag).replace(" ","").replace("(","").replace(")","") == tag.lower():
            return eachItem.value
    return ''


def getSequenceFromKey(DCM, SeqTag):
    ds = pydicom.dcmread(DCM)
    sq = None
    for elem in ds.elements():
        if str(elem.tag).replace(" ","").replace(")","").replace("(","") == SeqTag.lower():
            sq = pydicom.values.convert_SQ(elem.value, True, True)
            return sq
    return sq

