__author__ = 'zbb0263'

import csv
import datetime
import glob
import os
import shutil
import subprocess

def adTimestampToUnix(ad):
    #Convert an 18-digit Windows NT timestamp to a UNIX timestamp
    return int(((ad / 10000000) - 11644473600))

sourceDir = "//cedappidm03/MIIS_scripts/"
destDir = "//cedappidm03/MIIS_scripts/New/CAGAD_Comp.csv"
sourceFile = "//cedappidm03/MIIS_scripts/CAGAD_Comp_raw.csv"
destFile = "//cedappidm03/MIIS_scripts/CAGAD_Comp.csv"
Server = "CEDCAG82.cagdev.conagrafoodsdev.net"
LDAPFilter = "(objectClass=computer)"
LDAPAttributeList = "name,cagSAPCostCenter,cagDeptFunction,location,pwdLastSet,company,whenCreated"

command = "csvde -f %s -s %s -r %s -l %s" % (sourceFile, Server, LDAPFilter, LDAPAttributeList)
subprocess.check_call(command)

with open(sourceFile, 'rt') as file:
    with open(destFile, 'w', newline='') as fileWrite:
        csvFile = csv.reader(file)
        csvWrite = csv.writer(fileWrite, dialect='excel')
        for row in csvFile:
            csvWrite.writerow(row)
            for row in csvFile:
                whenCreated = row[1]
                year = whenCreated[:4]
                month = whenCreated[4:6]
                day = whenCreated[6:8]
                hour = whenCreated[8:10]
                minute = whenCreated[10:12]
                seconds = whenCreated[12:14]
                whenCreated = (month+"/"+day+"/"+year+" "+hour+":"+minute+":"+seconds)
                pwdLastSet = int(row[3])
                pwdLastSet = adTimestampToUnix(pwdLastSet)
                if pwdLastSet < 1:
                    pwdLastSet = ""
                else:
                    pwdLastSet = datetime.datetime.utcfromtimestamp(pwdLastSet).strftime('%Y-%m-%d %H:%M:%S')
                row = (row[0], whenCreated, row[2], pwdLastSet, row[4])
                csvWrite.writerow(row)
os.chdir(sourceDir)
files = glob.glob("CAGAD_Comp_raw.csv")
for filename in files:
    os.unlink(filename)
shutil.copy2(destFile,destDir)
#os.rename(destFile,destDir)