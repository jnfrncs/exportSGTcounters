# exportSGTcounters
Python script for Cat9K container ; reads SGACLS counters, processes then pushes them to ElasticSearch
#
This script is intended to run inside a Cisco Cat9K guestshell container

It reads SGACLS counters, converts the table-like CLI output into individual records,
and pushes them to an elasticsearch repository

It has been tested on IOS-XE 16.11, python 2.7 (IOS-XE 16.11)
