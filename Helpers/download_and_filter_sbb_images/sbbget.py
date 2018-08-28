import shutil
import argparse
import urllib.request
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import os
from PIL import Image
from time import gmtime, strftime
from datetime import datetime

ppns = []
dimensions = []
with open('OCR-PPN-Liste.txt') as f:
    lines = f.readlines()
    lines.pop(0)
    for line in lines:
        line_split = line.split(' ')
        ppn_cleaned = line_split[len(line_split)-1].rstrip().replace('PPN', '')
        ppns.append(ppn_cleaned)
        
    print(len(ppns))
    f.close()

def download_images():
    currentDownloadURL=metaDataDownloadURLPrefix+ppn

    # todo: error handling
    metsModsPath=ppn+".xml"
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

    fileID2physID=dict()
    # first, we have to build a dict mapping various IDs to physical pages
    for div in root.iter('{http://www.loc.gov/METS/}div'):
        for fptr in div.iter('{http://www.loc.gov/METS/}fptr'):
            #print(fptr.tag,fptr.attrib)
            fileID2physID[fptr.attrib['FILEID']]=div.attrib['ID']
            #print(fptr.attrib['FILEID'],fileID2physID[fptr.attrib['FILEID']])


    #raise SystemExit

    # a list of downloaded TIFF files
    alreadyDownloadedPhysID=[]
    # a dict of paths to ALTO fulltexts (id->download dir)
    altoPaths=dict()

    # we are only interested in fileGrp nodes below fileSec...
    for fileSec in root.iter('{http://www.loc.gov/METS/}fileSec'):
        for child in fileSec.iter('{http://www.loc.gov/METS/}fileGrp'):
            currentUse=child.attrib['USE']

            # which contains file nodes...
            for fileNode in child.iter('{http://www.loc.gov/METS/}file'):
            # embedding FLocat node pointing to the URLs of interest
                id = fileNode.attrib['ID']
                downloadDir="./"+downloadPathPrefix + "/" + id
                saveDir= "./" + savePathPrefix + "/" + id
                # only create need sub directories
                if currentUse in retrievalScope :
                    if not os.path.exists(downloadDir):
                        if verbose:
                            print(downloadDir)
                        os.mkdir(downloadDir)

                if 'TIFF' in retrievalScope:
                    # try to download TIFF first
                    downloadDir = "./" + downloadPathPrefix + "/" + id
                    saveDir = "./" + savePathPrefix + "/"
                    tiffDir=downloadDir.replace(currentUse,'TIFF')
                    if not os.path.exists(tiffDir):
                        os.mkdir(tiffDir)
                    try:
                        if not fileID2physID[id] in alreadyDownloadedPhysID:
                            if verbose:
                                print("Downloading to " + tiffDir)
                            if not skipDownloads:
                                urllib.request.urlretrieve(tiffDownloadLink.replace('@PPN@',ppn).replace('@PHYSID@',fileID2physID[id]),tiffDir+"/"+ppn+".tif")
                            alreadyDownloadedPhysID.append(fileID2physID[id])
                    except urllib.error.URLError:
                        print("Error downloading " + ppn+".tif")

                if currentUse in retrievalScope :
                    for fLocat in fileNode.iter('{http://www.loc.gov/METS/}FLocat'):
                        if (fLocat.attrib['LOCTYPE'] == 'URL'):
                            if verbose:
                                print("Processing "+id)
                            href=fLocat.attrib['{http://www.w3.org/1999/xlink}href']
                            rawPath=urlparse(href).path
                            tokens=rawPath.split("/")
                            outputPath=tokens[-1]

                            if verbose:
                                print("\tSaving to: " + downloadDir + "/" + outputPath)
                            try:
                                if not skipDownloads:
                                    urllib.request.urlretrieve(href, downloadDir+"/"+outputPath)
                                if currentUse=='FULLTEXT':
                                    altoPaths[id]=[downloadDir,outputPath]
                            except urllib.error.URLError:
                                print("\tError processing "+href)

    # extract illustrations found in ALTO files
    #illuID = 0
    if extractIllustrations:
        for key in altoPaths:
            tiffDir=altoPaths[key][0].replace('FULLTEXT','TIFF')+"/"+altoPaths[key][1].replace(".","_")+"/"
            tiffDir="."+tiffDir[1:-1]
            if not os.path.exists(tiffDir):
                os.mkdir(tiffDir)
                if verbose:
                    print("Creating "+tiffDir)
            if verbose:
                print("Processing ALTO XML in: "+altoPaths[key][0]+"/"+altoPaths[key][1])
            tree = ET.parse(altoPaths[key][0]+"/"+altoPaths[key][1])
            root = tree.getroot()
            for e in root.findall('.//{http://www.loc.gov/standards/alto/ns-v2#}PrintSpace'):
                for el in e:
                    if el.tag in consideredAltoElements:
                        illuID=el.attrib['ID']
                        #if verbose:
                        #print("\tExtracting "+illuID)
                        h=int(el.attrib['HEIGHT'])
                        w=int(el.attrib['WIDTH'])
                        if h > 150 and w > 150:
                            if verbose:
                                print("Saving Image")
                            entry = {"WIDTH" : w, "HEIGHT": h, "LABEL" : key.split("_")[1]}
                            dimensions.append(entry)
                            hpos=int(el.attrib['HPOS'])
                            vpos=int(el.attrib['VPOS'])
                            #print(altoPaths[key])
                            #print(altoPaths[key][0].replace('FULLTEXT','TIFF')+"/"+ppn+'.tif')
                            img=Image.open(altoPaths[key][0].replace('FULLTEXT','TIFF')+"/"+ppn+'.tif')
                            if verbose:
                                print("\t\tImage size:",img.size)
                                print("\t\tCrop range:", h, w, vpos, hpos)
                            # (left, upper, right, lower)-tuple.
                            img2 = img.crop((hpos, vpos, hpos+w, vpos+h))

                            img2.save(saveDir + key.split("_")[1] + "_" +illuID + illustrationExportFileType)
                        else:
                            if verbose:
                                print("Image is too small: Not considering")

    shutil.rmtree('sbb/download_temp', ignore_errors=True)
    if not os.path.exists("sbb/download_temp"):
        if verbose:
            print("Deleted tempfolder")
    print("Done.")

metaDataDownloadURLPrefix="http://digital.staatsbibliothek-berlin.de/metsresolver/?PPN="
downloadPathPrefix="."
addPPNPrefix=True
extractIllustrations=True
illustrationExportFileType= ".tif"
# handy if a certain file set has been downloaded before and processing has to be limited to post-processing only
skipDownloads=False
verbose=True
# determines which ALTO elements should be extracted
consideredAltoElements=['{http://www.loc.gov/standards/alto/ns-v2#}Illustration']#,'{http://www.loc.gov/standards/alto/ns-v2#}GraphicalElement']

tiffDownloadLink="http://ngcs.staatsbibliothek-berlin.de/?action=metsImage&format=jpg&metsFile=@PPN@&divID=@PHYSID@&original=true"

log_file_name = 'ppn_log.txt'
start = 0
end = len(ppns)
if os.path.isfile(log_file_name):
    with open(log_file_name, 'r') as log_file:
        log_entries = log_file.readlines()
        start = len(log_entries)
else:
    with open(log_file_name, 'w') as log_file:
        pass

for i in range(start,end):
    
    sbbPrefix = "sbb"
    downloadPathPrefix="download_temp"
    savePathPrefix="saved_images"
    ppn = ppns[i]
    current_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    with open(log_file_name, 'a') as log_file:
        log_file.write(current_time + " " + ppn + " (Number: %d)" % (i) + "\n")

    if addPPNPrefix:
        ppn="PPN"+ppn
        print(ppn)
    
    if not os.path.exists(sbbPrefix+"/"):
        if verbose:
            print("Creating "+sbbPrefix+"/")
        os.mkdir(sbbPrefix+"/")
    
    downloadPathPrefix= sbbPrefix + "/" + downloadPathPrefix
    savePathPrefix = sbbPrefix + "/" + savePathPrefix
    
    if not os.path.exists(downloadPathPrefix+"/"):
        if verbose:
            print("Creating "+downloadPathPrefix+"/")
        os.mkdir(downloadPathPrefix+"/")
    downloadPathPrefix=downloadPathPrefix+"/"+ppn
    if not os.path.exists(downloadPathPrefix+"/"):
        if verbose:
            print("Creating "+downloadPathPrefix+"/")
        os.mkdir(downloadPathPrefix+"/")

    if not os.path.exists(savePathPrefix+"/"):
        if verbose:
            print("Creating "+savePathPrefix+"/")
        os.mkdir(savePathPrefix+"/")
    savePathPrefix=savePathPrefix+"/"+ppn
    if not os.path.exists(savePathPrefix+"/"):
        if verbose:
            print("Creating "+savePathPrefix+"/")
        os.mkdir(savePathPrefix+"/")
        
download_images()