# Python Regular Expressions and argparse
# check password complexity, length, character requirements

# started 18DEC16
# Python 3.5

# >python -i pwd_chk.py --password SECRET -v
# >python -i pwd_chk.py -p secretSECRET123!@# -l 10 -a 3 -A 3 -n 3 -s 3 -v
# >python dir


import argparse
import re


def main():
    parser = build_parser()
    args = parse_args(parser)
    failed = check_password_old(args)

    # check if any test failed
    if not failed:
        print('PASSED - All tests passed.')


def check_password_new(args):
    passed = True

    # TODO test new code
    categories = (args.length, args.lower, args.upper, args.special, args.number)

    categories = ({'name': 'length', 'regex': r'.*', 'value': 0},)

    for category in categories:
        if category['value'] > 0:
            if args.verbose:
                print('Testing ' + category['name'] + ': ' + str(category['name']))

            str_regex = category['regex']
            compiled_regex = re.compile(str_regex)

            if args.verbose:
                print('\tRegex for ' + category['name'] + ': ' + str_regex)

            regex_result = compiled_regex.search(args.password)

            if regex_result is None:
                print('FAILED - Password failed ' + category['name'] + ' requirement.')
                passed = False
            else:
                if args.verbose:
                    print('\t' + category['name'] + '  regex: ' + regex_result.group())
                    print('\tPassed length')
    return passed


def check_password_old(args):
    passed = True  # Set false if password fails a test.

    # length regex
    if args.length > 0:
        if args.verbose:
            print('Testing length: ' + str(args.length))

        strLengthRegex = r'.{' + str(args.length) + ',}'
        lengthRegex = re.compile(strLengthRegex)

        if args.verbose:
            print('\tRegex for length: ' + strLengthRegex)

        lengthResult = lengthRegex.search(args.password)

        if lengthResult is None:
            print('FAILED - Password failed length requirement.')
            passed = False
        else:
            if args.verbose:
                print('\tLength result: ' + lengthResult.group())
                print('\tPassed length')
    # lower case regex
    if args.lower > 0:
        if args.verbose:
            print('Testing lower-case: ' + str(args.lower))

        strRegexLower = ''

        for count in range(args.lower):
            strRegexLower += '[a-z].*'

        strRegexLower = strRegexLower[:-2]
        if args.verbose:
            print('\tRegex for lower: ' + strRegexLower)

        lowerRegex = re.compile(strRegexLower)
        lowerResult = lowerRegex.search(args.password)

        if lowerResult is None:
            print('FAILED - Password failed lower-case letter requirement.')
            passed = False
        else:
            if args.verbose:
                print('\tLower-case results: ' + lowerResult.group())
                print('\tPassed lower-case')
    # upper case regex
    if args.upper > 0:
        if args.verbose:
            print('Testing upper-case: ' + str(args.upper))

        # build upper regex
        strRegexUpper = ''

        for count in range(args.upper):
            strRegexUpper += '[A-Z].*'

        strRegexUpper = strRegexUpper[:-2]
        if args.verbose:
            print('\tRegex for upper: ' + strRegexUpper)

        upperRegex = re.compile(strRegexUpper)
        upperResult = upperRegex.search(args.password)

        if upperResult is None:
            print('FAILED - Password failed upper-case letter requirement.')
            passed = False
        else:
            if args.verbose:
                print('\tUpper-case results: ' + upperResult.group())
                print('\tPassed upper-case')
    # special character regex
    if args.special > 0:
        if args.verbose:
            print('Testing special: ' + str(args.special))
            print('\tspecial set: ' + args.set)

        # build special character regex
        strRegexSpecial = ''

        for count in range(args.special):
            strRegexSpecial += '[' + args.set + '].*'

        strRegexSpecial = strRegexSpecial[:-2]
        if args.verbose:
            print('\tRegex for special: ' + strRegexSpecial)

        specialCharRegex = re.compile(strRegexSpecial)
        specialCharResult = specialCharRegex.search(args.password)

        if specialCharResult is None:
            print('FAILED - Password failed special character requirement.')
            passed = False
        else:
            if args.verbose:
                print('\tSpecial character results: ' + specialCharResult.group())
                print('\tPassed special character')
    # number regex
    if args.number > 0:
        if args.verbose:
            print('Testing number: ' + str(args.number))

        # build number regex
        strRegexNumber = ''

        for count in range(args.number):
            strRegexNumber += '\d.*'

        strRegexNumber = strRegexNumber[:-2]

        if args.verbose:
            print('\tRegex for number: ' + strRegexNumber)

        numberRegex = re.compile(strRegexNumber)
        numberResult = numberRegex.search(args.password)

        if numberResult is None:
            print('FAILED - Password failed number requirement.')
            passed = False
        else:
            if args.verbose:
                print('\tNumber results: ' + numberResult.group())
                print('\tPassed number')
    return passed


def parse_args(parser):
    # execute command parser
    args = parser.parse_args()
    if args.password:
        if args.verbose:
            print('Verbose mode.')
            print('Password is: ' + args.password)
            print('Settings are:')
            print('\tlength: ' + str(args.length))
            print('\tlower-case: ' + str(args.lower))
            print('\tupper-case: ' + str(args.upper))
            print('\tspecial: ' + str(args.special))
            print('\tspecial set: ' + args.set)
            print('\tnumber: ' + str(args.number))
            print('')
    else:
        parser.print_help()
        exit()
    return args


def build_parser():
    parser = argparse.ArgumentParser(description='Check if a password meets complexity requirements')
    parser.add_argument('--password', '-p', help='password to check', required=True)
    parser.add_argument('--length', '-l', help='minimum length of password, default is 0', default=0, type=int)
    parser.add_argument('--lower', '-a', help='number of lower-case alphabet letters required, default is 0', default=0,
                        type=int)
    parser.add_argument('--upper', '-A', help='number of upper-case alphabet letters required, default is 0', default=0,
                        type=int)
    parser.add_argument('--special', '-s', help='number of special characters required, default is 0', default=0,
                        type=int)
    parser.add_argument('--set', help='set of special characters allowed, default is \'!@#$%^&*.\'',
                        default='!@#$%^&*.',
                        type=str)
    parser.add_argument('--number', '-n', help='number of numeric characters required, default is 0', default=0,
                        type=int)
    parser.add_argument('--verbose', '-v', help='enable verbose mode', action='store_true')
    return parser


def test_build_parser():
    parser = build_parser()

    # test 1
    args = parser.parse_args(['-v', '--password', 'SECRET'])
    assert args.password == 'SECRET'
    assert args.verbose

    # test 2
    # -p secretSECRET123!@# -l 10 -a 3 -A 3 -n 3 -s 3 -v
    args = parser.parse_args(['-v', '-p', 'secretSECRET123!@#', '-l', '10', '-a', '3', '-A', '3', '-n', '3', '-s', '3'])
    assert args.password == 'secretSECRET123!@#'
    assert args.verbose
    assert args.length == 10


def test_check_password_old():
    def test(args, result):
        parsed_args = parser.parse_args(args)
        assert check_password_old(parsed_args) == result

    parser = build_parser()

    test(['-v', '--password', 'SECRET'], True)
    test(['-v', '--password', 'SECRET', '-l', '4'], True)
    test(['-v', '--password', 'SECRET', '-l', '10'], False)
    test(['-v', '--password', 'secret', '-a', '4'], True)
    test(['-v', '--password', 'secret', '-a', '10'], False)
    test(['-v', '--password', '0s1e2c3r4e5t6', '-a', '10'], False)
    test(['-v', '--password', 'SECRET', '-A', '4'], True)
    test(['-v', '--password', 'SECRET', '-A', '10'], False)
    test(['-v', '--password', '12345', '-n', '4'], True)
    test(['-v', '--password', '12345', '-n', '10'], False)
    test(['-v', '--password', '0s1e2c3r4e5t6', '-n', '4'], True)
    test(['-v', '--password', '0s1e2c3r4e5t6', '-n', '10'], False)
    test(['-v', '--password', '0S1E2CRETsecr!e@t#', '-s', '3'], True)
    test(['-v', '--password', '0S1E2CRETsecr!e@t#', '-s', '10'], False)
    test(['-v', '--password', '0S1E2CRETsecr!e@t#', '-l', '10', '-a', '3', '-A', '3', '-n', '3', '-s', '3'], True)


def test_check_password_new():
    def test(args, result):
        parsed_args = parser.parse_args(args)
        assert check_password_new(parsed_args) == result

    parser = build_parser()

    test(['-v', '--password', 'SECRET'], True)
    test(['-v', '--password', 'SECRET', '-l', '4'], True)
    test(['-v', '--password', 'SECRET', '-l', '10'], False)
    test(['-v', '--password', 'secret', '-a', '4'], True)
    test(['-v', '--password', 'secret', '-a', '10'], False)
    test(['-v', '--password', '0s1e2c3r4e5t6', '-a', '10'], False)
    test(['-v', '--password', 'SECRET', '-A', '4'], True)
    test(['-v', '--password', 'SECRET', '-A', '10'], False)
    test(['-v', '--password', '12345', '-n', '4'], True)
    test(['-v', '--password', '12345', '-n', '10'], False)
    test(['-v', '--password', '0s1e2c3r4e5t6', '-n', '4'], True)
    test(['-v', '--password', '0s1e2c3r4e5t6', '-n', '10'], False)
    test(['-v', '--password', '0S1E2CRETsecr!e@t#', '-s', '3'], True)
    test(['-v', '--password', '0S1E2CRETsecr!e@t#', '-s', '10'], False)
    test(['-v', '--password', '0S1E2CRETsecr!e@t#', '-l', '10', '-a', '3', '-A', '3', '-n', '3', '-s', '3'], True)


if __name__ == '__main__':
    main()
