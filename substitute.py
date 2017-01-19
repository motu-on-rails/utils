import os
import errno
import sys
import re
import codecs
from glob import glob
from os.path import splitext
from time import sleep

#dir = None
src_file_ext = 'sql'
tgt_file_ext = '.SIT.sql'
sit_dir = '__SIT'
single_insert_all = '__SINGLE_INSERT_ALL__'
patterns = {  'subs_from': 'subs_to', 'subs_from2': 'subs_to2', 'subs_from3': 'subs_to3'}

def substitute (file, patterns):
  filedata = None
  with codecs.open(file, 'r', 'utf-8') as file:
    filedata = file.read()
  
  for repl_from, repl_to in patterns.items():      
    filedata = re.sub(repl_from, repl_to, filedata, flags=re.I)

  return filedata
  
def write_file(file, filedata, tgt_dir, ext=tgt_file_ext):
  file_name, extension = splitext(file)
  file_base = os.path.basename(file_name)
  with codecs.open(tgt_dir + '\\' + file_base + ext, 'w', 'utf-8') as file:
    file.write(filedata)

  with codecs.open(tgt_dir + '\\' + single_insert_all + ext, 'a', 'utf-8') as file:
    file.write("\n--######### SQL FILE #############--")
    file.write("\nprint '###########" + file_name + extension + "';\n")
    file.write(filedata)
  return

def remove_files_in(dir):
  if os.path.exists(dir):
    try:
      raw_input("Will remove files in dir: " + dir)
      files_to_remove = [f for f in os.listdir(dir)]
      for f in files_to_remove:
        os.remove(sit_dir + '\\' + f)
    except OSError as e:
      print "ERROR: can't delete single file"
      print e
      raise

def create_dir(dir):
  if not os.path.exists(dir):
    try:
      print ("Creating a directory: " + dir)
      os.makedirs(dir)
    except OSError as exc: # Guard against race condition
      if exc.errno != errno.EEXIST:
        raise

def get_dir():
  print ("This script prepares configuration files for SIT environment..")
  dir = raw_input("Please enter directory with configuration files: ")
  print "\n" + dir
  raw_input ("\nHit Enter button if the path is correct, or Cntrl + C to cancel execution.")
  if not os.path.exists(dir):
      raw_input("Directory does not exist. Hit Enter to stop execution.")
      exit()
  return dir
  
def main():

  global sit_dir
  filedata = None

  dir = get_dir()
  sit_dir = dir + '\\' + sit_dir
  
  create_dir(sit_dir)
  remove_files_in(sit_dir)

  files = glob(dir + '\*' + src_file_ext)

  for file in files:
    try:
      filedata = substitute(file, patterns)
      write_file(file, filedata, sit_dir)
    except UnicodeDecodeError as e:
      print "\nNeed to manually convert to utf-8, file: \n", file
      print "\nError message", e
      raw_input ("Hit Enter.")
      exit()

if __name__ == "__main__":
  main()
