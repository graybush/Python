### copyLess will take a directory to be copied and look recursively for files. 
###If any files are found that after being copied will have paths greater than 255 characters,
### the files will be renamed by striping the shows title from the file name.

import shutil
import os
import sys
import re

def returnContents(path):
### returnContents looks returns a list (fileList) with all of the directory's files
  fileList = []
  for root, dirs, files in os.walk(path):
    for file in files:
      #if file.endswith(".mp3"):
      fileList.append(os.path.join(root, file))
  return fileList
    
def fileLen(copyFrom, copyTo):
### fileLen checks the fully qualified path for paths over 255 characters
  copyFromLen = len(copyFrom)
  copyToLen = len(copyTo)
  total = copyFromLen + copyToLen
  if copyFromLen + copyToLen > 255:
    return True
  else:
    return False


def main():
  if len(sys.argv) != 3:
    print('usage: ./copyLess.py copyFrom copyTo')
    sys.exit(1)
  copyFrom = sys.argv[1]
  copyTo = sys.argv[2]
  
  fileList = returnContents(copyFrom)
  toCopyList = []

  for file in fileList:
  ### Look at the first file, do you want to copy it?
    print('\n' + file)
    userInput = input('\n Approve copy? ')
    userInput = userInput.lower()
    if userInput == 'y':
	### If yes, then check the fully qualified path length
      if fileLen(file, copyTo) == False:
	  ### If the fully qualified path length is less than 255 copy it
        filename = os.path.split(file)
        a = ((file, copyTo + '\\' + filename[0], filename[1]))
        toCopyList.append(a)
      elif fileLen(file, copyTo) == True:
      ### If the fully qualified path length is greater than 255 rename then copy it 
        filename = os.path.split(file)
        match = re.search(r'\d\d\d\d.*', filename[1])
        print('\n' + match.group(0))
        userInput = input('\n Approve rename? ')
        userInput = userInput.lower()
        if userInput == 'y':
        ### Getting approval for the file rename
          b = ((file, copyTo + '\\' + filename[0], match.group(0)))
          toCopyList.append(b)
  
  for tuple in toCopyList:
    if os.path.exists(tuple[1]):
      shutil.copy2(tuple[0], tuple[1] + '\\' + tuple[2])
    else:
      os.mkdir(tuple[1])
      shutil.copy2(tuple[0], tuple[1] + '\\' + tuple[2])
  
  print('\nFiles copied ... \n')
  for tuple in toCopyList:
    print(tuple[2])

if __name__ == '__main__':
  main()