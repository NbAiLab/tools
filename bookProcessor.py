import sys
import os
import math
import numpy as np
import glob
import argparse
from os import path

from xmlHandler import xmlHandler
from altoProcessor import altoProcessor

if __name__ == '__main__':
    bookProcessor=altoProcessor()
    bookProcessor.ReadBook("../notram/testbok")