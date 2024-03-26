import pydicom
import os


def tagExist(dcmfile, keyword):
    tag_list = []
    ds = pydicom.dcmread(dcmfile)
    for elem in ds.elements():
        tag_list.append(str(elem.tag).replace(" ", ""))
    if keyword.lower() in tag_list:
        return True
    else:
        return False


def getValuefromDCMTag(dcmfile, keyword):
    ds = pydicom.dcmread(dcmfile)
    elem = ds[keyword]
    return str(elem.value)


'''
Step1: get dcm value and save to variable #text
Step2: format #text
Step3: write #text to new txt file if there is no new txt file
'''


def saveDCMValueToTxt(txtfile, dcmfile, txtfile_dataInDCM):
    with open(txtfile, "r+") as f:
        text = f.read()
        lines = text.split("\n")
        for line in lines[1:]:
            wordList = line.split(";")
            tag = wordList[0]
            keyword = wordList[1]
            if tagExist(dcmfile, tag):
                formatTag = "0x" + tag[1:-1].replace(",", "")  # change (0010,0010) to 0x00100010
                value = getValuefromDCMTag(dcmfile, formatTag)
                if value =="":
                    text = text.replace(keyword + ";", keyword + ";empty")
                else:
                    text = text.replace(keyword+ ";" , keyword + ";" + str(value))
            else:
                text = text.replace(keyword+ ";" , keyword + ";" + "TagNotExist")
            # else:
            #     print()
    firstLine = "        Tag;                              Keyword;                           ValueInDCM;                            ValueInDB;                            ValueInUI;"
    wordList = text.split(";")
    newText = []
    for word in wordList[5:]:
        word = word + ";"
        word = word.rjust(38, " ")
        newText.append(word)
    finalText = firstLine + "".join(newText)
    f.close()
    print(text)

    if os.path.exists(txtfile_dataInDCM):
        os.remove(txtfile_dataInDCM)
    with open(txtfile_dataInDCM, "w+") as f:
        f.write(finalText)
    f.close()


def main():
    # print(os.getcwd())
    txtFile = "C:\\Users\\clue09776\\PycharmProjects\\pythonProject\\dataMatch.txt"
    dcmFile = "C:\\Users\\clue09776\\PycharmProjects\\pythonProject\\test.dcm"
    txtFile_valueInDCM = "C:\\Users\\clue09776\\PycharmProjects\\pythonProject\\dataMatch_valueInDCM.txt"
    saveDCMValueToTxt(txtFile, dcmFile, txtFile_valueInDCM)


if __name__ == '__main__':
    main()
