import FlexUI

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--csv_name',default='Flex_1117.csv')
args = parser.parse_args()

def test_xjk():
    # print(args.filename)
    FlexUI.run(args)
test_xjk()