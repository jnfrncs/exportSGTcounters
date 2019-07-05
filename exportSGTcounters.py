"""
    Export the SGACLs counters from a 9K switch
    
    tested on a 9300 running 16.11
    requires the elasticsearch library

"""

__author__      = "Jean-Francois Pujol, Cisco Switzerland"
__copyright__   = "Copyright (c) 2019 Cisco and/or its affiliates."
__version__     = 1.0

"""
Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import cli # available within guestshell only
import time
from elasticsearch import Elasticsearch

# IP address / host running elasticsearch, credentials and index name
ELASTIC_HOST='172.16.90.9'
ELASTIC_CREDS='elastic:changeme'
ELASTIC_INDEX='sgacls'

"""
    From the IOS-XE command line output text (hits per SGT in a table style),
    creates a list of records (one per src / dst SGT combination)
    Translates the SGT number into clear text when available
"""
def showCtsCounters2Table(cliOutput):

    records = []
    if len(cliOutput) > 30:
        lines = cliOutput.split('\n')
        coln = len(lines[0])
        lnn = len(lines)
        if coln < 8 or lnn < 3:
            return(records) # nothing to extract
        
        headers = lines[1].lower().split() 
        formatedDate = time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        ctsDict = getSGTenvironment()
        
        for i in range(2,lnn):
            # for each line in the output table (excepted the headers)
            items = lines[i].split()
            sgtCnts = {}
            for j in range(len(items)):
                sgtCnts[headers[j]] = items[j]
            
            # additional infos added to the record
            sgtCnts['datetime'] = formatedDate
            sgtCnts['hostname'] = hostname()
            
            # adding SGT tags in cleartext (when available)
            if 'from' in sgtCnts.keys():
                if sgtCnts['from'] in ctsDict.keys():
                    sgtCnts['fromtxt'] = ctsDict[sgtCnts['from']]
            if 'to' in sgtCnts.keys():
                if sgtCnts['to'] in ctsDict.keys():
                    sgtCnts['totxt'] = ctsDict[sgtCnts['to']]

            records.append(sgtCnts)
            
    return(records)

"""
    Gets the name of the switch where the script executes
"""
def hostname():
    showver = cli.execute("show version")
    for line in showver.split('\n'):
        tokens = line.split()
        if len(tokens) > 2:
            if tokens[1] == 'uptime':
                return(tokens[0])
                break
    return('switch')

"""
    Creates a dictionnary with the name of each SGT 
"""
def getSGTenvironment():
    
    ctsEnvCommand = cli.execute('show cts environment')
    ctsDict = {'*' : 'Any'}

    for line in ctsEnvCommand.split('\n'):
        tok1 = line.split('-')
    
        if len(tok1) > 1:
            tok2 = tok1[1].split(':')
        else:
            tok2 = {}
        
        if len(tok2) == 2:
            ctsDict[tok1[0].strip()] = tok2[1].strip()
    
    return(ctsDict)

"""
    Main procedure : converts the cli output to a list of records,
    then push the records to elasticsearch

"""
def Main():

    es = Elasticsearch('http://' + ELASTIC_CREDS + '@' + ELASTIC_HOST + ':9200/')
    SGTcounters = cli.execute('show cts role-based counters')
    daclCounters = showCtsCounters2Table(SGTcounters)
    idx = int(time.time())
    for record in daclCounters:
        res = es.index(index=ELASTIC_INDEX, doc_type='counters', id=idx, body=record)
        idx +=1
        
    rs = cli.execute('clear cts role-based counters')

if __name__ == '__main__':
    Main()
