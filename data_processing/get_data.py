#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

ID = 1927 # address building footprints

def main(ID, key=None):
    url = 'http://api.data.mos.ru/v1/datasets/{0}/features'.format(ID)
    print 'Getting data from {0}'.format(url)

    r = requests.get(url)
    if r.status_code != 200:
        print r.status
    else:
        result = r.json()
        with open('raw.json', 'w') as f:
            json.dump(result, f)
        print 'done!'


if __name__ == '__main__':
    main(ID)
