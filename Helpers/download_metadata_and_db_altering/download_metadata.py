import shutil
import argparse
import urllib.request
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import os
import pymongo
from pymongo import MongoClient
import glob

ppn_list = []
metaDataDownloadURLPrefix="http://digital.staatsbibliothek-berlin.de/metsresolver/?PPN="


with open('PATH/TO/PPN-LIST') as f:
    lines = f.readlines()
    lines.pop(0)
    for line in lines:
        ppn_list.append(line)
        
    #print(len(ppn_list))
    f.close()

metaDataDownloadURLPrefix="http://digital.staatsbibliothek-berlin.de/metsresolver/?PPN="
downloadPathPrefix="."
addPPNPrefix=True
extractIllustrations=False
illustrationExportFileType= ".jpg"
# handy if a certain file set has been downloaded before and processing has to be limited to post-processing only
skipDownloads=False
verbose=True
# determines which ALTO elements should be extracted
consideredAltoElements=['{http://www.loc.gov/standards/alto/ns-v2#}Illustration']#,'{http://www.loc.gov/standards/alto/ns-v2#}GraphicalElement']

tiffDownloadLink="http://ngcs.staatsbibliothek-berlin.de/?action=metsImage&format=jpg&metsFile=@PPN@&divID=@PHYSID@&original=true"


#for i in range(50,450):
    
sbbPrefix = "sbb"
downloadPathPrefix="download_temp"
savePathPrefix="saved_images"
# set connection to mongodb
client = MongoClient()
# choose db
db = client.unicorn
# choose table
books = db.books

# Chinese book with fulltext
# ppn="3343669865"
# book with fulltext
#ppn="792383192"
# book with printer's mark without fulltext
#ppn="715665294"
count = 0
problems = []
for ppn in ppn_list:
    print(str(count) + ": Download " + str(ppn))
    count += 1
    currentDownloadURL = metaDataDownloadURLPrefix + str(ppn)
    # meds mods will be downloaded to where you started the script
    try: 

        # todo: error handling
        metsModsPath = str(ppn) + ".xml"
        urllib.request.urlretrieve(currentDownloadURL, metsModsPath)
        

        # STANDARD file download settings
        retrievalScope=['TIFF','FULLTEXT']
        # per Schalter steuern, default: FULLTEXT und PRESENTATION
        # <mets:fileGrp USE="THUMBS"
        # <mets:fileGrp USE="DEFAULT">
        # <mets:fileGrp USE="FULLTEXT">
        # <mets:fileGrp USE="PRESENTATION">
        # download der Files
        tree = ET.parse(metsModsPath)
        root = tree.getroot()

        # a list of downloaded TIFF files
        alreadyDownloadedPhysID=[]
        # a dict of paths to ALTO fulltexts (id->download dir)
        altoPaths=dict()

        titles = []
        genres = []
        publishers = []
        coverages = []
        creators = []

        
        for dmdSec in root.findall('{http://www.loc.gov/METS/}dmdSec'):
            for wrap in dmdSec.findall('{http://www.loc.gov/METS/}mdWrap'):
                for xml in wrap.findall('{http://www.loc.gov/METS/}xmlData'):
                    for mods in xml.findall('{http://www.loc.gov/mods/v3}mods'):  
                        # Here are the Information

                            # Get the title
                            for titleInfo in mods.findall('{http://www.loc.gov/mods/v3}titleInfo'):
                                for title in titleInfo.findall('{http://www.loc.gov/mods/v3}title'):
                                    titles.append(title.text)
                            
                            # Get the subject
                            for genre in mods.findall('{http://www.loc.gov/mods/v3}classification'):
                                genres.append(genre.text)
                                #print(genre.text)

                            # Get the language
                            for langs in mods.findall('{http://www.loc.gov/mods/v3}language'):
                                for lan in langs.findall('{http://www.loc.gov/mods/v3}languageTerm'):
                                    language = lan.text
                            
                            # Get PPN
                            for identifiers in mods.findall('{http://www.loc.gov/mods/v3}identifier'):
                                if identifiers.get('type') == "PPNanalog":
                                    PPN_a = identifiers.text
                            

                            for origInfo in mods.findall('{http://www.loc.gov/mods/v3}originInfo'):
                                # Get publisher
                                for publisher in origInfo.findall('{http://www.loc.gov/mods/v3}publisher'):
                                    publishers.append(publisher.text)

                                # Get Date
                                for dates in origInfo.findall('{http://www.loc.gov/mods/v3}dateIssued'):
                                    date = dates.text
                                
                                # Identifier
                                identifier = "PPN" + str(ppn)

                                # coverage
                                for places in origInfo.findall('{http://www.loc.gov/mods/v3}place'):
                                    for term in places.findall('{http://www.loc.gov/mods/v3}placeTerm'):
                                        coverages.append(term.text)


                            # creator
                            for names in mods.findall('{http://www.loc.gov/mods/v3}name'):
                                if names.get('type') == "personal":
                                    for name in names.findall('{http://www.loc.gov/mods/v3}displayForm'):
                                            creators.append(name.text)
                            
        temp = {
            "title" : titles,
            "subject" : genres,
            "language" : language,
            "PPN" : PPN_a,
            "publisher" : publishers,
            "date" : date,
            "identifier" : identifier,
            "creator" : creators,
            "coverage" : coverages
        }
        db.books.insert_one(temp)
        # Remove file you just downloaded, otherwise you will kill your storage
        files = glob.glob('PATH/TO/xml/*') # keep the *
        for f in files:
            os.remove(f)

    except Exception as e:
        problems.append({"ppn": str(ppn), "reason": str(e) })
        print("Problem at " + str(ppn))
    

print(problems)
