import notify2
import sys
import os

directory = '.'
if len(sys.argv) > 1:
    directory = sys.argv[1]

os.system('git add ' + directory)
os.system('git commit -m "Changes in ' + directory + ' pushed by gcommit"')
os.system('git push')

notify2.init('app name')
n = notify2.Notification('GCommit', 'Changes in ' + directory + ' have been pushed')
n.show()