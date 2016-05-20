#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

import json


def hasKeys(obj, keys):
    if not obj:
        return False
    if not keys:
        return False
    if set(keys).issubset(obj):
        return True
    return False


def dumpObj(obj):
    if not obj:
        return
    print(json.dumps(obj, ensure_ascii=False, indent=2))
