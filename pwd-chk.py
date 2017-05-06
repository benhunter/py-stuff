# Python Regular Expressions
# check password complexity, length, character requirements

# started 18DEC16
# Python 3.5

# >python -i pwd-chk.py --password SECRET -v 
# >python -i .\pwd-chk.py -p secretSECRET123!@# -l 10 -a 3 -A 3 -n 3 -s 3


import re
import argparse


failed = False  # Set true if password fails a test.

parser = argparse.ArgumentParser(description='Check if a password meets complexity requirements')
parser.add_argument('--password', '-p', help="password to check", required=True)
parser.add_argument('--length', '-l', help="minimum length of password, default is 0", default=0, type=int)
parser.add_argument('--lower', '-a', help="number of lower-case alphabet letters required, default is 0", default=0,
                    type=int)
parser.add_argument('--upper', '-A', help="number of upper-case alphabet letters required, default is 0", default=0,
                    type=int)
parser.add_argument('--special', '-s', help="number of special characters required, default is 0", default=0, type=int)
parser.add_argument('--set', help="set of special characters allowed, default is \"!@#$%^&*.\"", default="!@#$%^&*.",
                    type=str)
parser.add_argument('--number', '-n', help="number of numeric characters required, default is 0", default=0, type=int)

parser.add_argument('--verbose', '-v', help="enable verbose mode", action='store_true')

# execute command parser
args = parser.parse_args()

if args.password:
    if args.verbose:
        print("Verbose mode.")
        print("Password is: " + args.password)
        print("Settings are:")
        print("\tlength: " + str(args.length))
        print("\tlower-case: " + str(args.lower))
        print("\tupper-case: " + str(args.upper))
        print("\tspecial: " + str(args.special))
        print("\tspecial set: " + args.set)
        print("\tnumber: " + str(args.number))
        print("")
else:
    parser.print_help()
    exit()

# length regex
if args.length > 0:
    if args.verbose:
        print("Testing length: " + str(args.length))

    strLengthRegex = r'.{' + str(args.length) + ',}'
    lengthRegex = re.compile(strLengthRegex)

    if args.verbose:
        print("\tRegex for number: " + strLengthRegex)

    lengthResult = lengthRegex.search(args.password)

    if lengthResult == None:
        print('FAILED - Password failed length requirement.')
        failed = True
    else:
        if args.verbose:
            print("\tLength result: " + lengthResult.group())
            print("\tPassed length")

# lower case regex
if args.lower > 0:
    if args.verbose:
        print("Testing lower-case: " + str(args.lower))

    strRegexLower = ''

    for count in range(args.lower):
        strRegexLower += '[a-z].*'

    strRegexLower = strRegexLower[:-2]
    if args.verbose:
        print("\tRegex for lower: " + strRegexLower)

    lowerRegex = re.compile(strRegexLower)
    lowerResult = lowerRegex.search(args.password)

    if lowerResult == None:
        print('FAILED - Password failed lower-case letter requirement.')
        failed = True
    else:
        if args.verbose:
            print("\tLower-case results: " + lowerResult.group())
            print("\tPassed lower-case")

# upper case regex
if args.upper > 0:
    if args.verbose:
        print("Testing upper-case: " + str(args.upper))

    # build upper regex
    strRegexUpper = ''

    for count in range(args.upper):
        strRegexUpper += '[A-Z].*'

    strRegexUpper = strRegexUpper[:-2]
    if args.verbose:
        print("\tRegex for upper: " + strRegexUpper)

    upperRegex = re.compile(strRegexUpper)
    upperResult = upperRegex.search(args.password)

    if upperResult == None:
        print('FAILED - Password failed upper-case letter requirement.')
        failed = True
    else:
        if args.verbose:
            print("\tUpper-case results: " + upperResult.group())
            print("\tPassed upper-case")

# special character regex
if args.special > 0:
    if args.verbose:
        print("Testing special: " + str(args.special))
        print('\tspecial set: ' + args.set)

    # build special character regex
    strRegexSpecial = ''

    for count in range(args.special):
        strRegexSpecial += '[' + args.set + '].*'

    strRegexSpecial = strRegexSpecial[:-2]
    if args.verbose:
        print("\tRegex for special: " + strRegexSpecial)

    specialCharRegex = re.compile(strRegexSpecial)
    specialCharResult = specialCharRegex.search(args.password)

    if specialCharResult == None:
        print('FAILED - Password failed special character requirement.')
        failed = True
    else:
        if args.verbose:
            print("\tSpecial character results: " + specialCharResult.group())
            print("\tPassed special character")

# number regex
if args.number > 0:
    if args.verbose:
        print("Testing number: " + str(args.number))

    # build number regex
    strRegexNumber = ''

    for count in range(args.number):
        strRegexNumber += '\d.*'

    strRegexNumber = strRegexNumber[:-2]

    if args.verbose:
        print("\tRegex for number: " + strRegexNumber)

    numberRegex = re.compile(strRegexNumber)
    numberResult = numberRegex.search(args.password)

    if numberResult == None:
        print('FAILED - Password failed number requirement.')
        failed = True
    else:
        if args.verbose:
            print("\tNumber results: " + numberResult.group())
            print("\tPassed number")

# check if any test failed	
if not failed:
    print('PASSED - All tests passed.')

exit()
