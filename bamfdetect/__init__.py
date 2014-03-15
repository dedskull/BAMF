from sys import path
import modules
import modules.common
from os import listdir
from os.path import isfile, isdir, join, abspath, dirname

path.append(dirname(abspath(__file__)))


def get_version():
    return "1.1.0"


def get_loaded_modules():
    l = []
    for m in modules.common.Modules.list:
        l.append(m.get_metadata())
    return l


def scan_paths(paths, only_detect, recursive, module_filter):
    results = {}
    while len(paths) != 0:
        file_path = abspath(paths[0])
        del paths[0]
        if isfile(file_path):
            with open(file_path, mode='rb') as file_handle:
                file_content = file_handle.read()
                for m in modules.common.Modules.list:
                    if module_filter is not None and m.get_module_name() not in module_filter:
                        continue
                    if m.is_bot(file_content):
                        results[file_path] = {}
                        if not only_detect:
                            results[file_path]["information"] = m.get_bot_information(file_content)
                        results[file_path]["type"] = m.get_bot_name()
                        results[file_path]["module"] = m.get_module_name()
                        results[file_path]["description"] = m.get_metadata().description
        elif isdir(file_path):
            for p in listdir(file_path):
                p = join(file_path, p)
                if isfile(p) or (isdir(p) and recursive):
                    paths.append(p)
    return results