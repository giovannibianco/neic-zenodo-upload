#!/bin/sh

# You need to specify the full path to where the
# git clone https://github.com/neicnordic/neic.no.git
# places the files on your filesystem...
#
# DIRECTORY=/home/jwhite/NeIC/neic.no/_people/*.md
#

DIRECTORY=/home/jwhite/NeIC/neic.no/_people/*.md
OUTPUT_FILE=metadata.txt

if [ -f $OUTPUT_FILE ]
then
    echo $OUTPUT_FILE exists... copying to $OUTPUT_FILE.bak
    cp $OUTPUT_FILE $OUTPUT_FILE.bak
    echo Removing $OUTPUT_FILE ... 
    rm $OUTPUT_FILE
fi

PROJECT=dellingr
ROLE=dellingr-author
unset IFS

#
# assume the following format:
#
# name: John White
# home: <a href="http://home.cern/">CERN</a>
# orcid: <a href="https://orcid.org/0000-0001-5614-0895">ORCID ID</a>
#  dellingr:
#    role: Project leader, dellingr-author
#
files=`ls -1 $DIRECTORY`
# echo $files

for ffile in $files
do
    # echo $ffile
    grep $PROJECT $ffile > /dev/null 2>&1; result=$?
    if [ $result -eq 0 ] # person is in the project
    then # check if an author
	# echo $ffile
	grep $ROLE $ffile > /dev/null 2>&1; result=$?
	if [ $result -eq 0 ] # person is an author. extract name from the file...
	then
	    nname=`grep 'name\:' $ffile`; # echo $nname
	    name1=${nname#*': '}; # echo Full name $name1; # assume first name family name
	    IFS=' ' # space is set as delimiter
	    read -ra ADDR <<< "$name1" # str is read into an array as tokens separated by IFS
	    first=${ADDR[0]}; # echo First name = $first # Last name is assumed to be the second name
	    last=${ADDR[1]}; # echo Last name = $last
	    # first=${name1%' '}; echo First name = $first
	    # names=($(echo $name1 | tr " " "\n")); echo $names[1]
	    affil=`grep 'home\:' $ffile`; # echo $affil
	    bbb=${affil#*': '}; # echo $bbb # Need to strip away the html tags.
	    aaa=${bbb#\<*\>}; # echo $aaa
	    affiliation=${aaa%\<*\>}; # echo $affiliation
	    orcid1=`grep 'orcid\:' $ffile`; # echo $orcid1
	    orcid2=${orcid1#*'orcid.org/'}; orcid=${orcid2%%'">ORCID'*}; # echo $orcid2
	    echo "$name1 from $affiliation with ORCID $orcid is an $ROLE for the $PROJECT project..."
	    # assume: e.g.
	    # White John,0000-0001-5614-0895,NeIC
	    # Saar Ahti,0000-0003-0642-961X,University of Tartu
            echo $last $first,$orcid,$affiliation >> $OUTPUT_FILE
	fi
    fi
done
