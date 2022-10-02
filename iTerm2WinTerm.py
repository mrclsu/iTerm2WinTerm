#!/usr/bin/env python3

import plistlib
import json
import re
from sys import argv

itermColorsRegex = re.compile('(.+).itermcolors')
jsonRegex = re.compile('(.+).json')
arvgl = len(argv)

def itermKeyToWinKey(iterm_key):
    itermToWinDict = {
        'Ansi 0 Color'    : 'black',
        'Ansi 1 Color'    : 'red',
        'Ansi 2 Color'    : 'green',
        'Ansi 3 Color'    : 'yellow',
        'Ansi 4 Color'    : 'blue',
        'Ansi 5 Color'    : 'purple',
        'Ansi 6 Color'    : 'cyan',
        'Ansi 7 Color'    : 'white',
        'Ansi 8 Color'    : 'brightBlack',
        'Ansi 9 Color'    : 'brightRed',
        'Ansi 10 Color'   : 'brightGreen',
        'Ansi 11 Color'   : 'brightYellow',
        'Ansi 12 Color'   : 'brightBlue',
        'Ansi 13 Color'   : 'brightPurple',
        'Ansi 14 Color'   : 'brightCyan',
        'Ansi 15 Color'   : 'brightWhite',
        'Background Color': 'background',
        'Foreground Color': 'foreground',
    }
    try:
        return itermToWinDict[iterm_key]
    except:
        return 'undefined'

def rgbToHex(r, g, b):
    return ('#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))).upper()

def printUsage():
    print("usage: iTerm2WinTerm.py <iTerm color scheme> [--out <output JSON location>]")
    exit(0)

def checkArgs():
    if arvgl != 2 and arvgl != 4:
        printUsage()
    if itermColorsRegex.fullmatch(argv[1]) == None:
        printUsage()
    if arvgl == 4 and argv[2] != '--out':
        printUsage()

def main():
    checkArgs()

    print(argv)

    itermFileName = argv[1]
    schemeName = itermColorsRegex.fullmatch(itermFileName).group(1)

    itermFile = ''
    itermScheme = ''
    try:
        itermFile = open(itermFileName, "rb")
        itermScheme = plistlib.load(itermFile, fmt = plistlib.FMT_XML)
    except IOError:
        print("Cannot find specified iTerm colors file")
        printUsage()
    except:
        print("Error parsing {}".format(itermFileName))
        printUsage()
    outputDict = {'name': schemeName}

    for key in itermScheme:
        winKey = itermKeyToWinKey(key)
        colorDict = itermScheme[key]
        if winKey != 'undefined':
            outputDict[winKey] = rgbToHex(colorDict['Red Component'], colorDict['Green Component'], colorDict['Blue Component'])
    
    prettyJson = json.dumps(outputDict, indent=4)
    if arvgl == 4:
        outFileName = argv[3]
        if jsonRegex.fullmatch(outFileName) == None: outFileName += '.json'
        try:
            jsonFile = open(outFileName, 'w')
            jsonFile.write(prettyJson)
            jsonFile.close()
        except:
            print("Error while writing to {}".format(outFileName))
    else:
        print(prettyJson)


if __name__ == '__main__':
    main()
