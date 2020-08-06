## Python执行可执行文件的方法demo

```python

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shlex
import subprocess
from threading import Thread
from xml.dom import pulldom
import warnings
import platform
try:
    import pwd
except ImportError:
    pass


class MasscanProcess(Thread):

    def __init__(self):
        Thread.__init__(self)

        self.cmd = '/usr/bin/sudo /Users/chiweiwei/Development/PortAg/PortAg/bin/masscan -oJ - -p22,8080,80 -n -Pn 10.0.0.0/24'

    def run(self):
        proc = subprocess.Popen(args=shlex.split(self.cmd),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                bufsize=0)

        print(proc.poll())
        print("---------------")
        while proc.poll() is None:
            for stre in iter(proc.stderr.readline, ''):
                print(stre)

            for streamline in iter(proc.stdout.readline, ''):
                print(streamline)

        print(proc.stderr.read())
        print("+++++++++++++")
        print(proc.poll())


if __name__ == '__main__':
    # m = MasscanProcess()
    # m.start()

    import re
    m = re.match(r'Starting\smasscan\s([\d\.]{5}) \(.+?\)\sat\s([\d\-\s\:]{19}) GMT\n', 'Starting masscan 1.0.6 (http://bit.ly/14GZzcT) at 2020-01-04 08:53:31 GMT\n')
    print(m.group(2))


```