BAMF
====

Botnet Attack Modular Framework

BAMF is a modular framework designed to be a platform to launch attacks against botnets.  This framework is more than your usual exploit framework, as botnets have many moving parts and not all attacks are looking to execute code.
This framework will focus on many different things, initially with getting the health of the botnet, information from the botnet, then simple (non-proxied) attacks against the botnet.

Note: Until I have more time to actually design a v1, I will mostly be uploading different PoCs to this repository into the IntegrationQueue folder.  The purpose of the IntegrationQueue is ideas to incorporate into the design.

Parts
=====
At this point in time, I have decided to break BAMF up into multiple interfacing scripts serving different purposes.  This makes designing quite a bit easier and decreases the requirements for a module.  The proposed parts are as follows:

* bamfdetect - Parse binary files and scripts detecting known bots.  Also capable of extracting configuration information from the bot.
* bamfwatch - Parsing pcap or live traffic, identifying known botnet traffic and logging it
* bamfstalk - Monitor the external command structure for a botnet, essentially pretending to be a bot
* bamfbrute - Brute force login credentials to the botnet command and control
* bamfdump - Dump information from the command and control panel (database, credentials, logs, etc)

bamfdetect
----------
bamfdetect is the first to be implemented.  The following are supported modules:

* Dexter
* Madness Pro
* pBot


<pre>cloud@strife:~/git/BAMF$ ./bamfdetect.py -h
usage: ./bamfdetect.py [-h] [-v] [-d] [-r] [-l] [-m MODULE] [path [path ...]]

Identifies and extracts information from bots

positional arguments:
  path                  Paths to files or directories to scan

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -d, --detect          Only detect files
  -r, --recursive       Scan paths recursively
  -l, --list            List available modules
  -m MODULE, --module MODULE
                        Modules to use, if not definedall modules are used

./bamfdetect.py v1.1.0 by Brian Wallace (@botnet_hunter)
</pre>
