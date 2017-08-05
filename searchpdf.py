# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 15:13:20 2017

@author: DELL PM
"""

import os
import errno
import glob
import subprocess, shlex
from pathlib import PurePath
import sys
import itertools
import string
import traceback


class pdf(object):
    def __init__(self, input_path):
        self.input_path = input_path
        
    def is_exe(self,fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK) and os.access(fpath, os.F_OK) 

    def which_win(self, program):
        

        fpath, fname = os.path.split(program)
        if fpath:
            if self.is_exe(program):
                return program
        else:
            environ_keys = [key for key in os.environ.keys()]
            for path in list(itertools.chain(*[os.environ[key].split(os.pathsep) for key in environ_keys])):
                path = path.strip('"')
                if program == 'tesseract.exe':
                    file_with_exe = '/Tesseract-OCR'
                    len_of_file_name = len(file_with_exe)
                    if path[-len_of_file_name:] == file_with_exe:
                        exe_file = os.path.join(path, program)
                    else:
                        path += file_with_exe
                        exe_file = os.path.join(path, program)
                        if self.is_exe(exe_file):
                                   return exe_file
                elif program == 'gswin64c.exe' or 'gswin32c.exe':
                    if '/gs/' in path:
                        if path[-3:] == 'bin':
                            file_with_exe = path
                        else:
                            file_with_exe = str(PurePath(glob.glob(path + '/bin')[0]))
                    elif path[-3:] == '/gs':

                        file_with_exe = str(PurePath(glob.glob(path + '/gs*/bin')[0]))
                    else:
                        if os.path.isdir(path + '/gs'):

                            file_with_exe = str(PurePath(glob.glob(path + '/gs/gs*/bin')[0]))
                        else:

                            continue
                    exe_file = os.path.join(file_with_exe, program)
                    if self.is_exe(exe_file):
                        return exe_file
                else:

                    return None

    def transform(self):
        try:
 
            inpath = self.input_path
            cwd = os.getcwd()
            if inpath=='':
                inpath=cwd
            path = PurePath(inpath)
            
            if path.suffix != '':

                if path.suffix != '.pdf':

                    raise ValueError("The input file is not a pdf file")

                else:
                    if '\\' not in str(path):

                               l = [cwd+'\\'+str(path)]
                    else:
                               l = [str(path)]

            else:

                if str(path) != cwd :

                    l = [str(PurePath(file)) for file in glob.glob(inpath + "/*.pdf")]
          
                else:

                    l = [file for file in glob.glob("*.pdf")]

                if l == []:
                    raise ValueError("No pdf files in this directory")

            if os.name == 'nt':
                if self.is_exe(str(PurePath(glob.glob('C:/Program Files/gs/gs*/bin/gswin64c.exe')[0]))):
                    dirg=str(PurePath(glob.glob('C:/Program Files/gs/gs*/bin/gswin64c.exe')[0]))
                elif self.is_exe(str(PurePath(glob.glob('C:/Program Files/gs/gs*/bin/gswin32c.exe')[0]))):
                    dirg=str(PurePath(glob.glob('C:/Program Files/gs/gs*/bin/gswin32c.exe')[0]))
                else:
                    if self.which_win('gswin64c.exe') is not None:
                        dirg = str(PurePath(self.which_win('gswin64c.exe')))
                        
                    elif self.which_win('gswin32c.exe') is not None:
                        dirg = str(PurePath(self.which_win('gswin64c.exe')))
                    else:
                        dis_seg=list(string.ascii_lowercase)
                        segs=[]
                        for l in dis_seg:
                            k=glob.glob(l+":\\")
                            segs+=k
                        for seg in segs:
                            for r,d,f in os.walk(seg):
                                for files in f:
                                    if files == "gswin64c.exe" or files == "gswin32c.exe":
                                         if self.is_exe(os.path.join(r,files)):
                                                         dirg=str(PurePath(os.path.join(r,files)))
                
                if dirg is None:
                        sys.exit("Please install Ghostscript, if you want to complete this task")
                
                if self.is_exe(str(PurePath('C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'))):
                    dirt=str(PurePath('C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'))
                
                elif self.is_exe(str(PurePath('C:/Program Files/Tesseract-OCR/tesseract.exe'))):
                    dirt=str(PurePath('C:/Program Files/Tesseract-OCR/tesseract.exe'))
                    
                else:
                    if self.which_win('tesseract.exe') is not None:
                        dirt = str(PurePath(self.which_win('tesseract.exe')))
                        
                   
                    else:
                        dis_seg=list(string.ascii_lowercase)
                        segs=[]
                        for l in dis_seg:
                            k=glob.glob(l+":\\")
                            segs+=k
                        for seg in segs:
                            for r,d,f in os.walk(seg):
                                for files in f:
                                    if files == "tesseract.exe" :
                                        if self.is_exe(os.path.join(r,files)):
                                              dirt=str(PurePath(os.path.join(r,files)))
                    
                if dirt is None: 
                            sys.exit("Please install Tesseract-OCR, if you want to complete this task")
               
                for inp in l:
                     si = subprocess.STARTUPINFO()
                     si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                     directory = str(PurePath(inp).parent)
                     inp = PurePath(inp).name
                     try:
                        
                        call = PurePath(dirg).name
                        call = call.split('.')[0]
                        outp = inp.split('.')[0] + '.tiff'
                        command_line = call + ' -q -r300 -dNOPAUSE -sDEVICE=tiffgray -dBATCH -dINTERPOLATE -o ' + outp + ' -f ' + inp + ' -c quit'
                        args = shlex.split(command_line)
                        proc = subprocess.Popen(args, executable=dirg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                cwd=directory,startupinfo=si)
                                        
                        proc.wait()
                     except:
                         
                         print ("Error while running Ghostscript subprocess. Traceback:")
                         print ("Traceback:\n%s"%traceback.format_exc())
                         
                     stdout, stderr = proc.communicate()
                     if stderr:
                         print ("Ghostscript stderr:\n'%s'" % stderr)
                     try:
                         read_pdf=outp.split('.')[0]+'_new'
                         command_line1='tesseract '+outp+' '+read_pdf+' pdf'
                         args1= shlex.split(command_line1)
                         proc1=subprocess.Popen(args1 ,executable=dirt, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,cwd=directory,startupinfo=si)
                         proc1.wait()
                     except:
                         
                         print ("Error while running Tesseract subprocess. Traceback:")
                         print ("Traceback:\n%s"%traceback.format_exc())
                         
                     stdout1, stderr1 = proc1.communicate()
                     if stderr1:
                         print ("Tesseract stderr:\n'%s'" % stderr1)    
                        
                     try:
                            os.remove(directory+'\\'+outp)
                     except OSError:
                            
                            raise
                     


            elif os.name == 'posix':
                if os.path.isfile(PurePath("/usr/local/bin/gs")):
                    dirg = str(PurePath("/usr/local/bin/gs"))
                else:
                   for r,d,f in os.walk('/usr'):  
                           for files in f:
                               if files == 'gs':
                                 if self.is_exe(os.path.join(r,files)):
                                              dirg=os.path.join(r,files)
                   if dirg is None:                           
                       for r,d,f in os.walk('/'):  
                          for files in f:
                             if files == 'gs':
                                 if self.is_exe(os.path.join(r,files)):
                                              dirg=os.path.join(r,files)
                if dirg is None:
                        sys.exit("Please install Ghostscript, if you want to complete this task")
                        
                if os.path.isfile(PurePath("/usr/local/bin/tesseract")):
                    dirt = str(PurePath("/usr/local/bin/tesseract"))
                else:    
                    for r,d,f in os.walk('/usr'):  
                           for files in f:
                               if files == 'tesseract':
                                 if self.is_exe(os.path.join(r,files)):
                                              dirt=os.path.join(r,files)
                    if dirt is None:    
                       for r,d,f in os.walk('/'):  
                           for files in f:
                               if files == 'tesseract':
                                 if self.is_exe(os.path.join(r,files)):
                                              dirt=os.path.join(r,files)
                if dirt is None:
                            sys.exit("Please install Tesseract, if you want to complete this task")
                        
                        
                for inp in l:
                     si = subprocess.STARTUPINFO()
                     si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                     directory = str(PurePath(inp).parent)
                     inp = PurePath(inp).name
                     try:
                        outp = inp.split('.')[0] + '.tiff'
                        command_line = 'gs -q -r300 -dNOPAUSE -sDEVICE=tiffgray -dBATCH -dINTERPOLATE -o ' + outp + ' -f ' + inp + ' -c quit'
                        args = shlex.split(command_line)
                        proc = subprocess.Popen(args, executable=dirg, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                                cwd=directory,startupinfo=si)
                                        
                        proc.wait()
                     except:
                         
                         print ("Error while running Ghostscript subprocess. Traceback:")
                         print ("Traceback:\n%s"%traceback.format_exc())
                         
                     stdout, stderr = proc.communicate()
                     if stderr:
                         print ("Ghostscript stderr:\n'%s'" % stderr)
                     try:
                         read_pdf=outp.split('.')[0]+'_new'
                         command_line1='tesseract '+outp+' '+read_pdf+' pdf'
                         args1= shlex.split(command_line1)
                         proc1=subprocess.Popen(args1 ,executable=dirt, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,cwd=directory,startupinfo=si)
                         proc1.wait()
                     except:
                         
                         print ("Error while running Tesseract subprocess. Traceback:")
                         print ("Traceback:\n%s"%traceback.format_exc())
                         
                     stdout1, stderr1 = proc1.communicate()
                     if stderr1:
                         print ("Tesseract stderr:\n'%s'" % stderr1)    
                        
                     try:
                            os.remove(directory+'\\'+outp)
                     except OSError:
                            
                            raise
                         

            else:
                sys.exit('Only for Windows or Linux')


        except OSError as error:

            if error.errno == errno.ENOENT:
                raise FileNotFoundError()

            elif error.errno in [errno.EPERM, errno.EACCES]:
                raise PermissionError()
                
            else:
                raise

        return "1"


 