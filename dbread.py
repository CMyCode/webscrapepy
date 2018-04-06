iterimport pymysql
import nltk
import re

def readDataFromDb():
    data=""
    db = pymysql.connect(host = "localhost", user = "root", passwd = "root", db = "news")
    cur = db.cursor()
#    print ("----------------------")
    try:
       sql="select news,date from thehindu"
       cur.execute(sql)
        
       for (news_value,date) in cur:
                     
           news_value=news_value.replace('\n',' ')
           news_value=news_value.replace('\t',' ')
           news_value=news_value.replace("\'",'')
           news_value=news_value.replace('\',' ')
           news_value=news_value.replace("\",' ')
           news_value=news_value.replace('\n',' ')
           news_value=news_value.replace('\t',' ')
           news_value=news_value.replace("\'",'')
           news_value=news_value.replace('\',' ')
           news_value=news_value.replace("\",' ')
           news_value=news_value.replace("\x91",'')
           news_value=news_value.replace("\x92",'')
           news_value=news_value.replace("\x93",'')
           news_value=news_value.replace("\x94",'')
           news_value=news_value.replace("\x97",'')
           news_value=news_value.replace("\/",' ')
           news_value=news_value.replace("\",' ')
           news_value=news_value.replace("\",' ')
           news_value=news_value.replace("\% ",' ')
           news_value=news_value.replace("Consider ",'')
           news_value=news_value.replace("following",'')
           news_value=news_value.replace("determines",'')
           news_value=news_value.replace("’",'')
           news_value=news_value.replace("?",'')

#          to remove numerics from strings
           news_value=''.join([i for i in news_value if not i.isdigit()])

#           to remove special characters
           news_value=re.sub(r'[.|$|/|:|!|)|(]',r' ',news_value)
           
           print(news_value);
                
           tok=nltk_word_tag(news_value)
               
           nounString=getNouns(tok)
           nounString=nounString[:-1]
           nounword=nounString.split('|')
               
           pronounString=getPronouns(tok)
           pronounString=pronounString[:-1]
           pronounword=pronounString.split('|')

           verbString=getVerbs(tok)
           verbString=verbString[:-1]
           verbword=verbString.split('|')

           adjectiveString=getAdjectives(tok)
           adjectiveString=adjectiveString[:-1]
           adjectiveword=adjectiveString.split('|')

           adverbString=getAdverbs(tok)
           adverbString=adverbString[:-1]
           adverbword=adverbString.split('|')

#          db = pymysql.connect(host = "localhost", user = "root", passwd = "root", db = "news")
              
#          to find max size 
           countList=[len(nounword),len(verbword),len(adjectiveword),len(adverbword)];
           count=max(countList);
                              
           print(nounword);
                   
           print(verbword);
           print(count);
               
               
           for i in range(count):
                   print(i);
                   nw="";
                   vw="";
                   adjv="";
                   advb=""
                   pr="";
                   if i<len(nounword):
                       nw=nounword[i];
                   if i<len(pronounword):
                       pr=pronounword[i];
                   if i<len(verbword):
                       vw=verbword[i];
                   if i<len(adjectiveword):
                       adjv=adjectiveword[i];
                   if i<len(adverbword):
                       advb=adverbword[i];

                   cur = db.cursor()
                   sql="";
                   try:
                       sql=("insert into thehindupos values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(news_value,nw,pr,vw,adjv,advb,date))
                       cur.execute(sql)
                       db.commit()
#                           print("updated")
        
                   except pymysql.Error as err:
                       print("Something went wrong: {}".format(err))   
               
           print("-------Succefully Updated-----------------")
           
    except pymysql.Error as err:
          print("Something went wrong: {}".format(err))
    return data

def nltk_word_tag(sent):
        tokens=nltk.word_tokenize(sent)
        pos_tokens=nltk.pos_tag(tokens) 
        return pos_tokens; 

def getNouns(tokens):
    nouns=""
    for eachtoken in tokens:
        if any([eachtoken[1]=="NN",eachtoken[1]=="NNP",eachtoken[1]=="NNS",eachtoken[1]=="NNPS"]):  
           nouns=nouns+eachtoken[0]+"|"
    return nouns 

def getPronouns(tokens):
    pronouns=""
    for eachtoken in tokens:
        if any([eachtoken[1]=="WP",eachtoken[1]=="WPS",eachtoken[1]=="PRP",eachtoken[1]=="PRPS"]):  
            pronouns=pronouns+eachtoken[0]+"|"
    return pronouns 

def getVerbs(tokens):
    verbs=""
    for eachtoken in tokens:
        if any([eachtoken[1]=="VB",eachtoken[1]=="VBD",eachtoken[1]=="VBG",eachtoken[1]=="VBGN",eachtoken[1]=="VBP",eachtoken[1]=="VBZ"]):
            verbs=verbs+eachtoken[0]+"|"
    return verbs

def getAdjectives(tok):
    adjectives=""
    for eachtoken in tok:
        if any ([eachtoken[1]=="JJ",eachtoken[1]=="JJR",eachtoken[1]=="JJS"]):
           adjectives=adjectives+eachtoken[0]+"|"
    return adjectives 

def getAdverbs(tok):
    adverbs=""
    for eachtoken in tok:
        if any ([eachtoken[1]=="RB",eachtoken[1]=="RBR",eachtoken[1]=="RBS",eachtoken[1]=="WRB"]):
           adverbs=adverbs+eachtoken[0]+"|"
    return adverbs
    
readDataFromDb()