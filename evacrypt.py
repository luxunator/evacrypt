from crypter import crypter as evacrypter
import argparse
import colored

# Tool header
print(rf'''{colored.fg(93)}
___________                                          __
\_   _____/__  _______    ___________ ___.__._______/  |_
 |    __)_\  \/ /\__  \ _/ ___\_  __ <   |  |\____ \   __\
 |        \\   /  / __ \\  \___|  | \/\___  ||  |_> >  |
/_______  / \_/  (____  /\___  >__|   / ____||   __/|__|
        \/            \/     \/       \/     |__|
''')

# Set arguments to be used
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument('infile', help='file to obfuscate', type=str)
parser.add_argument("--b16", help="number of times to base64 "
                                  "encode source code", type=int)
parser.add_argument("--b32", help="number of times to base32 "
                                  "encode source code", type=int)
parser.add_argument("--b64", help="number of times to base16 "
                                  "encode source code", type=int)
parser.add_argument("--zlib", help="number of times to zlib "
                                   "compress source code", type=int)
parser.add_argument("--marshal", help="number of times to use marshal "
                                      "to obfuscate and load "
                                      "compiled source code", type=int)
parser.add_argument("--b16marshal", help="number of times to use base16 "
                                         "and marshal to obfuscate and "
                                         "load compiled source code", type=int)
parser.add_argument("--b32marshal", help="number of times to use base32 "
                                         "and marshal to obfuscate and "
                                         "load compiled source code", type=int)
parser.add_argument("--b64marshal", help="number of times to use base64 "
                                         "and marshal to obfuscate and "
                                         "load compiled source code", type=int)
parser.add_argument("--zmarshal", help="number of times to use zlib "
                                       "and marshal to obfuscate and "
                                       "load compiled source code", type=int)
group.add_argument("-z", "--zip", help="convert to executable zip as "
                                       "last obfuscation", action='store_true')
group.add_argument("-c", "--pyc", help="compile python source code "
                                       "to pyc as last obfuscation",
                                       action='store_true')
parser.add_argument("-o", "--outfile", help="output file location",
                                            default=None)
args = parser.parse_args()

# Checks for errors in arguments
if args.infile.endswith('.py'):
    script = evacrypter(args.infile, args.outfile)
else:
    parser.error('Input file must be a .py')

# Function execution for arguments supplied
if args.b16:
    script.b16(args.b16)

if args.b32:
    script.b32(args.b32)

if args.b64:
    script.b64(args.b64)

if args.zlib:
    script.zlib(args.zlib)

if args.b16marshal:
    script.b16_marshal(args.b16marshal)

if args.b32marshal:
    script.b32_marshal(args.b32marshal)

if args.b64marshal:
    script.b64_marshal(args.b64marshal)

if args.zmarshal:
    script.zlib_marshal(args.zmarshal)

if args.marshal:
    script.marshal(args.marshal)

# Output type functions
if args.zip:
    script.tozip()

if args.pyc:
    script.pyc()

# Save to output file
script.save()
