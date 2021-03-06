__author__ = 'ad'

import sys
import os
import os.path

import nose


if __name__ == '__main__':
    project_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(project_dir)
    sys.exit(nose.main(argv=['nose', '-v', '-i={}'.format(project_dir)] + sys.argv[1:]))