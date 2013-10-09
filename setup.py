'''
Created on 30 09 2013 

@author: prolubnikovda
'''
from distutils.core import setup
import py2exe

setup(
    windows=[{"script":"main.py"}], 
    options={"py2exe": {"includes":["sip"]}}
)