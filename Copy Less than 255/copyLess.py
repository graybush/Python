'''
copyLess will take a directory to be copied and looks recursively for files. 
If any files are found that after being copied will have paths greater than 255 characters,
the files will be renamed by striping the shows title from the file name.
'''

import shutil
import os
import sys
import re

def copier(toCopyList, copyTo):
  '''
  checks to see if the path exists, if it does it copies files into the directory
  if the path doesnt exist it makes the dir then performs the copy
  '''
  for tuple in toCopyList:
    if os.path.exists(copyTo):
      if os.path.exists(tuple[1]):
        shutil.copy2(tuple[0], tuple[1] + '\\' + tuple[2])
      else:
        os.mkdir(tuple[1])
        shutil.copy2(tuple[0], tuple[1] + '\\' + tuple[2])
    else:
      os.mkdir(copyTo)
      os.mkdir(tuple[1])
      shutil.copy2(tuple[0], tuple[1] + '\\' + tuple[2])
  
  print('\nFiles copied ... \n')
  sortedList = []
  for tuple in toCopyList:
    sortedList.append(tuple[2])
  sortedList = sorted(sortedList)
  for tuple in sortedList:
    print(tuple)

def fileLen(filePath, copyTo, copyFrom):
  '''
  fileLen checks the fully qualified path for paths over 255 characters
  '''
  filePathLen = len(filePath)
  copyToLen = len(copyTo)
  copyFromLen = len(copyFrom)
  total = filePathLen - copyFromLen + copyToLen
  if total > 255:
    return True
  else:
    return False

def returnContents(path, args):
  '''
  returnContents looks returns a list (fileList) with all of the directory's files
  remove files with following file extensions: par2
  '''
  if args == '--copy':
    fileList = []
    for root, dirs, files in os.walk(path):
      for file in files:
        if file.endswith(".par2"):
          os.unlink(root + '\\' + file)
        else:
          fileList.append(os.path.join(root, file))
    return fileList

  if args == '--rename':
    fileList = []
    for root, dirs, files in os.walk(path):
      for file in files:
        if file.endswith(".par2"):
          os.unlink(root + '\\' + file)
        else:
          a = ((root, file))
          fileList.append(a)
    return fileList
    
def prepare2copy(fileList, copyTo, copyFrom):
  '''
  prepare2copy creates a list of files to be copied
  if the fully qualified path length is greater than 255 it will first rename the file
  '''
  toCopyList = []
  for file in fileList:
    if fileLen(file, copyTo, copyFrom) == False:
    ### If the fully qualified path length is less than 255 copy it
      filename = os.path.split(file)
      a = ((file, copyTo + filename[0][len(copyFrom):], filename[1]))
      toCopyList.append(a)
    elif fileLen(file, copyTo, copyFrom) == True:
    ### If the fully qualified path length is greater than 255 rename then copy it 
      filename = os.path.split(file)
      match = re.search(r'\d\d\d\d.*', filename[1])
      print('\n' + match.group(0))
      userInput = input('\n Approve rename? ')
      userInput = userInput.lower()
      if userInput == 'y':
      ### Getting approval for the file rename
        b = ((file, copyTo + filename[0][len(copyFrom):], match.group(0)))
        toCopyList.append(b)
  return toCopyList

def prepare2rename(fileList):
  '''
  prepare2rename renames obfuscated files using the parent directory as the file name
  '''
  toRenameList = []
  for file in fileList:
    filePath = file[0] + '\\' + file[1]
    a = ((filePath, file[0] + file[0][len(os.path.dirname(os.path.dirname(filePath))):] + file[1][-4:], file[0]))
    toRenameList.append(a)
  return toRenameList

def renamer(toRenameList):
  '''
  renames the files in the directory with the directory name
  '''
  for tuple in toRenameList:
    os.rename(tuple[0], tuple[1])
  print('\nFiles renamed ... \n')
  toRenameList = sorted(toRenameList, key=lambda x: x[1])
  for tuple in toRenameList:
    pathLength = len(tuple[2])
    print(tuple[0][pathLength:] + ' >>> ' + tuple[1][pathLength:] + '\n')


def main():
  args = sys.argv[1:]
  
  if not args:
    print("usage [--copy copyFrom copyTo][--rename copyFrom]")
    sys.exit(1)
  
  if args[0] == '--copy':
    copyFrom = args[1]
    copyTo = args[2]
    fileList = returnContents(copyFrom, args[0])
    toCopyList = prepare2copy(fileList, copyTo, copyFrom)
    copier(toCopyList, copyTo)

  if args[0] == '--rename':
    renameDir = args[1]
    fileList = returnContents(renameDir, args[0])
    toRenameList = prepare2rename(fileList)
    renamer(toRenameList)


if __name__ == '__main__':
  main()