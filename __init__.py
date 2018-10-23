"""
Debug provides methods for code debugging and rapid testing purposes

"""

import __future__

__all__ = ['Input', 'Output', 'App', 'Canvas', 'File', 'Debug', 'Threads']
__version__ = '0.1'
__author__ = 'Christopher Skorka'

# from devkit.In import *
# from devkit.Out import *
import devkit.Input
import devkit.Output
from devkit.App import *
from devkit.Canvas import *
from devkit.File import *
from devkit.Debug import *
from devkit.Threads import *