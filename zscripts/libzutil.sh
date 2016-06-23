


####################################################################
# Global variables
####################################################################

if [ "$isep" = "" ]
then
	isep="@zitem@"
fi

if [ "$lsep" = "" ]
then
	lsep="@zline@"
fi

if [ "$nonop" = "" ]
then
	nonop=1
fi

if [ "$minpara" = "" ]
then
	minpara=0
fi

if [ "$maxpara" = "" ]
then
	maxpara=100
fi

####################################################################
# A pile of debug functions for inside use 
####################################################################

# Print argument values for debugging use.
# e.g., to print values of var, type: prtarg var,
# which equals to: echo "var = $var".
prtarg()
{
	if [ -z $1 ]
	then
		echo "printarg() function usage error"
		exit 1;
	fi
	echo -n "$1 = "
	eval v='$'$1;
	echo "$v";
}

# Print user-input arguments parsing result.
# Used after parsing
prtparse()
{
	local i
	i=1
	while [ $i -le $optc ]
	do
		getop $i
		prtarg on_$op
		prtarg value_$op
		i=$(($i+1))
	done

	i=1
	while [ $i -le $parac ]
	do
		prtarg para$i
		i=$(($i+1))
	done

}

####################################################################
# A pile of aid functions, only to be used inside 
####################################################################

# Indent a line with spaces
prtnspace()
{
	local i
	i=1
	while [ $i -le $1 ]
	do
		echo -n " "
		i=$(($i+1))
	done
}

zspace_n=44

# Get and print option explanation info by index.
# e.g., to get the explanation for the 2nd option,type " prtoel 2".
# The explanation value will be given to echo,
# as well as stored in a global variable called oel.
prtoel()
{
	id=$1;
	oelt=$optexpl;

	while [ $id -gt 0 ]
	do
		oel=${oelt%%${isep}*}
		oelt=${oelt#*${isep}}	
		conti=`expr substr "$oelt" 1 ${#isep}`
		while [ "$conti" = "$isep" ]
		do
			oel=${oel}"${isep}";
			oelt=${oelt#*${isep}}	
			oel=${oel}${oelt%%${isep}*}
			oelt=${oelt#*${isep}}	
			conti=`expr substr "$oelt" 1 ${#isep}`
		done
		id=$((${id}-1))
	done

	#Now oel contains the explanation info to be printed
	lineno=0
	oelt=$oel
	#Now oelt contains the explanation info to be printed
	while [ ${#oelt} -ne 0 ]
	do
		brkc=`expr match "$oelt" .*${lsep}`
		if [ $brkc -eq 0 ] # oelt may be:case1.one-line explanation;case2. last part of an explanation
		then
			if [ $lineno -ne 0 ] # case2
			then
				prtnspace $zspace_n
			fi
			echo "$oelt"
			break
		fi	

		# $line contains first part of oelt(characters before the first lsep )
		line=${oelt%%${lsep}*}
		
		# $oelt is trucated off first part
		oelt=${oelt#*${lsep}}

		lineno=$(($lineno+1))

		
		conti=`expr substr "$oelt" 1 ${#lsep}`
		while [ "$conti" = "${lsep}" ]
		do
			line=${line}"${lsep}";
			oelt=${oelt#*${lsep}}	
			line=${line}${oelt%%${lsep}*}
			oelt=${oelt#*${lsep}}	
			conti=`expr substr "$oelt" 1 ${#lsep}`
	   done

	  if [ $lineno -ne 1 ]
	  then
		  prtnspace $zspace_n
	  fi
	  echo "$line"
   done
}

# Do programming checks:
# the number of option names, values, and explanations must be equal
# to each other
checkopt()
{
	optc=`echo ${options} | wc -w`; #Num of option names
	loptc=`echo ${loptions} | wc -w`; #Num of option names
	valc=`echo ${values} | wc -w`; #Num of option values
	oelc=0; #Num of option explanations. Waiting to be computed.
	oelt="$optexpl";
	
	while [ ${#oelt} -ne 0 ]
	do
		oelc=$(($oelc+1))
		brkc=`expr match "$oelt" .*${isep}`
		if [ $brkc -eq 0 ] #oelt no longer containes ${isep}
		then
			break;
		fi
		oelt=${oelt#*${isep}}	
		conti=`expr substr "$oelt" 1 ${#isep}`
		while [ "$conti" = ${isep} ] #oelt starts with ${isep} after trucating "*${isep}" pattern
		do
			#a double ${isep} is not interpreted as ${isep} at all	
			oelt=${oelt#*${isep}}	
			oelt=${oelt#*${isep}}	
			conti=`expr substr "$oelt" 1 ${#isep}`
		done
	done

	if [ $optc != $valc -o $optc != $oelc -o $optc != $loptc ]
	then
		echo Programming error. Please check number of options.
		exit 1;
	fi
}

#A function to parse a line into words.
#Usage: getword index line
# index denotes the positon, and the function stores
# the corresponding word into a variable called word
getword()
{
	if [ $# -lt 2 ]
	then
			echo getword function usage error.;
			exit 1;
	fi

	local id;
	eval id='$'$(($1+1))
	word=${id}
}

#A function to get an option name by index, and store it in op
getop()
{
	getword $1 ${options};
	op=${word};
}

#A function to get an long option name by index, and store it in longop
getlongop()
{
	getword $1 ${loptions};
	longop=${word};
}

#A function to get an option value by index, and store it in va
getva()
{
	getword $1 ${values};
	va=${word};
	if [ ${va} = "0" ]
	then
		va="";
	fi
}	



#A function only used inside function zparse_arg() to parse a single argument
get_opt()
{
	ii=1;
	while [ $ii -le $optc ]
	do
		getop $ii; 
		getlongop $ii
		if [ "-$op" = "$carg" -o "--$longop" = "$carg" ] #option matched	
		then
			getva $ii;
			if [ "$va" != "" ] # this option requires a value
			then
				if [ "$nxtarg" = "" ] #this option gets no value
				then
					echo "Option $carg: Missing value"
					echo "Type $cmdname -h for help"
					exit 1;
				fi
				eval value_$op='$nxtarg';
				curind=$(($curind+1));
			fi
			eval on_$op=1;
			break;
		fi
		ii=$(($ii+1));
	done

	if [ $ii -gt $optc ] #No option match found. carg has to be a parameter
	then
		parac=$(($parac+1));
		eval para$parac='$carg';
		if [ $parac -ne 1 ]
		then
			paras="${paras} "
		fi
		paras="${paras}${carg}"
	fi
	curind=$(($curind+1));
}


#Function:Parse user-input arguments
#Input:almost all the global variables
#Outpus:on[] array, value[] array, para[] array, parac
#Fisrt reset the on[] and value[] array to zeros, and later
# set the corrisponding array item according to parsed arguments.
# on[] item set to 1 if corresponding user option is detected
# value[] item is set to corresponding option value
# For detected parameter, write to para[] array and counts them into parac
#NOTICE: dash shell does not support array, so use on_h, on_v...instead of on[1], on[2]
parse_arg()
{
	if [ $# -eq 0 ]
	then
		if [ $nonop != "1" ] # No-opt mode not enabled		
		then
			echo "No option given";
			echo "Type $cmdname -h for help"
			exit 1;
		fi
		if [ $minpara -gt 0 ] # A value required.
		then
			echo "No value given";
			echo "Type $cmdname -h for help"
			exit 1;
		else
			defaultop;
		fi
	fi # if [ $# -eq 0 ]

	#Number of parameters currently recognized
	parac=0;
	#Parameter array as a space-separated line
	paras=""
	#Current index of arguments being parsed
	curind=1;
	
	#Intitialize on[] and value[] array to zeros.
	jj=1;
	while [ $jj -le $optc ]
	do
		getop $jj
		eval on_$op=0
		eval value_$op=0
		jj=$(($jj+1))
	done

	while [ $curind -le $# ]
	do
		eval carg='$'$curind #carg=argv[curind]
		nxtind=$(($curind+1))
		if [ $nxtind -le $# ]
		then
			eval nxtarg='$'$nxtind;
		else
			nxtarg="";
		fi
		get_opt
	done

	if [ $parac -lt $minpara -o $parac -gt $maxpara ]
	then
		echo "Number of parameters($parac) out of range([$minpara, $maxpara])."
		echo "Parameters detected : $paras"
		echo "Type $cmdname -h for help"
		exit 1;
	fi

}


####################################################################
# A pile of util functions that can be called outside 
####################################################################

# Print help info and exit
zusage()
{
	if [ "$formula" != "" ]
	then
		echo "Usage: $formula"
	fi

	echo "Function: $func"

	if [ $optc -gt 0 ]
	then
		echo Options:;
	fi

	ii=1;
	while [ ${ii} -le ${optc} ]
	do
		getop ${ii}
		getva ${ii}
		getlongop $ii
		op="-$op"
		longop="--$longop"
		printf "\t%-6s%-20s%-10s"	"${op}" "${longop}" "${va}" 
		prtoel ${ii}
		ii=$((${ii}+1))
	done
	
	if [ "$version" != "" ]
	then
		echo "Version: $version"
	fi

	if [ "$notice" != "" ]
	then
		echo "Notice: $notice"
	fi

	if [ "$dependlist" != "" ]
	then
		echo "Depend softwares: $dependlist"
	fi

	exit 1;
}

# Print tool's function info and exit
zprtfunc()
{
	echo "${cmdname}: ${func}"
	exit 0
}

if [ $# -eq 1 ]
then
	if [ "$1" = "--prtfunc" ]
	then
		zprtfunc
	fi
fi

# Print tool's version info and exit
zversion()
{
	echo "Version : $version"
	exit 0
}


# Print value of given variable in a human-readable format. 
# Intended to be used for debugging
zprtvar()
{
	if [ $# -gt 0 ]
	then
		prtarg $1;
	fi
}

#Check whether specified software installed
# set global variable is_installed=1 if installed, else set it to 0
zis_installed()
{
	tool=`dpkg -l | grep "\s$1"`
#	tool=`rpm -ql "\s$1"`
	if [ "$tool" = "" ]
	then
		is_installed=0
	else
	  	is_installed=1
	fi
}

zcheck_install()
{
	zis_installed $1
	if [ $is_installed -eq 0 ]
	then
		echo "This script depends on $1, but you do not have $1 installed"
		exit 1;
	fi
}


# Run Unix 'file' command on a file and parse the result, check 
# whether the result contains specified regular expression
zfinfo_contain()
{
	local filename
	local keyword	
	local exam_str
	filename=$1	
	keyword=$2	
	if [ ! -f "$filename" ];then
		echo "Unable to find file "$filename""
		exit 1
	fi
	exam_str=`file "$filename"`
	match_format=`expr match "$exam_str" "$keyword"`
}


####################################################################
#Here we start the main program by checking option designing and
# parsing user-input arguments
####################################################################

#Check for programming error
checkopt; 
#Parse arguments
parse_arg "$@";
#prtparse
