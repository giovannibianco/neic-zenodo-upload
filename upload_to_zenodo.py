#!/usr/bin/python

import sys, getopt
import requests
import json
from os import system, name

def main(argv):
   global inputfile; inputfile = ''
   global pathtofile; pathtofile = ''
   global metadatafile; metadatafile = ''
   global descriptionfile; descriptionfile = ''
   global ACCESS_TOKEN; ACCESS_TOKEN = ""
   prog_string='test.py -i <file to be published> -o <metadata file> -d <description file> -A <access_token>'
   try:
      opts, args = getopt.getopt(argv,"hi:m:d:A:p:",["ifile=","ofile=","dfile=","token=","path="])
   except getopt.GetoptError:
      print prog_string
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print prog_string
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-p", "--path"):
         pathtofile = arg
      elif opt in ("-m", "--ofile"):
         metadatafile = arg
      elif opt in ("-d", "--dfile"):
         descriptionfile = arg
      elif opt in ("-A", "--token"):
         ACCESS_TOKEN = str(arg)
   print 'File to be published is: ',pathtofile,inputfile
   print 'Author metadata file is : ',metadatafile
   print 'Description file is : ',descriptionfile
   print 'Access token = ', ACCESS_TOKEN

if __name__ == "__main__":
   main(sys.argv[1:])

system('clear');
   
filename = inputfile; # this is for the put request below...
path = "/home/jwhite/%s" % filename  ## this is for opening the file below
path = pathtofile + inputfile; # print path # We must test that the full pathname is VALID!
from pathlib import Path

my_file = Path(path)
if not my_file.is_file():
    # system('clear');
    print 'The file to be uploaded ',path,' is invalid... exiting. error code 2.'
    sys.exit(2)


my_file = Path(metadatafile)
if not my_file.is_file():
    # system('clear');
    print 'The metadata file ',metadatafile,' is invalid... exiting. error code 2.'
    sys.exit(2)

filename = inputfile; # this is for the put request below...
path = "/home/jwhite/%s" % filename  ## this is for opening the file below
path = pathtofile + inputfile; # print path # We must test that the full pathname is VALID!
from pathlib import Path

my_file = Path(descriptionfile)
if not my_file.is_file():
    # system('clear');
    print 'The description file ',descriptionfile,' is invalid... exiting. error code 2.'
    sys.exit(2)

    # Set up the headers
headers = {"Content-Type": "application/json"}
params = {'access_token': ACCESS_TOKEN}

# sys.exit(1);

r = requests.post('https://sandbox.zenodo.org/api/deposit/depositions',params=params,json={},headers=headers)
print 'HTTP return code: ',r.status_code
json_formatted_str = json.dumps(r.json(), indent=2)
print json_formatted_str

bucket_url = r.json()["links"]["bucket"]
deposition_id=r.json()["record_id"]


        
# We pass the file object (fp) directly to the request as the 'data' to be uploaded.
# The target URL is a combination of the buckets link with the desired filename separated by a slash.
with open(path, "rb") as fp:
    r = requests.put("%s/%s" % (bucket_url, filename), data=fp, params=params)

print 'HTTP return code from file adding step: ',r.status_code
json_formatted_str = json.dumps(r.json(), indent=2)
print json_formatted_str

jsondata={}
metadata={}
creators = []

FILE=metadatafile;
tmp_creator={};

with open(FILE) as f:
    for line in f:
        name="";orcid="";affil=""
        name,orcid,affil1=line.split(',') # here we must check that an ORCID exists! It might not? User may not have one!
        # if not orcid:
        #     print 'ORCID is empty...',orcid;
        # else:
        #     print 'ORCID is ...',orcid;
        affil=affil1.rstrip();
        family_name,first_name=name.split(' ')
        final_name=family_name+', '+first_name;
        tmp_creator['name']=final_name
        if orcid:
            tmp_creator['orcid']=orcid
        tmp_creator['affiliation']=affil
        creators.append(tmp_creator)
        tmp_creator={}

metadata['creators']=creators

FILE=descriptionfile;
description_string=""
with open(FILE, 'r') as file:
    description_string = file.read().replace('\n', ' ')

# print description_string;
metadata['description']=description_string # from the file above

title=str(raw_input("Enter title of upload: "))
metadata['title']=title # "Euro to CHF exchange rates"

# upload type: Publication, Poster, Presentation, Dataset, Image, Audio/Video, Software, Lesson, Other
# Maybe this could be interrogated from the web interface? later...
up_type=str(raw_input("Enter upload type. Case in-sensitive. Must be one of the following:\nPublication\nPoster\nPresentation\nDataset\nImage\nAudio/Video\nSoftware\nLesson\nOther\n : "))
metadata['upload_type']=up_type # Check this!
#    
# if the upload_type is  Publication, then one of the following must be selected:
#
# publication type: Annotation collection, Book, Book section, Conference paper, Data management plan, Journal article, Patent, Preprint, Project deliverable, Project milestone, Proposal, Report, Software documentation, Taxonomic treatment, Technical note, Thesis, Working paper, Other
#
# if the upload_type is image, then one of the following must be selected:
#
# image_type: figure, plot, drawing, diagram, photo, other
#

# Maybe this could be interrogated from the web interface? later...
list_of_pub_types=["Annotation collection", "Book", "Book section", "Conference paper", "Data management plan", "Journal article", "Patent", "Preprint", "Project deliverable", "Project milestone", "Proposal", "Report", "Software documentation", "Taxonomic treatment", "Technical note", "Thesis", "Working paper", "Other"]

list_of_fig_types=["figure", "plot", "drawing", "diagram", "photo", "other"]

if up_type.lower() == "publication":
    metadata['publication_type']=""
    pub_type=str(raw_input("Enter publication type. Case in-sensitive. Must be one of the following:\nAnnotation collection\nBook\nBook section\nConference paper\nData management plan\nJournal article\nPatent\nPreprint\nProject deliverable\nProject milestone\nProposal\nReport\nSoftware documentation\nTaxonomic treatment\nTechnical note\nThesis\nWorking paper\nOther\n : ")) # print pub_type; chop trailing whitespaces??
    for pubt in list_of_pub_types:
        if pubt.lower() == pub_type.lower():
            metadata['publication_type']=pub_type
            
    if metadata['publication_type'] == "":
        print 'Error: Publication type was set to ',pub_type,' exiting.'
        sys.exit(2)

if up_type.lower() == "image":
    metadata['image_type']=""
    im_type=str(raw_input("Enter image type. Case in-sensitive. Must be one of the following:\nfigure\nplot\ndrawing\ndiagram\nphoto\nother\n : "))
    for figt in list_of_fig_types:
        if figt.lower() == im_type.lower():
            metadata['image_type']=im_type

    if metadata['image_type'] == "":
        print 'Error: Image type was set to ',im_type,' exiting.'
        sys.exit(2)
        
# jsondata is the metadata to be uploaded to the deposition_id
jsondata['metadata']=metadata;
json_formatted_str = json.dumps(jsondata, indent=2)
print(json_formatted_str)

# Add the metadata... to the deposition ID
r = requests.put('https://sandbox.zenodo.org/api/deposit/depositions/%s' % deposition_id,params={'access_token': ACCESS_TOKEN}, data=json.dumps(jsondata),headers=headers)
print "HTTP return code from metadata step: ",r.status_code

sys.exit(1)
#
# Here is the publishing step...
# Note... all you need here is the deposition_id obtained above! Could be a good place for sanity check?
#
r = requests.post('https://sandbox.zenodo.org/api/deposit/depositions/%s/actions/publish' % deposition_id, params={'access_token': ACCESS_TOKEN})
print "HTTP return code from publishing step: ",r.status_code
json_formatted_str = json.dumps(r.json(), indent=2)
print json_formatted_str