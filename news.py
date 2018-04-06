import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import datetime
import pandas as pd
from random import choice
from collections import defaultdict
from nltk.corpus import stopwords
from datetime import datetime, timedelta
from random import *
import string
import nltk
from nltk.tokenize import TreebankWordTokenizer

#nltk.download('all')



# Function to generate date in required format

def DateFunctions(request):
    if request == 'Y':
        yesterday = datetime.now() - timedelta(days=1)
        return yesterday.strftime('%Y%m%d')
    else:
        return datetime.now().strftime('%Y%m%d')


# Function to generate Full file name in required format

def GenerateFileName(
    path,
    request,
    FileString,
    FileExt,
    ):

    fdate = DateFunctions(request)
    LinkFileName = FileString + fdate + '.' + FileExt
    LinkFileNameFull = os.path.join(path, LinkFileName)
    return LinkFileNameFull


# Function to Pull all the links and create a file
# File is used by nextday's process to identify Fresh News on that day

def CreateLinksFile(file):

    AllLinks = {}
    Cnt = 1
    url = 'http://tolivelugu.com/'
    resp = requests.get(url)
    if resp.status_code == 200:
        print 'Successfully opened the web page:--> {}'.format(url)

        # print 'The news Links are below :-\n'

        soup = BeautifulSoup(resp.text, 'html.parser')
        for j in set(soup.find_all('a', href=True, title=True)):
            if re.search('eruditesoft', str(j)) or re.search('/videos/'
                    , str(j)):
                pass
            else:

                AllLinks[j['href']] = Cnt
                Cnt += 1
        with open(file, 'w') as f:
            for key in AllLinks.keys():
                f.write(key + '\n')

        return AllLinks
    else:
        print 'Error'


# Function to identify Fresh news as on that day

def CompareAndGenDiff(CurrLinks, PrevFile,Dataset):
    
        if os.path.exists(PrevFile) and  Dataset <> 'ALL':
        
		    with open(PrevFile, 'r') as rf:
			    PrevLinks = rf.readlines()

		# print(PrevLinks)

		    for CurrLink in CurrLinks.keys():
			    CurrLink1 = str(CurrLink) + '\n'
			    if CurrLink1 in PrevLinks:
				    pass
			    else:
				    NewLinks.append(CurrLink)

		    return NewLinks
        else:
                print('Either previous day file not present or dataset was set to ALL')
                return list(CurrLinks.keys())
			
			
	    


# Function to read content from the link provided

def ReadNews(link):
    lresp = requests.get(link)
    if lresp.status_code == 200:
        print 'Successfully opened the web page:-->{}'.format(link)
        #print 'Content Below:-\n'
        Csoup = BeautifulSoup(lresp.text, 'html.parser')

        # Csoup=Csoup.encode('utf-8')
        # txtFile=str(filename)+'.txt'
        # fpath = os.path.join(path, txtFile)
        # f = open(fpath, 'w')
        # f.write((Csoup.prettify()))
        # f.close()

        # print link

        for j in Csoup.find_all('div', attrs={'class': 'desc_row'}):
            if re.search('eruditesoft', str(j)):
                pass
            else:
                text = j.find_all(text=True)
                return text  # .encode('utf-8')
    else:
        print 'Error'


# Function to Generate WORD COUNT exclduing stop words

def GetWordCount(data):
    stop_words = set(stopwords.words('english'))

    words = []
    wordcount = defaultdict(int)
    for i in data:
        if i == '\n':
            continue
        else:
            #i = i.encode('utf-8')
            words = i.split(' ')

            # print(words)

            for j in set(words):

                #j = j.decode('utf-8').strip()

                wordcount[j] = wordcount[j] + words.count(j)

                # print(wordcount)

    # print 'WORD::::::::::COUNT'

    for (k, v) in wordcount.items():
        if k.lower() in stop_words:
            del wordcount[k]
	
    return wordcount

def GetWordCount2(data):
    tokenizer = TreebankWordTokenizer()
    stop_words = set(stopwords.words('english'))
    words = []
    wordcount = defaultdict(int)
    for i in data:
        if i == '\n':
            continue
        else:
            #i = i.encode('utf-8')
            words = tokenizer.tokenize(i)

            # print(words)

            for j in set(words):

                #j = j.decode('utf-8').strip()

                wordcount[j] = wordcount[j] + words.count(j)

                # print(wordcount)

    # print 'WORD::::::::::COUNT'

    for (k, v) in wordcount.items():
        if k.lower() in stop_words:
            del wordcount[k]
	
    return wordcount

def GetExcelSheetName(url):
    Sname = ''
    SplitList = url.split('/')
    NameList = SplitList[-2].split('-')
    for i in range(len(NameList)):

            Sname = Sname + NameList[i]
    if len(Sname) >= 15:
        return Sname[0:12]
    else:
        return Sname


def RandomTextGen():
    RText=''
    str=string.ascii_uppercase
    return RText.join(choice(str) for x in range(3))	
	
def PosTags(dct):
    NounKeys=''
    ProNounKeys=''
    VerbKeys=''
    AdjKeys=''
    AdVerbKeys=''
    NounCnt,ProNounCnt,VerbCnt,AdjCnt,AdvCnt=[0,0,0,0,0]
    KeySonly=list(dct.keys())
    for i in KeySonly:
        if i  not in list(string.punctuation):
            ValNTag=list(nltk.pos_tag([i]))
            #print(ValNTag)

            if any([ValNTag[0][1]=="NN",ValNTag[0][1]=="NNP",ValNTag[0][1]=="NNS",ValNTag[0][1]=="NNPS"]):
                NounKeys= NounKeys+ValNTag[0][0]+"|" 
                NounCnt+=1
            if any([ValNTag[0][1]=="WP",ValNTag[0][1]=="WPS",ValNTag[0][1]=="PRP",ValNTag[0][1]=="PRPS"]):  
                ProNounKeys=ProNounKeys+ValNTag[0][0]+"|"
                ProNounCnt+=1
            if any([ValNTag[0][1]=="VB",ValNTag[0][1]=="VBD",ValNTag[0][1]=="VBG",ValNTag[0][1]=="VBGN",ValNTag[0][1]=="VBP",ValNTag[0][1]=="VBZ"]):
                VerbKeys=VerbKeys+ValNTag[0][0]+"|"
                VerbCnt+=1

    return {'POS':['Noun','ProNoun','Verb'],
	         'COUNT':[NounCnt,ProNounCnt,VerbCnt],
			 'VALUES':[ NounKeys,ProNounKeys,VerbKeys]}


# Program starts in here

path = os.getcwd()

#path='D:\python\News' #edit this with the path you need 
Dataset='DELTA' # chnage this to something else ('DELTA') if you want to see difference data
CurrFileName = GenerateFileName(path, 'T', 'NEWS', 'TXT')
PrevFileName = GenerateFileName(path, 'Y', 'NEWS', 'TXT')
CountsFileName = GenerateFileName(path, 'T', 'Counts_', 'xls')
NewLinks = []
PosCountsNList={}
TodaysNewsALL = CreateLinksFile(CurrFileName)
TodaysNewsLatest = CompareAndGenDiff(TodaysNewsALL, PrevFileName,Dataset)
ExWriter = pd.ExcelWriter(CountsFileName)
for todaysnews in TodaysNewsLatest:
    Content = ReadNews(todaysnews)
    WorndsNCounts = GetWordCount2(Content)
    PosCountsNList=PosTags(WorndsNCounts)
    #print(PosCountsNList)
    SheetName = GetExcelSheetName(todaysnews)+RandomTextGen()
    Header = ({'NewsURL':[todaysnews]})
    df_Header = pd.DataFrame(Header)
    df_POSData=pd.DataFrame(PosCountsNList)
    
    df_Header.to_excel(ExWriter,SheetName, index=False)
    df_POSData.to_excel(ExWriter,SheetName, index=False,startrow=3)
    Df = pd.DataFrame({'WORD': WorndsNCounts.keys(),
                      'COUNT': WorndsNCounts.values()})
    
    Df.to_excel(ExWriter, SheetName,index=False,startrow=8)
    print'TAB :-->{} Created'.format(SheetName)
    ExWriter.save()
