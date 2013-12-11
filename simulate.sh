#!/bin/bash

printf 'You must provide input for reqired fields.
To leave optional fields empty just hit enter\n'
arg=''
# Entering Project name
read -p "Eneter the project name (optional):"  proj 
read -p "Plot data on google map(y/n)?:"  ply
# Entering Time
count=0
Error=true
while $Error
do
read -p "Eneter Time in <yyyy_mo,yyyy_mo ... > (Required):"  table 
if [ -z "$table" ] 
then
	exit 1
elif [ $table == "f" ]
then
read -p "Eneter Filename:"  inF
if [ -a "Inputs/"$inF ]
then
table=`cat "Inputs/"$inF`
else
printf "File doesnot exists\n"
fi
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

fName=$table
arg=$arg" -t $table"

#Enetering prefix
count=0
Error=true
while $Error
do
read -p "Eneter prefix in <x.x.x.x/x,x.x.x.x/x ... > (Optional):"  prefix 
if [ -z "$prefix" ] 
then
break
elif [ $prefix == "f" ]
then
read -p "Eneter Filename:"  inF
if [ -a "Inputs/"$inF ]
then
prefix=`cat "Inputs/"$inF`
else
printf "File doesnot exists\n"
fi
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
if [ -n "$prefix" ]
then
fName=$fName"-ip-"$prefix
arg=$arg" -p $prefix"
fi


#Enetering server prefix
count=0
Error=true
while $Error
do
read -p "Eneter Server prefix <x.x.x.x/x,x.x.x.x/x ... > (Optional):"  server 
if [ -z "$server" ] 
then
break
elif [ $server == "f" ]
then
read -p "Eneter Filename:"  inF
if [ -a "Inputs/"$inF ]
then
server=`cat "Inputs/"$inF`
else
printf "File doesnot exists\n"
fi
fi
for w in `echo $server |tr ',' '\n'`
do
Error=false
if echo $w | grep -qxo '[0-9]\{1,3\}\.[0-9]\{1,3\}.[0-9]\{1,3\}\.[0-9]\{1,3\}/[0-9]\{1,2\}'
then
	:
else
printf "Sorry your input is not correct, try again or \n hit enter to search among all servers\n"
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
if [ -n "$server" ]
then
fName=$fName"-server-"$server
arg=$arg" -s $server"
fi


#Eneter Continents

count=0
Error=true
while $Error
	do
	read -p "Eneter continents in <con1,con2 ... > (Optional):"  con1
	if [ -z "$con1" ]  
		then
		con=$con1
		break
	elif [ $con1 == "f" ]
		then
		read -p "Eneter Filename:"  inF
		if [ -a "Inputs/"$inF ]
		then
		con1=`cat "Inputs/"$inF`
		else
		printf "File doesnot exists\n"
		fi
	fi
	if echo $con1 |grep -Fqxo '?'
	then
	arg=$arg" -l ?"
	break
	fi
	con=''
	for w in `echo $con1 |tr ' ,' '-\n'`
		do
		nfound=true
		for temp in `cat Files/continents|tr ' ' '-'`
			do
			if echo $w|grep -qxi $temp
				then
				nfound=false
				if [ -z "$con" ]
				then
					con=`echo "$temp"|tr '-' ' '`
				else
					con=`echo "$con","$temp"|tr '-' ' '`
				fi
				break
			else
				:
			fi
		done
		if $nfound
		then
			con=''
			printf "Sorry your input is not correct, try again or \n hit enter to search among all continentss\n"
			Error=true
			let 'count+=1'
			if [ "$count" -gt "9" ]
			then
				exit 1
			fi
			break
		else
			Error=false
		fi 
	done
	arg=$arg" -l $con"
done
if [ -n "$con" ] && !  echo $con1 |grep -Fqxo '?'
then
fName=$fName"-con-"$con
arg=$arg" -l $con"
fi



#Entering Country

count=0
Error=true
while $Error
	do
	read -p "Eneter countires in <country1,country2 ... > (Optional):"  country1
	if [ -z "$country1" ] 
		then
		country=$country1
		break
	elif [ $country1== "f" ]
		then
		read -p "Eneter Filename:"  inF
		if [ -a "Inputs/"$inF ]
		then
		country1=`cat "Inputs/"$inF`
		else
		printf "File doesnot exists\n"
		fi
	fi
	if  echo $country1 |grep -Fqxo '?'
		then
		arg=$arg" -k ?"
		break
	fi
	country=''
	for w in `echo $country1 |tr ' ,' '-\n'`
		do
		nfound=true
		for temp in `cat Files/countries|tr ' ' '-'`
			do
			if echo $w|grep -qxi $temp
				then
				nfound=false
				if [ -z "$country" ]
				then
					country=`echo "$temp"|tr '-' ' '`
				else
					country=`echo "$country","$temp"|tr '-' ' '`
				fi
				break
			else
				:
			fi
		done
		if $nfound
		then
			country=''
			printf "Sorry your input is not correct, try again or \n hit enter to search among all countries\n"
			Error=true
			let 'count+=1'
			if [ "$count" -gt "9" ]
			then
				exit 1
			fi
			break
		else
			Error=false
		fi 
	done
done
if [ -n "$country" ] && !  echo $country1 |grep -Fqxo '?'
then
fName=$fName"-country-"$country
country=`echo $country| sed 's/ /\\\ /'`
arg=$arg" -k $country"
fi

#Entering region

count=0
Error=true
while $Error
	do
	read -p "Eneter regions in <region1,region2 ... > (Optional):"  region1
	if [ -z "$region1" ] 
		then
		region=$region1
		break
	elif [ $region1== "f" ]
		then
		read -p "Eneter Filename:"  inF
		if [ -a "Inputs/"$inF ]
		then
		region1=`cat "Inputs/"$inF`
		else
		printf "File doesnot exists\n"
		fi
	fi
	if echo $region1 |grep -Fqxo '?'
	then
	arg=$arg" -r ?"
	break
	fi
	region=''
	for w in `echo $region1 |tr ' ,' '-\n'`
		do
		nfound=true
		for temp in `cat Files/regions|tr ' ' '-'`
			do
			if echo $w|grep -qxi $temp
				then
				nfound=false
				if [ -z "$region" ]
				then
					region=`echo "$temp"|tr '-' ' '`
				else
					region=`echo "$region","$temp"|tr '-' ' '`
				fi
				break
			else
				:
			fi
		done
		if $nfound
		then
			region=''
			printf "Sorry your input is not correct, try again or \n hit enter to search among all regions\n"
			Error=true
			let 'count+=1'
			if [ "$count" -gt "9" ]
			then
				exit 1
			fi
			break
		else
			Error=false
		fi 
	done
done
if [ -n "$region" ] && !  echo $region1 |grep -Fqxo '?'
then
fName=$fName"-state-"$region
arg=$arg" -r $region"
fi

#Entering city

count=0
Error=true
read -p "Eneter cities in <city1,city2 ... > (Optional):"  city
if [ -n "$city" ] && !  echo $city |grep -Fqxo '?'
then
fName=$fName"-city-"$city
city=`echo $city| sed 's/ /\\\ /'`
arg=$arg" -c $city"
fi
if [ -n "$city" ] &&  echo $city |grep -Fqxo '?'
then
arg=$arg" -c $city"
fi
fName=`echo $fName|sed 's/ //g'|tr ',' '~'|tr '/' 's'`
fName=${fName:0:150}
if [ -z proj ]
then
:
else
fName=$proj
fi
arg=$arg" -f $fName"
w="./bq.py $arg"
echo "Downloading data..."
eval $w

echo "Forming NG graph:"
s="./graph.py -f $fName"
eval $s
if [ $? -eq 11 ]
then
echo 'Sorry, There is not enough data for your inputs to form clusters'
else
echo "Clustering..."
s="./cluster.py -f $fName"
eval $s
echo "geolocating clients"
s="./geoUoS.py -f $fName"
eval $s
if [ $ply == 'y' ] || [ $ply == 'Y' ];
then
echo "Ploting Geolocations"
s="./geoPlot.py -f $fName"
eval $s
fi
fi

