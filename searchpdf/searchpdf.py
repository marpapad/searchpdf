# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 00:43:53 2017

@author: DELL PM
"""

import os

import errno

import glob

import subprocess, shlex

from pathlib import PurePath

import sys

import itertools

import traceback

import click


class pdf(object):
    def __init__(self, input_path):

        self.input_path = input_path

    def is_exe(self, fpath):

        return os.path.isfile(fpath) and os.access(fpath, os.X_OK) and os.access(fpath, os.F_OK)

    def which_win(self,program):

            environ_keys = [key for key in os.environ.keys()]
            for path in list(itertools.chain(*[os.environ[key].split(os.pathsep) for key in environ_keys])):

                path = path.strip('"')

                if program == 'tesseract.exe':

                    file_with_exe = '/Tesseract-OCR'

                    len_of_file_name = len(file_with_exe)

                    if path[-len_of_file_name:] == file_with_exe:
                        exe_file = os.path.join(path, program)

                    elif os.path.isdir(path + file_with_exe):
                        exe_file = os.path.join(path + file_with_exe, program)



                elif program == 'gswin64c.exe' or program == 'gswin32c.exe':

                    if '/gs/' in path and path[-3:] == 'bin':
                        exe_file = os.path.join(path, program)

                    elif os.path.isdir(path + '/gs'):
                        exe_file = os.path.join(str(PurePath(glob.glob(path + '/gs/gs*/bin')[0])), program)
                else:
                    exe_file=''
            if self.is_exe(exe_file):
                return exe_file
    
    def transform(self):

        try:
            inpath = self.input_path
            l=[]
            if os.path.isabs(inpath):
                file_or_dir = os.path.splitext(inpath)[1]
                if file_or_dir == '' and os.path.isdir(os.path.realpath(inpath)):
                    l = [file for file in glob.glob(os.path.realpath(inpath) + "/*.pdf")]
                elif file_or_dir == '.pdf' and os.path.isfile(os.path.realpath(inpath)):
                    l = [os.path.realpath(inpath)]
            else:
                file_or_dir = os.path.splitext(inpath)[1]


                if file_or_dir == '' and os.path.isdir(os.path.join(os.getcwd(), inpath)):
                        l = [file for file in glob.glob(os.path.join(os.getcwd(), inpath) + "/*.pdf")]
                elif file_or_dir == '.pdf' and os.path.isfile(os.path.join(os.getcwd(), inpath)):
                        l = [os.path.join(os.getcwd(), inpath)]
                elif file_or_dir == '' and os.path.isdir(os.path.realpath(inpath)):
                        l = [file for file in glob.glob(os.path.realpath(inpath) + "/*.pdf")]
                elif file_or_dir == '.pdf' and os.path.isfile(os.path.realpath(inpath)):
                        l = [os.path.join(os.path.realpath(inpath), inpath)]
                else:
                        if os.name == 'nt':
                            l=[]
                            for r, d, f in os.walk(os.path.realpath('\\')):
                               
                                if file_or_dir == '.pdf':
                                    
                                    for file in f:
                                        
                                        if len(inpath.split('\\')) == 1:
                                            if file == inpath:
                                                if os.path.isfile(os.path.join(r, file)):
                                                    l.append(os.path.join(r, file))
                                        else:
                                            if file == inpath.split('\\')[-1] and '\\'.join(inpath.split('\\')[:-1]) in r:
                                                if os.path.isfile(os.path.join(r, file)):
                                                    l.append(os.path.join(r, file))
                                elif file_or_dir == '':
                                    
                                    if inpath==r[-len(inpath):]:
                                        l+=[file for file in glob.glob(r + "/*.pdf")]

                        elif os.name == 'posix':
                            l=[]
                            for r, d, f in os.walk('/'):
                                    
                                    if file_or_dir == '.pdf':
                                        for file in f:
                                            if len(inpath.split('/')) == 1:
                                                if file == inpath:
                                                    if os.path.isfile(os.path.join(r, file)):
                                                        l.append(os.path.join(r, file))
                                            else:
                                                if file == inpath.split('/')[-1] and '/'.join(inpath.split('/')[:-1]) in r:
                                                    if os.path.isfile(os.path.join(r, file)):
                                                        l.append(os.path.join(r, file))
                                    elif file_or_dir == '':
                                        
                                        if inpath==r[-len(inpath):]:
                                            l+=[file for file in glob.glob(r + "/*.pdf")]
                                

            if l == []:
                if file_or_dir=='': 
                        raise FileNotFoundError("This is either a non-existent directory or no pdf file exists in this directory")
                elif file_or_dir=='.pdf':
                        raise FileNotFoundError("This is an non-existent pdf file")
                else:
                        raise ValueError("Only pdf files are acceptable as input")
            if os.name == 'nt':
                dirg=''
                if self.which_win('gswin64c.exe') is not None:

                    dirg = str(PurePath(self.which_win('gswin64c.exe')))



                elif self.which_win('gswin32c.exe') is not None:

                    dirg = str(PurePath(self.which_win('gswin64c.exe')))


                else:
                    for r, d, f in os.walk(os.path.realpath('\\')):

                        for files in f:

                            if files == 'gswin64c.exe' or files == 'gswin32c.exe':

                                if self.is_exe(os.path.join(r, files)):
                                    dirt = str(PurePath(os.path.join(r, files)))

                if dirg is None or dirg=='':
                    sys.exit("Please install Ghostscript, if you want to complete this task")
                    
                dirt=''
                if self.which_win('tesseract.exe') is not None:

                    dirt = str(PurePath(self.which_win('tesseract.exe')))

                else:

                    for r, d, f in os.walk(os.path.realpath('\\')):

                        for files in f:

                            if files == "tesseract.exe":

                                if self.is_exe(os.path.join(r, files)):
                                    dirt = str(PurePath(os.path.join(r, files)))

                if dirt is None or dirt=='':
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

                                                cwd=directory, startupinfo=si)

                        proc.wait()

                    except:

                        print("Error while running Ghostscript subprocess. Traceback:")

                        print("Traceback:\n%s" % traceback.format_exc())

                    stdout, stderr = proc.communicate()

                    if stderr:
                        print("Ghostscript stderr:\n'%s'" % stderr)

                    try:

                        read_pdf = outp.split('.')[0] + '_new'

                        command_line1 = 'tesseract ' + outp + ' ' + read_pdf + ' pdf'

                        args1 = shlex.split(command_line1)

                        proc1 = subprocess.Popen(args1, executable=dirt, stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT, cwd=directory, startupinfo=si)

                        proc1.wait()

                    except:

                        print("Error while running Tesseract subprocess. Traceback:")

                        print("Traceback:\n%s" % traceback.format_exc())

                    stdout1, stderr1 = proc1.communicate()

                    if stderr1:
                        print("Tesseract stderr:\n'%s'" % stderr1)

                    try:

                        os.remove(directory + '\\' + outp)

                    except OSError:

                        raise







            elif os.name == 'posix':
                
                check1=subprocess.Popen(['which','tesseract'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                check1.wait()
                c1stdout, c1stderr = check1.communicate()
                if c1stdout==b'':
                    raise FileNotFoundError("Please install Tesseract-OCR, if you want to complete this task")
                
                
                check2=subprocess.Popen(['which','gs'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                check2.wait()
                c2stdout, c2stderr = check2.communicate()
                if c2stdout==b'':
                    raise FileNotFoundError("Please install Ghostscript, if you want to complete this task")
                
                for inp in l:

                    

                  

                    directory = str(PurePath(inp).parent)

                    inp = PurePath(inp).name

                    try:

                        outp = inp.split('.')[0] + '.tiff'

                        command_line = 'gs -q -r300 -dNOPAUSE -sDEVICE=tiffgray -dBATCH -dINTERPOLATE -o ' + outp + ' -f ' + inp + ' -c quit'

                        args = shlex.split(command_line)

                        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory)

                        proc.wait()

                    except:

                        print("Error while running Ghostscript subprocess. Traceback:")

                        print("Traceback:\n%s" % traceback.format_exc())

                    stdout, stderr = proc.communicate()

                    if stderr:
                        print("Ghostscript stderr:\n'%s'" % stderr)

                    try:

                        read_pdf = outp.split('.')[0] + '_new'

                        command_line1 = 'tesseract ' + outp + ' ' + read_pdf + ' pdf'

                        args1 = shlex.split(command_line1)

                        proc1 = subprocess.Popen(args1, stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT, cwd=directory)

                        proc1.wait()

                    except:

                        print("Error while running Tesseract subprocess. Traceback:")

                        print("Traceback:\n%s" % traceback.format_exc())

                    stdout1, stderr1 = proc1.communicate()

                    if stderr1:
                        print("Tesseract stderr:\n'%s'" % stderr1)

                    try:

                        os.remove(directory + '/' + outp)

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


@click.command()
@click.argument('input_path')
def main(input_path):
    new_pdfs = pdf(input_path)
    new_pdfs.transform()


if __name__ == "__main__":
    main()

