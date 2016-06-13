#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def generateCode():
    with open('./cityCode.log', mode='r') as fin:
        for line in fin:
            if len(line) > 0:
                #  print('processing {}'.format(line))
                pass
            try:
                codeObjs = json.loads(line)[0]
                print(
                    '"{}|{}|{}|{}",'.format(
                        codeObjs['Title'],
                        codeObjs['DisplayTitle'],
                        codeObjs['RCode'],
                        codeObjs['Synonyms'])
                )
            except Exception as e:
                #  raise e
                #  print(e.args)
                pass

if __name__ == "__main__":
    print('static String[] Cities = {\n')
    generateCode()
    print('};')
