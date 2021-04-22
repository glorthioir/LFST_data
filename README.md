# LFST_data
This repository contains the necessary code to generate the data used in the paper: 

Python 3 was used for the implementation.

To generate the data you just need to type the command: python mainTest.py
Three files will be generated:
-----> grid_data.txt
-----> cube_data.txt
-----> 421_data.txt

They contain the traces for their respective environment (see the paper). The data are also available inside different lists in the code so you can modify the file "mainTest.py" and directly used them instead of using the txt files.

PS: There is currently an infinite loop that happens in the script sometimes due to the generation of one of the environment (CubeWorld) that use random generators, if it happens just run the file again, it usually does not happen more than two or three consecutive times (the script finishes in 2 or 3 second usually).
