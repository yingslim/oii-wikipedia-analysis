import os
import sys

CURR_DIR = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
PROJECT_ROOT =  os.path.dirname(CURR_DIR).replace("\\", "/")
sys.path.append(PROJECT_ROOT)

DATA_DIR = os.path.join(PROJECT_ROOT, 'data').replace("\\", "/")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output').replace("\\", "/")

print(CURR_DIR)