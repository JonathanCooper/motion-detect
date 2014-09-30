from optparse import OptionParser
import sys
import os

# TODO: logging
parser = OptionParser()
parser.add_option('-e', '--enable', action='store_true', dest='enable', help='enable the alarm system', default=False)
parser.add_option('-d', '--disable', action='store_true', dest='disable', help='disable the alarm system', default=False)

(options, args) = parser.parse_args()

if not options.enable and not options.disable:
    print 'Error: Must use one of (-e|-d)'
    sys.exit(1)

lock_file = '/www/motiondetect/run/lock'

if options.enable:
    if not os.path.isfile(lock_file):
        print 'Error: System is already enabled'
        sys.exit(2)
    else:
        os.remove(lock_file)
        print 'System enabled'
        sys.exit(0)
elif options.disable:
    if os.path.isfile(lock_file):
        print 'Error: System is already disabled'
        sys.exit(3)
    else:
        open(lock_file, 'w').close()
        os.chown(lock_file, 81, 81)
        print 'System disabled'
        sys.exit(0)

print 'Error: We are not supposed to get here'
sys.exit(4)
