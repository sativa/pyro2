from __future__ import print_function
import sys

# inspiration from                                                                          
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python      
# which in-turn cites the blender build scripts                                             
class _TermColors:
    WARNING = '\033[33m'
    SUCCESS = '\033[32m'
    FAIL = '\033[31m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def fail(str):
    """
    Output a string to the terminal and abort if we are running
    non-interactively.  The string is colored red to indicate a 
    failure
    """
    print(_TermColors.FAIL + str + _TermColors.ENDC)

    # only exit if we are not running in interactive mode.  sys.ps1 is
    # only defined in interactive mode.
    if hasattr(sys, 'ps1'):
        return
    else:
        sys.exit()

def warning(str):
    """
    Output a string to the terminal colored orange to indicate a 
    warning
    """
    print(_TermColors.WARNING + str + _TermColors.ENDC)

def success(str):
    """
    Output a string to the terminal colored green to indicate 
    success
    """
    print(_TermColors.SUCCESS + str + _TermColors.ENDC)

def bold(str):
    """ Output a string in a bold weight"""
    print(_TermColors.BOLD + str + _TermColors.ENDC)



