import argparse
import io
import os
import glob
import sys
import codecs

from os import path
from xmlHandler import xmlHandler



class altoProcessor:
    minimalNumberOfWordsInParagraph = 6

    content = ""
    globalAntallOver98 = 0
    globalAntallOrd = 0
    globalSumWC = 0
    altoObjectDir=""
    rootNodeName = None
    handler = None

    def __init__(self, altoObjectDir,rootNodeName=None):
        self.altoObjectDir=altoObjectDir
        if rootNodeName == None:
            self.rootNodeName = "alto"
        else:
            self.rootNodeName = rootNodeName
        self.content = ""
        self.globalSumWC = 0
        self.globalAntallOrd = 0
        self.handler = None
        self.globalAntallOver98 = 0
        self.minimalNumberOfWordsInParagraph = 6

    def __init__(self):
        self.altoObjectDir=""
        self.rootNodeName = "alto"
        self.content = ""
        self.globalSumWC = 0
        self.globalAntallOrd = 0
        self.handler = None
        self.globalAntallOver98 = 0
        self.minimalNumberOfWordsInParagraph = 6

    def findBookTextInTextBlocks(self,urn, bList):

        for block in bList:
            searchString = "Layout/Page/PrintSpace/TextBlock[@ID='" + block + "']"
            res = self.handler.findAllNodes(searchString)
            for i in res:
                res3 = self.handler.findInSub(i, "TextLine/String")
                localstr = ""
                sumwc = 0
                antallOver98 = 0


                for k in res3:
                    if 'SUBS_TYPE' not in k.attrib:
                        localstr += k.attrib['CONTENT'].strip()
                        localwc = float(k.attrib['WC'].strip())
                        sumwc += localwc
                        if (len(res3) >= self.minimalNumberOfWordsInParagraph):
                            self.globalSumWC += localwc
                            self.globalAntallOrd += 1
                        localstr += " "
                        if (localwc >= 0.98):
                            antallOver98 += 1
                            self.globalAntallOver98 += 1


                    elif 'SUBS_TYPE' in k.attrib and k.attrib['SUBS_TYPE'].strip() == 'HypPart2':
                        localstr += k.attrib['SUBS_CONTENT'].strip()
                        localwc = float(k.attrib['WC'].strip())
                        sumwc += localwc

                        if (len(res3) >= self.minimalNumberOfWordsInParagraph):
                            self.globalSumWC += localwc
                            self.globalAntallOrd += 1
                        localstr += " "
                        if (localwc >= 0.98):
                            antallOver98 += 1
                            self.globalAntallOver98 += 1

                    elif 'SUBS_TYPE' in k.attrib and k.attrib['SUBS_TYPE'].strip() == 'HypPart1':
                            localwc = float(k.attrib['WC'].strip())
                            sumwc += localwc
                            if (len(res3) >= self.minimalNumberOfWordsInParagraph):
                                self.globalSumWC += localwc
                                self.globalAntallOrd += 1
                            if (localwc >= 0.98):
                                antallOver98 += 1
                                self.globalAntallOver98 += 1

            if (len(res3) > 0):
                self.content += urn + "_" + block + "_" + str(round(sumwc / len(res3), 2)) + "\n"
                self.content += localstr + "\n"
                # globalAntallOrd += 1
                # print(urn + "_" + block + "_" + str(round(antallOver98/len(res3),2)) )
                # print(localstr)
                # print("\n")

    def FindAllTextBlocksInBook(self,filen, urn):
        blockList = []
        self.handler = xmlHandler(inputXmlFile=filen, rootNodeName="alto")
        blockResult = self.handler.findAllNodes("Layout/Page/PrintSpace/TextBlock")
        for block in blockResult:
            blockList.append(block.attrib['ID'])
        self.findBookTextInTextBlocks(urn, blockList)



    def ReadBook(self,altoObjectDir):
        self.altoObjectDir=altoObjectDir
        self.content = ""
        self.globalSumWC = 0
        self.globalAntallOrd = 0
        self.handler = None
        self.globalAntallOver98 = 0
        infiles = sorted(glob.glob(self.altoObjectDir + '/digibok_[0-9]*_[0-9]*.xml'))
        currentUrn = infiles[0].split('/')[-1].split('_')[0] + "_" + infiles[0].split('/')[-1].split('_')[1]
        for i in infiles:
            self.FindAllTextBlocksInBook(i, currentUrn)
        print(currentUrn + "_" + str(round(self.globalSumWC /self.globalAntallOrd, 2)))
        print(self.content)



