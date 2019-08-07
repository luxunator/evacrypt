from zipfile import ZipFile
import py_compile
import marshal
import base64
import zlib
import math
import os


class crypter():

    def _get_size(self, file):  # Gets size of file in easy to read form
        size = os.path.getsize(file)
        if size == 0:
            print(f"{self.infile} is Empty! 0B")
            exit()
        size_label = ("B", "KB", "MB", "GB")
        i = int(math.floor(math.log(size, 1024)))
        p = math.pow(1024, i)
        size = round(size / p, 2)
        return size, size_label[i]

    def __init__(self, infile, outfile):
        self.infile = infile
        size, label = self._get_size(self.infile)  # Return size of input file
        print(f"Size of Input File '{self.infile}' = {size} {label}")
        self.outfile = outfile
        if not self.outfile:  # If no output file then default location is set
            self.outfile = f'eva_{infile.split("/")[-1]}'
            self.outdir = './crypted/'
        else:                 # Use output location if set
            self.outdir = (f'{"/".join(self.outfile.split("/")[:-1])}/'
                           if '/' in self.outfile else
                           f'./{"/".join(self.outfile.split("/")[:-1])}')
            self.outfile = self.outfile.split("/")[-1]
        try:
            with open(self.infile) as f:
                self.contents = f.read()
        except UnicodeDecodeError as e:  # Handling unreadable input file
            print(f"Error in Reading {self.infile}: {e}\n"
                  "Make sure file is plaintext!")
            exit()

    def b16(self, depth):                      # Base 16 encode python source
        with open(self.infile, 'r') as source:
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                b16contents = base64.b16encode(source).decode('utf-8')
                source = 'import base64\n' \
                         f'exec(base64.b16decode("{b16contents}"))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def b32(self, depth):                      # Base 32 encode python source
        with open(self.infile, 'r') as source:
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                b32contents = base64.b32encode(source).decode('utf-8')
                source = 'import base64\n' \
                         f'exec(base64.b32decode("{b32contents}"))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def b64(self, depth):                      # Base 64 encode python source
        with open(self.infile, 'r') as source:
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                b64contents = base64.b64encode(source).decode('utf-8')
                source = 'import base64\n' \
                         f'exec(base64.b64decode("{b64contents}"))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def zlib(self, depth):                     # Compress source with zlib
        with open(self.infile, 'r') as source:
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                contents = zlib.compress(source)
                source = 'import zlib\n' \
                         f'exec(zlib.decompress({contents}))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def marshal(self, depth):                  # Compile source then
        with open(self.infile, 'r') as source:  # load with marshal
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                contents = marshal.dumps(compile(source, '<script>', 'exec'))
                source = f'import marshal\nexec(marshal.loads({contents}))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def b16_marshal(self, depth):              # Compile source, base16 encode,
        with open(self.infile, 'r') as source:  # and then load with marshal
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                contents = marshal.dumps(compile(source, '<script>', 'exec'))
                b16contents = base64.b16encode(contents).decode('utf-8')
                source = 'import marshal\n' \
                         'import base64\nexec(marshal.loads(' \
                         f'base64.b16decode("{b16contents}")))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def b32_marshal(self, depth):              # Compile source, base32 encode,
        with open(self.infile, 'r') as source:  # and then load with marshal
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                contents = marshal.dumps(compile(source, '<script>', 'exec'))
                b32contents = base64.b32encode(contents).decode('utf-8')
                source = 'import marshal\n' \
                         'import base64\nexec(marshal.loads(' \
                         f'base64.b32decode("{b32contents}")))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def b64_marshal(self, depth):              # Compile source, base64 encode,
        with open(self.infile, 'r') as source:  # and then load with marshal
            source = source.read()
            for layer in range(depth):
                source = source.encode('utf-8')
                contents = marshal.dumps(compile(source, '<script>', 'exec'))
                b64contents = base64.b64encode(contents).decode('utf-8')
                source = 'import marshal\n' \
                         'import base64\nexec(marshal.loads(' \
                         f'base64.b64decode("{b64contents}")))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def zlib_marshal(self, depth):             # Compile source, compress
        with open(self.infile, 'r') as source:  # with zlib, and then load
            source = source.read()               # load with marshal
            for layer in range(depth):
                source = source.encode('utf-8')
                contents = marshal.dumps(compile(source, '<script>', 'exec'))
                zcontent = zlib.compress(contents)
                source = 'import marshal\n' \
                         'import zlib\nexec(marshal.loads(' \
                         f'zlib.decompress({zcontent})))'

            with open(self.infile, 'w') as out:
                out.write(source)

    def tozip(self):                                # Convert python file to
        with ZipFile(self.infile, 'w') as zip_file:  # executable zip file
            with open('__main__.py', 'w') as main:
                with open(self.infile, 'r') as in_file:
                    main.write(in_file.read())

            zip_file.write('__main__.py')
        os.remove('__main__.py')

    def pyc(self):  # Compile python file
        py_compile.compile(self.infile, cfile=self.infile)

    def save(self):  # Save file to output location
        if f'{self.outdir}{self.infile}' != f'{self.outdir}{self.outfile}':
            os.rename(self.infile, f'{self.outdir}{self.outfile}')
            with open(self.infile, 'w') as f:
                f.write(self.contents)
        else:
            os.rename(self.infile, f'{self.outdir}{self.outfile}')
        size, label = self._get_size(f'{self.outdir}{self.outfile}')

        print("Done! Size of Output File "  # Return size of output file
              f"'{self.outdir}{self.outfile}' = {size} {label}")
