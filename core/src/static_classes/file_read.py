import functools
import os
import os.path as op
import re
import traceback

import gettext
_ = gettext.gettext

from core.src.static_classes.static_data import GlobalData
from core.src.structs_classes.extract_structs import PerWorkList


class FileFilter(object):
    # File processing

    @staticmethod
    def file_deal(paths, info_list: PerWorkList, clear_list: bool = False, pattern=r'^[.\n]*$',
                  is_file=True,
                  replace_str: str = '', names: dict = None, type_set=1):
        data = GlobalData()

        def info_write_builder(is_files, dict_path_group, replace_string, info_group,
                               names_dict, type_use):
            def info_write(per_path):
                if not is_files:
                    name = per_path
                    per_path = dict_path_group[name]
                    name = op.splitext(name)[0].replace(replace_string, '')
                else:
                    name = op.splitext(op.basename(per_path))[0].replace(replace_string, '')

                name = re.sub(r'\s#\d+?$', "", name, flags=re.IGNORECASE)

                key = info_group.append_name(name, names_dict)

                if type_use == data.fi_texture_type:
                    info_group.set_tex(per_path, key)
                if type_use == data.fi_mesh_type:
                    info_group.set_mesh(per_path, key)

            return info_write

        try:
            if names is None:
                names = {}

            pattern_re = re.compile(pattern)
            if not is_file:
                dict_path = paths.copy()
                paths = paths.keys()
                num = len(paths)
            else:
                dict_path = {}
                num = len(info_list)

            if clear_list:
                if type_set == 2:
                    info_list.clear_mesh()
                if type_set == 1:
                    info_list.clear_tex()
                num = 0

            if not len(paths) == 0:

                path = filter(lambda x: pattern_re.match(
                    re.sub(r'\s#\d+?(?=\.png|obj)', "", os.path.basename(x), flags=re.IGNORECASE)) is not None, paths)
                path = list(path)

                info_write2 = info_write_builder(is_file, dict_path, replace_str, info_list,
                                                 names, type_set)

                path_len = len(path)

                num += len(list(map(info_write2, path)))

                if path_len == 0:
                    return False, _('Import completed, no new items!')
            else:
                return False, _('Import failed, no items to import!')
        except Exception as info:
            #  raise
            print(''.join(traceback.format_tb(info.__traceback__)))
            return False, _('Import failed, an error occurred! {}').format(info.__str__)
        else:
            return True, _('Import successful! Successfully imported {} items!').format(num)

    # Recursive file reading
    @staticmethod
    def build_return_list(x, y):
        x = list(x)
        x.extend(list(y))

        return x

    @staticmethod
    def all_file(dir_name, skip_type=r'^UISprite.+$'):
        """
        a function to get all file in a dir
        :param dir_name: the path to get all files
        :param skip_type: the file name pattern which are skipped
        :return: the all files path
        """
        list_keep = os.listdir(dir_name)

        skip_pattern = re.compile(skip_type, flags=re.IGNORECASE)
        out_list = filter(lambda x: os.path.isfile(dir_name + "\\" + x) and skip_pattern.match(x) is None, list_keep)
        out_list = map(lambda x: dir_name + "\\" + x, out_list)

        dir_list = filter(lambda x: os.path.isdir(dir_name + "\\" + x), list_keep)
        dir_list = map(lambda x: dir_name + "\\" + x, dir_list)
        dir_list = map(lambda x: FileFilter.all_file(x, skip_type), dir_list)

        out_list = list(out_list)
        dir_list = list(dir_list)

        return_list = functools.reduce(FileFilter.build_return_list, dir_list, out_list)

        return_list = list(return_list)

        return return_list
