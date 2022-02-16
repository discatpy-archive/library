import argparse
import sys

import disbotpy
import platform

def neofetch():
    print(
    """
d8888b       **                d88888b.                       d888888b.  
88    `8D    **      .d8888.   88     8D                      88    `8D  
88     88            88'   YP  88     8D    .d88b.      00    88     8D  88     88
88     88    88      `8bo.     88oooooY'   88     88  888888  88oodD'    '88  88'
88     88    88        Y8b.    88     b.   88     88   '88'   88           '88'
88    .8D   .88.   db    8D    88     8D   88     88    88    88           88
Y88888D    888888   `8888Y'    Y8888P'      'Y88P'      'YP   88         YP

----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
    """
    )

    entries = []
    entries.append("Python Version: {0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(sys.version_info))
    entries.append("DisBotPy Version: {}".format(disbotpy.__version__))
    entries.append("System Information: {0.system} {0.release} {0.version}".format(platform.uname()))
    print('\n'.join(entries))

def main():
    neofetch()

if __name__ == '__main__':
    main()