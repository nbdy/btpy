from os.path import isfile, isdir
import json
from datetime import datetime


class Static(object):
    timestamp_format = "%d.%m.%Y %H:%M:%S"

    @staticmethod
    def make_timestamp():
        return datetime.now().strftime(Static.timestamp_format)

    @staticmethod
    def save(obj, path):
        if isdir(path):
            fpath = path + obj.address.replace(':', '').lower() + ".json"
            if isfile(fpath):
                fdata = json.load(open(fpath))
            else:
                fdata = {}
            fdata.update(obj.to_dict())
            with open(fpath, 'w') as o:
                json.dump(fdata, o)

    @staticmethod
    def save_multiple(objs, path):
        for obj in objs:
            Static.save(obj, path)
