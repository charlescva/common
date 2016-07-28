#!/bin/bash
FILENAME=$1

#colorize
green() { echo "$(tput setaf 2)$*$(tput setaf 9)"; }
red() { echo "$(tput setaf 1)$*$(tput setaf 9)"; }
yellow() { echo "$(tput setaf 3)$*$(tput setaf 9)"; }


# getbytes(skip, length)
function getbytes() {
if [ $3 -eq 0 ]; then
	VAL=$(hexdump -s $1 -n $2 -e '16/1 "%02x"' $FILENAME )
elif [ $3 -eq 1 ]; then
	VAL=$(od -t x -j $1 -N $2 $FILENAME | awk '{for (i=2;i<=NF;i++) printf $i}')
fi
echo $VAL 
}

#strips whitespace
function strip_space() {
	s="$1"
	echo ${s//[[:blank:]]/}
}

#hex to int32
function int32() {
	echo $(perl -le 'print hex("$ARGV[0]")' ${1})
}

#hex to int16
function int16() {
	echo $(perl -le 'print hex("$ARGV[0]")' ${1})
}

#hex to int8
function int8() {
	echo $(perl -le 'print hex("$ARGV[0]")' ${1})
}


#epoch to human
function todate() {
	echo $(date -d @$1)
}

yellow "---------- PCAP File Header (Start) ----------"
echo "PCAP Magic Number  : "$(getbytes 0 4 1)
echo "Major Version      : "$(getbytes 4 2 1)
echo "Minor Vesion       : "$(getbytes 6 2 1)
echo "Time Zone Offset   : "$(getbytes 8 4 1)
echo "Timestamp Accuracy : "$(getbytes 12 4 1)

SNAPLEN=$(int32 "$(getbytes 16 4 1)")
if [ "$SNAPLEN" == "65535" ]; then
	echo "Snapshot Length    : 65535 (Max)"
else
	echo "Snapshot Length    : $SNAPLEN"
fi

LINKTYPE=$(getbytes 20 4 1)
#if [ "$LINKTYPE" == "00000001" ]; then
#	echo "Link-Layer Type    : DLT_EN10MB"
#else
	echo "Link-Layer Type    : $(int32 $LINKTYPE) (www.tcpdump.org/linktypes.html)"
#fi

i=1

nextbyte=24
yellow "---------- PCAP File Header (End) ----------"
echo
FILESIZE=$(stat -c%s "$FILENAME")

while [ $nextbyte -lt $FILESIZE ]
do
	green "|--------------------| Frame #$i |-----------------------|"
	TIMESTAMP=$(int32 $(getbytes $nextbyte 4 1 0))
	echo "|Timestamp          : "$(todate $TIMESTAMP)
	nextbyte=$((nextbyte + 4))
	echo "|Timestamp Epoch    : "$TIMESTAMP.$(int32 $(getbytes $nextbyte 4 1 0))
	nextbyte=$((nextbyte + 4))
	PACKET_LENGTH=$(int32 $(getbytes $nextbyte 4 1 0))
	nextbyte=$((nextbyte + 4))
	echo "|Frame Length       : "$PACKET_LENGTH
	echo "|Capture Length     : "$(int32 $(getbytes $nextbyte 4 1 0))
	nextbyte=$((nextbyte + 4))
	
	green "|-----------------| Ethernet II Frame |-----------------|"
	echo "|Destination MAC    : "$(getbytes $nextbyte 6 0)
	nextbyte=$((nextbyte + 6))
	echo "|Source MAC         : "$(getbytes $nextbyte 6 0)
	nextbyte=$((nextbyte + 6))
	echo "|Type               : "$(getbytes $nextbyte 2 0)
	nextbyte=$((nextbyte + 2))
	
	
	green "|----------------| Internet Protocol |------------------|"
	#Skipping Differentiated Service Field
	nextbyte=$((nextbyte + 2))
	IP_PACKET_LENGTH=$(int16 $(getbytes $nextbyte 2 0))
	echo "|Total Length       : "$IP_PACKET_LENGTH
	nextbyte=$((nextbyte + 2))
	echo "|Identification     : "$(int32 $(getbytes $nextbyte 2 0))
	nextbyte=$((nextbyte + 2))
	#Skipping Flags/Fragoffsets
	nextbyte=$((nextbyte + 2))
	echo "|TTL                :" $(int8 $(getbytes $nextbyte 1 0))
	nextbyte=$((nextbyte + 1))
	PROTOCOL=$(int8 $(getbytes $nextbyte 1 0))
	if [ $PROTOCOL -eq 6 ]; then
		echo "|Protocol           : TCP (6)"
	else
		echo "|Protocol           : "$PROTOCOL
	fi
	nextbyte=$((nextbyte + 1))
	#Skipping Header/Checksum
	nextbyte=$((nextbyte + 2))
	echo "|Source IP          : "$(printf "%d." $(echo $(getbytes $nextbyte 4 0) | sed 's/../0x& /g' | tr ' ' '\n') | sed 's/\.$/\n/')
	nextbyte=$((nextbyte + 4))
	echo "|Destination IP     : "$(printf "%d." $(echo $(getbytes $nextbyte 4 0) | sed 's/../0x& /g' | tr ' ' '\n') | sed 's/\.$/\n/')
	nextbyte=$((nextbyte + 4))

	green "|--------| TCP (Transmission Control Protocol) |--------|"
	echo "|Source Port        : "$(int32 $(getbytes $nextbyte 2 0))
	nextbyte=$((nextbyte + 2))
	echo "|Destination Port   : "$(int32 $(getbytes $nextbyte 2 0))
	nextbyte=$((nextbyte + 2))
	echo "|Sequence Num       : "$(getbytes $nextbyte 4 0)
	nextbyte=$((nextbyte + 4))
	echo "|Ack Number         : "$(getbytes $nextbyte 4 0)
	nextbyte=$((nextbyte + 4))
	# Skipping offset, flags, reserved, sliding window for now
	nextbyte=$((nextbyte + 4))
	echo "|Checksum           : "0x$(getbytes $nextbyte 2 0)
	nextbyte=$((nextbyte + 2))
	echo "|Urgent Pointer     : "$(getbytes $nextbyte 2 0)
	nextbyte=$((nextbyte + 2))
	# Skipping options and padding
	nextbyte=$((nextbyte + 12))		
	
	green "|------------------| End Frame #$i |---------------------|"
	let i=i+1

	echo $nextbyte
	echo $SNAPLEN
	if [ $nextbyte -gt $SNAPLEN ]; then
		exit
	fi
	
done
