
# coding: utf-8

# # Companies House Parser

# In[1]:

from bs4 import BeautifulSoup
from lxml import etree
import json
import graphlab
import datetime
import cPickle as pickle
import csv
import re
import sys
import os
get_ipython().magic(u'matplotlib inline')


# In[7]:

directory='C:\Users\User\Desktop\XBRL\Accounts_Bulk_Data-2016-11-02'

def CH_parse(docLink):
    
    docTuple=[]
    
    try:
        docTree = etree.parse(docLink)
    except etree.XMLSyntaxError,detail:
        return detail.error_log
    
    docTuple.append((docTree.getroot()).nsmap)
    
    for child in (docTree.getroot()).getiterator():
        if (child.text!=None or child.tail!=None) and re.search('^.*STYLE',(etree.tostring(child)).upper())==None:
            
            if child.text==None:
                text=child.text
            else:
                text=(child.text).strip()
            
            if child.tail==None:    
                tail=child.tail
            else: 
                tail=(child.tail).strip()
            
            docTuple.append([child.items(),text,tail])
            #clear text and tuple?
        else:
            continue
                

    return docTuple    
    


# In[4]:

sys.getsizeof(CH_parse('C:\Users\User\Desktop\XBRL\Accounts_Bulk_Data-2016-11-02\Prod223_1734_00107641_20160331.html'))


# In[5]:

CH_parse('C:\Users\User\Desktop\XBRL\Accounts_Bulk_Data-2016-11-02\Prod223_1734_00107641_20160331.html')


# In[6]:

dbCH=[]
for filename in os.listdir(directory):
    if filename.endswith(".html") or filename.endswith(".xml"): 
        dbCH.append(CH_parse(os.path.join(directory, filename)))
        continue
    else:
        continue

print 'directory iterated!'


# In[7]:

sys.getsizeof(dbCH)


# In[64]:

p=0
with open('C:\Users\User\Desktop\XBRL\dbCH.csv', 'wb') as outfile:
    wr = csv.writer(outfile)# quoting=csv.QUOTE_ALL)
    for rec in dbCH:
        wr.writerow(rec)
        p += 1
print 'done!'
print p


# In[65]:

myfile.close()


# In[7]:

len(dbCH)#csv has 70 more records..why?


# In[152]:

dbCH_In=[]
csv.field_size_limit(1000000)
with open('C:\Users\User\Desktop\XBRL\dbCH.csv', 'rb') as infile:
    rdr = csv.reader(infile, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    for row in rdr:
        dbCH_In.append(row)
        


# In[153]:

infile.close()


# In[154]:

len(dbCH_In)


# In[160]:

type(dbCH_In[0])


# In[156]:

type(dbCH_In[0][0])


# In[157]:

dbCH_In[0]


# ### pickle

# In[8]:

with open('C:\Users\User\Desktop\XBRL\dbCH_Pickle', 'wb') as pkFile:
    pickle.dump(dbCH,pkFile)
print 'done!'
#######consider using JSON


# In[9]:

pkFile.close() #this file is larger than csv also try lagacy pickle


# In[2]:

with open('C:\Users\User\Desktop\XBRL\dbCH_Pickle', 'rb') as pkFilea:
    dbCH_unpk=pickle.load(pkFilea)
print 'done!'


# In[4]:

type(dbCH_unpk)


# In[ ]:




# ## Search Function

# In[4]:

dbCH_unpk[0][3][0][1][1]


# In[5]:

type(dbCH_unpk[0][3][0][1])


# In[3]:

dbCH_unpk[0][3][0]


# In[4]:

dbCH_unpk[0][0]


# def retrieve_fields(argList):
#     retfield=[]
#     for arg in argList:
#         for i in xrange(len(dbCH_unpk)):# no of recs
#             for j in xrange(len(dbCH_unpk[i])):# record
#                 for k in xrange(len(dbCH_unpk[i][j])):#
#                     for l in xrange(len(dbCH_unpk[i][j][k])):
#                         for m in xrange(len(dbCH_unpk[i][j][k][l])):
#                             for n in xrange(len(dbCH_unpk[i][j][k][l][m])):
#                                 if re.search(arg,dbCH_unpk[i][j][k][l][m])==True:
#                                     retfield.append(dbCH_unpk[i][j][1])
#     return retfield
#                                  
#         
# 

# In[4]:

argList=['UKCompaniesHouseRegisteredNumber','NameEntityOfficer','NameThirdPartyAgent']


# In[ ]:

#print retrieve_fields(agl)


# In[5]:

#def retrieve_fields(argList):
#retfield=[]
#for arg in argList:
for record in dbCH_unpk:
    for tag in record:
        if type(tag)!=dict:
            for tpl in tag:
                if type(tpl)==list and len(tpl)>0:
                    for attr in tpl:
                        #print attr[1],attr[1].strip(),tag[1]
                        if re.search('.*NameThirdPartyAgent',attr[1].strip())!=None:
                            #retfield.append(tag[1])
                            print tag[1]
                

                    
#print retfield
                      


# In[ ]:

print retfield


# In[ ]:

len(retfield)


# In[ ]:

#def retrieve_fields2(argList):
retfield=[]
outfield=[]

for record in dbCH_unpk:
    for itag in [tag for tag in record if type(tag)!=dict]:
        for itpl in [tpl for tpl in itag if type(tpl)==list and len(tpl)>0]:
            for attr in itpl:
                #print attr[1],attr[1].strip(),tag[1]
                for arg in argList:
                    if re.search('.*'+ re.escape(arg)+'',attr[1].strip())!=None:#the if excludes docs that do not have arg
                        retfield.append((arg,itag[1]))
    field_values=set(retfield)
    retfield=[]
    print sorted(list(field_values))
    
                
                

                    
    #return retfield


# In[ ]:

print cc


# In[22]:

counta=0
countb=[]
noTags=0
for record in dbCH_unpk:
    noTags=len(record)
    ikey=[key for key in (record[0]).keys() if re.search('xbrl',record[0][key])!=None]
    print ikey
    for itag in [tag for tag in record if type(tag)!=dict]:
        for itpl in [tpl for tpl in itag if type(tpl)==list and len(tpl)>0]:
            for attr in itpl:
                 if (attr[1]).find(':')>0:
                        if attr[1][0:(attr[1]).find(':')] in ikey:
                            counta +=1
    if counta>0:
        countb.append((counta,noTags))
        counta=0
        noTags=0
                            
            
print countb          
    
    ##strip!!!!!!!
    #for tpl in record[1][0]:
        
        #print tpl
        #for attr in tpl:
            #print attr
            #if (attr[1]).find(':')>0:
                #print attr[1]
                
            
        
        
    


# In[8]:

for key in (dbCH_unpk[0][0]).keys():
    if re.search('xbrl',dbCH_unpk[0][0][key])==None:
        print dbCH_unpk[0][0][key]


# In[10]:

#generator


# In[20]:

dbCH_unpk[0][93][0]


# In[19]:

len(countb)


# In[8]:

counta=0
countb=[]
noTags=0
for record in dbCH_unpk:
    noTags=len(record)
    ikey=[key for key in (record[0]).keys() if re.compile('.*xbrl.*|.*govtalk.*').search(record[0][key])!=None]
    for itag in [tag for tag in record if type(tag)!=dict]:
        for itpl in [tpl for tpl in itag if type(tpl)==list and len(tpl)>0]:
            for attr in itpl:
                 if (attr[1]).find(':')>0 and (attr[0]).upper()=='NAME':
                        if attr[1][0:(attr[1]).find(':')] in ikey:
                            counta +=1
    if counta>0:
        countb.append((counta,noTags))
        counta=0
        noTags=0
                            
            
print countb     


# In[ ]:



