""" main """
import os
import subprocess
import sys

def verify():
    try:
        import config as c
    except:
        if not os.path.isfile('config.py'):
            confile = open('config.py', 'w+')

            confile.write('filename = \'main\'\n')
            confile.write('filepath = \'./lists/\'')

            confile.close()
            print('created config from template')
    finally:
        import config as c
        if not os.path.exists(c.filepath):
            try:
                print("Creating file directory")
                os.makedirs(c.filepath)
            except:
                print("Could not create directory. Check config formatting.\nExiting...")
                raise SystemExit
        if not os.path.isfile(c.filepath+c.filename):
            try:
                print("Creating file")
                file = open(c.filepath+c.filename, 'w+')
                file.close()
            except:
                print("Could not create file. Check config formatting.\nExiting...")
                raise SystemExit
verify()
import config as c

def helpme():
    print('\n\tUsage: python3 punct.py [arguments]\n')
    print('\t                   No argument, shows list contents.')
    print('\t       -l          Same as no argument, Lists out list content.')
    print('\t       -h          Shows this dialog.')
    print('\t       -c          Check/uncheck list.')
    print('\t       -s List     Sets which todo list to use.')
    print('\t       -f Path     Sets list dir (folder)')
    print('\t       -a Content  Adds an entry to your todo list.')
    print('\t       -r Index    Removes an entry from your todo list.')
    print('\t       -p          Purge completed tasks.')
    print('')

def add():
    try:
        file = open(c.filepath+c.filename, 'a+')
        file.write('\n-[]'+sys.argv[2])
        file.close()
    except:
        print("Could not add entry to list.\nExiting...\n")
        raise SystemExit

def display():
    try:
        f = open(c.filepath+c.filename, 'r')
        l = [l for l in f.readlines() if l.strip()]
        f.close()
        f = open(c.filepath+c.filename, 'w+')
        f.writelines( l )
        f.close()
    except:
        print("Could not remove whitespace from list contents.\nExiting...\n")
        raise SystemExit
    finally:
        print('')
        file = open(c.filepath+c.filename, 'r')
        i = 0
        for line in file:
            i += 1
            print(str("{}   ".format(i)+line.strip("\n")))
        file.close()
        print('')

def check():
    with open(c.filepath+c.filename, 'r') as file:
        data = file.readlines()
        if data[int(sys.argv[2])-1][:3] == "-[]":
            data[int(sys.argv[2])-1] = data[int(sys.argv[2])-1].replace("-[]", "-[x]")
        else:
            data[int(sys.argv[2])-1] = data[int(sys.argv[2])-1].replace("-[x]", "-[]")
        with open(c.filepath+c.filename, 'w') as file:
            file.writelines( data )


def remove():
    with open(c.filepath+c.filename, 'r') as file:
        data = file.readlines()
        data[int(sys.argv[2])-1] = ""
        with open(c.filepath+c.filename, 'w') as file:
            file.writelines( data )

def setList():
    file = open('config.py', 'r')
    i = 0
    for line in file:
        i += 1
        if "filename" in line:
            with open('config.py', 'r') as file:
                data = file.readlines()
                data[i-1] = "\nfilename='{}'\n".format(sys.argv[2])
                with open('config.py', 'w') as file:
                        file.writelines( data )
                file.close()

                f = open('config.py', 'r')
                l = [l for l in f.readlines() if l.strip()]
                f.close()
                f = open('config.py', 'w+')
                f.writelines( l )
                f.close()

def setFolder():
    file = open('config.py', 'r')
    i = 0
    for line in file:
        i += 1
        if "filepath" in line:
            with open('config.py', 'r') as file:
                data = file.readlines()
                data[i-1] = "\nfilepath='{}'\n".format(sys.argv[2])
                with open('config.py', 'w') as file:
                        file.writelines( data )
                file.close()

                f = open('config.py', 'r')
                l = [l for l in f.readlines() if l.strip()]
                f.close()
                f = open('config.py', 'w+')
                f.writelines( l )
                f.close()

def purge():
    bad_words = ['-[x]']

    with open(c.filepath+c.filename) as oldfile, open(c.filepath+c.filename+".tmp", 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words):
                newfile.write(line)
    with open(c.filepath+c.filename+".tmp") as f:
        with open(c.filepath+c.filename, "w") as f1:
            for line in f:
                f1.write(line)
    f.close()
    f1.close()
    os.remove(c.filepath+c.filename+".tmp")

if len(sys.argv) > 3:
    print('Too many arguments!')
    raise SystemExit

if len(sys.argv) <= 1 or '-l' in sys.argv:
    display()
    raise SystemExit # prevent display from being ran twice, see bottom of file
elif '-h' in sys.argv:
    helpme()
    raise SystemExit # prevent display from being ran twice, see bottom of file
elif '-a' in sys.argv:
    add()
elif '-r' in sys.argv:
    remove()
elif '-s' in sys.argv:
    setList()
    raise SystemExit
elif '-f' in sys.argv:
    setFolder()
    raise SystemExit
elif '-c' in sys.argv:
    check()
    #raise SystemExit # prevent display from being ran twice, see bottom of file
elif '-p' in sys.argv:
    purge()
else:
    print('Unknown operation: {}'.format(sys.argv))

display()
raise SystemExit