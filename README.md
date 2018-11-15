# LMAP

In this project we've implemented two different attacks that achieve to obtain the secret ID used in the LMAP protocol proposed by Peris-Lopez et al. [(Paper available here)](https://www.researchgate.net/publication/228766102_LMAP_A_real_lightweight_mutual_authentication_protocol_for_low-cost_RFID_tags) 

First, we implemented the attack described in ["Breaking LMAP"](https://www.researchgate.net/publication/267305720_Breaking_LMAP).

Then, a tango attack was written as well. 

To run start tag.py and LMAP.py

`python3 tag.py`
`python3 LMAP.py`

### Attacker

This scripts simulates the attack described in the first paper, to run it, the user must simply execute it with python. The script will automatically listed the communications between the reader and the tag and print the results.

`python3 attacker.py`

### tangoAttacker
This attacker takes as input argument the tags ID number in order to perform calculations. Get this ID from the terminal when starting tag.py
To run it use:

`python3 tangoAttacker.py <ID>`

### Requirements:
`BitVector`
