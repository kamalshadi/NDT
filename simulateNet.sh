#!/bin/bash

printf 'You must provide input for reqired fields.
To leave optional fields empty just hit enter\n'
arg=''
# Entering Project name
read -p "Eneter the project name (Required):"  proj 
if [ -z "$proj" ] 
then
	exit 1
fi
# Entering Time
count=0
Error=true
while $Error
do
	read -p "Eneter Time in <yyyy_mo,yyyy_mo ... > (Required):"  table 
	if [ -z "$table" ] 
	then
		exit 1
	fi
	for w in `echo $table |tr ',' '\n'`
	do
		Error=false
		if echo $w | grep -qxo '[0-9]\{4\}_[0-9]\{2\}'
		then
			:
		else
			printf "Sorry your input is not correct, try again or hit enter to exit\n"
			Error=true
			let 'count+=1'
			if [ "$count" -gt "9" ] 
			then
				exit 1
			fi
			break
		fi 
	done
done

arg=$arg" -t $table"

#Enetering prefix
count=0
Error=true
while $Error
do
	read -p "Eneter prefix file(Required):"  inF 
	if [ -a "Inputs/"$inF ]
	then
		prefix=`cat "Inputs/"$inF`
	else
		printf "File doesnot exists\n"
	fi
	for w in `echo $prefix |tr ',' '\n'`
	do
		Error=false
		if echo $w | grep -qxo '[0-9]\{1,3\}\.[0-9]\{1,3\}.[0-9]\{1,3\}\.[0-9]\{1,3\}/[0-9]\{1,2\}'
		then
			:
		else
			printf "Sorry your input is not correct, try again or \n hit enter to search among all prefixes\n"
			Error=true
			let 'count+=1'
			if [ "$count" -gt "9" ] 
			then
			exit 1
			fi
			break
		fi
	done
done



fName=$proj

printf "prefix, uos \n" > CSV/$fName".net"
k=`echo $prefix |tr ',' '\n'|wc -l`
count=0
for w in `echo $prefix |tr ',' '\n'`
do
	printf "___________________________________________\n"
	let count=$count+1
	echo "prefix $count of $k"
	s="./is24.py -p $w"
	eval $s
	if [ $? -eq 11 ]
	then
		printf "$w,['$w']\n" >> CSV/$fName".net"
	else
		arg2=$arg" -f $fName -p $w "
		com="./bqNet.py $arg2"
		echo "Downloading data..."
		eval $com
		echo "Forming uos..."
		s="./allNet.py -f $fName -p $w"
		eval $s
		#~ echo "geolocating clients"
		#~ s="./geoUoSNet.py -f $fName"
		#~ eval $s
	fi
	printf "___________________________________________\n"
done

