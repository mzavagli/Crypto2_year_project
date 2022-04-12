#!/usr/bin/zsh

python3 GenerateSubTables.py
python3 MergeSubTables.py

if [ $# -lt '1' ]
then
exit
fi

if [ $1 = 'demo' ]
then
python3 ElGamalHomLook.py
fi
