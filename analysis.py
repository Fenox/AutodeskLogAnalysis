import glob, os
import sys, getopt

def main(argv):
    #parse command line (folder to search logs)
    inputfolder = ''
    try:
        opts, args = getopt.getopt(argv[1:], 'hl:',["help", "logs="])
    except getopt.GetoptError:
        print 'befehlFilter.py -logs <logs folder>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'befehlFilter.py -logs <logs folder>'
            sys.exit()
        elif opt in ("-l", "--logs"):
            inputfolder = arg

    os.chdir(inputfolder)

    #Read all files in given Folder and concatenate them
    log = list()
    for filename in os.listdir("."):
        f = open(filename, "r")
        log.extend(f.read().splitlines())


    from collections import Counter
    # Read each line starting with: "Befehl" and remove "Befehl: " from the line.
    commands = map(lambda y : y[8:], filter(lambda x : "Befehl: " in x, log))

    # Filter each file that no content.
    nullLengthFiltered = filter(lambda x : len(x.split()) > 0, commands)

    # Get commands starting with _ or *
    filteredByCmd = filter(lambda cmd: (cmd[0] == '_') or (cmd[0] == '*'), nullLengthFiltered)
    
    # Remove trailing text
    onlyCmdName = map(lambda cmd: cmd.split(' ')[0], filteredByCmd)

    # Create list (cmd, count)
    result0 = Counter(onlyCmdName).items()

    # swap (cmd, count) to (count, cmd) to be able to sort by count
    result = (map(lambda t: (t[1], t[0]), result0))

    # sum over the number of used commands
    cmdSum = sum(zip(*result)[0])

    print '%      Occurrences  Name'
    for num, name in sorted(result,reverse=True):
        print '{:.2%}'.format(num / float(cmdSum)), num, name 

if __name__ == "__main__":
    main(sys.argv)