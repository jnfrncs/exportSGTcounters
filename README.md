# exportSGTcounters
Python script for Cat9K container ; reads SGACLS counters, processes then pushes them to ElasticSearch
#
This script is intended to run inside a Cisco Cat9K guestshell container

It reads SGACLS counters, converts the table-like CLI output into individual records,
and pushes them to an elasticsearch repository

It has been tested on IOS-XE 16.11, python 2.7 (IOS-XE 16.11)

<img width="1669" alt="Screenshot 2019-07-03 at 11 16 20" src="https://user-images.githubusercontent.com/22447118/60709521-eb733580-9f10-11e9-81f0-25a0607186c8.png">
