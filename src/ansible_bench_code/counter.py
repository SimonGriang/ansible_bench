from datetime import datetime
from multiprocessing import process
import os
import subprocess
import re
import time


i = 0
while(True):
    i += 1
    if (i > 4):
        print (f"Abbruch bei nach {i} Durchläufen")
        break
    print(i)
