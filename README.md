# exportSGTcounters
Python script for Cat9K container ; reads SGACLS counters, processes then pushes them to ElasticSearch
#
This script is intended to run inside a Cisco Cat9K guestshell container

It reads SGACLS counters, converts the table-like CLI output into individual records,
and pushes them to an elasticsearch repository

It has been tested on IOS-XE 16.11, python 2.7 (IOS-XE 16.11)

Example of Kibana report with Denied/Permit SGTs

<img width="1669" alt="Screenshot 2019-07-03 at 11 16 20" src="https://user-images.githubusercontent.com/22447118/60709521-eb733580-9f10-11e9-81f0-25a0607186c8.png">

Deployment :
1/ copy the file on a Cisco Cat9K swictch (or any IOS-XE platform supporting guestshell and trustsec)

2/ enable guestshell, add the elasticsearch python library

3/ Schedule the script (by using EEM for example)

4/ Configure Kibana to visualize the data

More detailed description here : https://gblogs.cisco.com/ch-tech/trustsec-policy-monitoring-on-a-cat9k/
