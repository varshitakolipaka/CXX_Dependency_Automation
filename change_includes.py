import os
import shutil
from pathlib import Path
import re
import pydot

c_headers = ["<exception>", "<limits>", "<new>", "<new.h>", "<typeinfo>", "<stdexcept>", "<utility>", "<functional>", "<memory>", "<string>", "<locale>", "<algorithm>", "<bitset>", "<deque>", "<iterator>", "<list>", "<map>", "<queue>", "<set>", "<stack>", "<unordered_map>", "<unordered, set>", "<vector>", "<complex>", "<numeric>", "<valarray>", "<fstream>", "<iomanip>", "<ios>", "<iosfwd>", "<iostream>", "<istream>", "<ostream>", "<streambuf>", "<sstream>", "<strstream>", "<cassert>", "<assert.h>", "<cctype>", "<ctype.h>", "<cerrno>", "<errno.h>", "<cfloat>", "<float.h>", "<ciso646>", "<iso646.h>", "<climits>", "<limits.h>", "<clocale>", "<locale.h>", "<cmath>", "<math.h>", "<csetjmp>", "<setjmp.h>", "<csignal>", "<signal.h>", "<cstdarg>", "<stdarg.h>", "<cstddef>", "<stddef.h>", "<cstdio>", "<stdio.h>", "<cstdlib>", "<stdlib.h>", "<cstring>", "<string.h>", "<ctime>", "<time.h>", "<cwchar>", "<wchar.h>", "<cwctype>", "<wctype.h>", "<array>", "<random>", "<regex>", "<type_traits>", "<tuple>", "<unordered_map>", "<unordered_set>", "<algorithm>", "<array>", "<bitset>", "<cassert>", "<cctype>", "<cerrno>", "<cfloat>", "<ciso646>", "<climits>", "<clocale>", "<cmath>", "<complex>", "<csetjmp>", "<csignal>", "<cstdarg>", "<cstddef>", "<cstdio>", "<cstdlib>", "<cstring>", "<ctime>", "<cwchar>", "<cwctype>", "<deque>", "<exception>", "<fstream>", "<functional>", "<iomanip>", "<ios>", "<iosfwd>", "<iostream>", "<istream>", "<iterator>", "<limits>", "<list>", "<locale>", "<map>", "<memory>", "<new>", "<numeric>", "<ostream>", "<queue>", "<random>", "<regex>", "<set>", "<sstream>", "<stack>", "<stdexcept>", "<streambuf>", "<string>", "<strstream>", "<tuple>", "<typeinfo>", "<type_traits>", "<unordered_map>", "<unordered_set>", "<utility>", "<valarray>", "<vector>"]

def changed_line(myline, file_path):
    ''' finds all instances of include patterns in a line.
    checks in [()], and checks whether such an array exists, else, an include is not found'''

    match = re.findall('(#include *\"(.*?.(h|hpp))\")|(#include *\<(.*?.(h|hpp))\>)', myline)
    newstr = myline
    if len(match):
        newstr = newstr.replace("<", "\"") 
        newstr = newstr.replace(">", "\"")
        include_thingy = re.findall('(#include *\"(.*?.(h|hpp))\")', newstr)
        include_path = include_thingy[0][1]
        relative_path = os.path.relpath("/Users/vars/OneDrive - International Institute of Information Technology/CXX_Dependency_Automation/opencv2", file_path)
        if include_path not in c_headers:
            newstr = "#include \"" + relative_path + "/" + include_path + "\"\n"
            print("MODIFIED INCLUDE IN ",file_path + "IS: " +  newstr)
        # get relative path of folder enclosing opencv2 from the current c++ file 
    return newstr
    
    
def preprocess_includes(file_path, file_path2):
    # read file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # write file
    with open(file_path2, 'w') as f2:
        for line in lines:
            f2.write(changed_line(line, file_path))
    f2.close()
    f.close()

