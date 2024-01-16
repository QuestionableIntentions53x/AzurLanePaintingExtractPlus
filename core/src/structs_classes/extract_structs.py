import collections
import os
import re
import time
from itertools import filterfalse
from typing import Dict, Tuple

import wx

from core.src.static_classes.static_data import GlobalData
from core.src.structs_classes.basic_class import BasicInfo, BasicInfoList

import gettext
_ = gettext.gettext

class PerInfo(BasicInfo):
    def __init__(self, name, val, has_cn):
        super(PerInfo, self).__init__(name, val)
        self.sub_data = 1

        self.tex_step = 2
        self.mesh_step = 2
        self.data = GlobalData()
        # tree storage structure group
        self._tex_path = "Empty"
        self.more_tex = ["Empty"]
        self._mesh_path = "Empty"
        self.more_mesh = ["Empty"]
        # target file location
        self.lay_in = ""
        # whether restoration is possible
        self._is_able_work = False
        # export target location
        self._save_path: str = ""
        # Chinese name
        self.cn_name = val
        self.has_cn = has_cn
        # parent component
        self.parent = None

        self.must_able = False

        # tree ID
        self.key = ...
        self.tree_ID = ...
        self.tex_id = ...
        self.more_tex_per_id = []
        self.mesh_id = ...
        self.more_mesh_per_id = []

        self.action_group = [
            "independent",
            "face_match",
            "atlas_split",
            "set_able",
            "split_only",
            "remove_item",
            "sprite_spilt",
            "change_local",
            "import_sprite"
        ]
        # whether to save as Chinese
        self._is_save_as_cn = True

    def __contains__(self, item):
        if self.name in item or self.cn_name in item:
            return True
        else:
            return False

    @property
    def is_able_work(self):
        if self.must_able:
            return True
        else:
            return self._is_able_work

    @property
    def tex_path(self):
        return self._tex_path

    @tex_path.setter
    def tex_path(self, value):
        self._tex_path = value
        self._is_able_work = self.is_able()

    @property
    def mesh_path(self):
        return self._mesh_path

    @mesh_path.setter
    def mesh_path(self, value):
        self._mesh_path = value
        self._is_able_work = self.is_able()

    @property
    def save_path(self):
        return self._save_path

    @save_path.setter
    def save_path(self, value):
        if self._is_save_as_cn:
            self._save_path = os.path.join(value, self.cn_name + ".png")
        else:
            self._save_path = os.path.join(value, self.name + ".png")

    @property
    def is_save_as_cn(self):
        return self._is_save_as_cn

    @is_save_as_cn.setter
    def is_save_as_cn(self, value):
        if isinstance(value, bool):
            self._is_save_as_cn = value

    @staticmethod
    def is_def(val):
        return bool(val)

    def get_is_able_work(self):
        return self._is_able_work

    def is_able(self):
        if os.path.isfile(self.tex_path) and os.path.isfile(self.mesh_path):
            return True
        else:
            return False

    def transform_able(self):
        self.must_able = not self.must_able

    def set_single_path(self, path):
        self._save_path = path

    def append_item_tree(self, tree: wx.TreeCtrl):
        # name
        self.key = key = tree.AppendItem(self.tree_ID, f"Name: {self.cn_name}")
        if self.is_able_work:
            tree.SetItemTextColour(key, wx.Colour(253, 86, 255))
        tree.AppendItem(self.tree_ID, f"Index name: {self.name}")
        # texture
        self.tex_id = tree.AppendItem(self.tree_ID, f"Texture file path: {self.tex_path}")

        more_tex_id = tree.AppendItem(self.tree_ID, f"Other Texture path({len(self.more_tex)})")
        for each_path in self.more_tex:
            val = tree.AppendItem(more_tex_id, each_path)
            self.more_tex_per_id.append(val)
        # mesh
        self.mesh_id = tree.AppendItem(self.tree_ID, f"Mesh file path: {self.mesh_path}")

        more_mesh_id = tree.AppendItem(self.tree_ID, f"Other Mesh path({len(self.more_mesh)})")
        for each_path in self.more_mesh:
            val = tree.AppendItem(more_mesh_id, each_path)
            self.more_mesh_per_id.append(val)

        action_root = tree.AppendItem(self.tree_ID, "Function Button")
        # Function keys
        independent = self.action_group[self.data.at_independent] = tree.AppendItem(action_root,
                                                                                    _("Duplicate"))
        tree.SetItemTextColour(independent, wx.Colour(255, 0, 166))

        face_match = self.action_group[self.data.at_face_match] = tree.AppendItem(action_root,
                                                                                    _("Import facial expression"))
        tree.SetItemTextColour(face_match, wx.Colour(0, 16, 166))

        atlas_spilt = self.action_group[self.data.at_atlas_split] = tree.AppendItem(action_root,
                                                                                    _("Atlas slicer"))
        tree.SetItemTextColour(atlas_spilt, wx.Colour(140, 0, 166))

        sprite_spilt = self.action_group[self.data.at_sprite_split] = tree.AppendItem(action_root,
                                                                                      _("Sprite slicer"))
        tree.SetItemTextColour(sprite_spilt, wx.Colour(248, 40, 255))

        set_able = self.action_group[self.data.at_set_able] = tree.AppendItem(action_root,
                                                                              _("Force to a reversible state [{}]").format(self.must_able))
        tree.SetItemTextColour(set_able, wx.Colour(255, 177, 166))

        split_only = self.action_group[self.data.at_split_only] = tree.AppendItem(action_root,
                                                                                  _("Export sprite sliced on texture boundry"))
        tree.SetItemTextColour(split_only, wx.Colour(248, 66, 255))

        remove_item = self.action_group[self.data.at_remove_item] = tree.AppendItem(action_root,
                                                                                    _("Delete"))
        tree.SetItemTextColour(remove_item, wx.Colour(248, 0, 255))

        """change_local = self.action_group[self.data.at_change_local] = tree.AppendItem(action_root,
                                                                                      "Modify localization")
        tree.SetItemTextColour(change_local, wx.Colour(248, 44, 255))"""
        
        import_sprite = self.action_group[self.data.at_import_sprite] = tree.AppendItem(action_root,
                                                                                      _("Convert PNG to tex"))
        tree.SetItemTextColour(import_sprite, wx.Colour(248, 44, 200))

    def append_to_tree(self, tree: wx.TreeCtrl, tree_root: wx.TreeItemId):
        """
        Add to tree, build tree list
        :param tree: tree object
        :param tree_root: root id
        :return:
        """
        self.more_mesh_per_id.clear()
        self.more_tex_per_id.clear()

        self.tree_ID = tree.AppendItem(tree_root, self.cn_name)
        self.append_item_tree(tree)

    def get_select(self, type_is: bool):
        """
        Get selected list
        :param type_is: true: texture, false: mesh
        :return: list, selected list
        """
        if type_is:
            return self.more_tex
        else:
            return self.more_mesh

    # Path setting related
    def set_tex(self, index):
        self.tex_path = self.more_tex[index]
        return self.tex_id, f"Texture file path: {self.tex_path}"

    def set_mesh(self, index):
        self.mesh_path = self.more_mesh[index]
        return self.mesh_id, f"Mesh file path: {self.mesh_path}"

    def add_save(self, path):
        self.save_path = path

    def clear_tex(self):
        self.tex_id, self.more_tex, self.tex_path, self.more_tex_per_id = None, [], "Empty", []

    def clear_mesh(self):
        self.mesh_id, self.more_mesh, self.mesh_path, self.more_mesh_per_id = None, [], "Empty", []

    def update_name(self, names: dict):
        if self.name in names.keys():
            self.has_cn = True
            self.cn_name = names.get(self.name)

    def build_sub(self, value_type, file_type, index):
        """
        Find the target from its own treeid
        :param value_type:
        :param file_type:
        :param index:
        :return:
        """
        val = PerInfo(self.name, self.val, self.has_cn)
        if value_type == self.data.td_single:
            if file_type == self.data.td_texture_type:
                val.tex_path = self.tex_path
            elif file_type == self.data.td_mesh_type:
                val.mesh_path = self.mesh_path
        elif value_type == self.data.td_list_item:
            if file_type == self.data.td_texture_type:
                val.tex_path = self.more_tex[index]
            elif file_type == self.data.td_mesh_type:
                val.mesh_path = self.more_mesh[index]

        return os.path.isfile(val.tex_path), val

    def independent(self, name, tree, tree_root):
        # independent
        target = PerInfo(name, f"{self.val}-# {self.sub_data}", self.has_cn)
        target.tex_path = self.tex_path
        target.mesh_path = self.mesh_path
        target.append_to_tree(tree, tree_root)
        self.parent[target.name] = target
        self.sub_data += 1


class PerWorkList(BasicInfoList):
    def __init__(self, item: collections.abc.Iterable = None, mesh_match=None, texture_match=None,
                 is_ignore_case=False):
        super(PerWorkList, self).__init__(item)
        self.is_ignore_case = is_ignore_case
        self.texture_match = texture_match
        self.mesh_match = mesh_match
        self.data = GlobalData()

    # Show part
    def show_in_tree(self, tree, tree_root):
        list(map(lambda x: self._info_dict[x].append_to_tree(tree, tree_root), self._key_list))

    def append(self, name, cn_name, has_cn):
        value = PerInfo(name, cn_name, has_cn)

        self[value.name] = value
        return value

    def remove(self, item: collections.abc.Iterable):
        return PerWorkList(super(PerWorkList, self).remove(item))

    # Find part
    def find_by_id(self, id):
        values = list(filter(lambda x: self._info_dict[x].tree_ID == id, self._key_list))
        if values.__len__() == 0:
            return False, None
        return True, self[values[0]]

    def find_in_each(self, id) -> Tuple[bool, bool, bool, int, PerInfo]:
        """
        Find the specified id from each
        :param id:
        :return: (whether successful, type [single True, list False], type [tex(True), mesh(False)], index, object itself)
        """
        target = None
        for value in self:
            # If the ID is in the following section, enter
            if id == value.tex_id == id or id in value.more_tex_per_id or value.mesh_id == id or \
                    id in value.more_mesh_per_id:
                target = value
        if target is None:
            return False, False, False, -1, None
        if id == target.tex_id:
            return True, self.data.td_single, self.data.td_texture_type, 0, target
        elif id == target.mesh_id:
            return True, self.data.td_single, self.data.td_mesh_type, 0, target
        elif id in target.more_tex_per_id:
            return True, self.data.td_list_item, self.data.td_texture_type, target.more_tex_per_id.index(id), target
        elif id in target.more_mesh_per_id:
            return True, self.data.td_list_item, self.data.td_mesh_type, target.more_mesh_per_id.index(id), target

    def find_action(self, id) -> Tuple[bool, int, PerInfo]:
        """
        Check if it is a special action button
        :param id:
        :return: Whether successful [true/false], action type, target
        """
        target = None
        for value in self:
            # If the ID is in the following section, enter
            if id in value.action_group:
                target = value
                break
        if target is None:
            return False, -1, target
        else:
            index = target.action_group.index(id)
            return True, index, target

    # Adding part
    def set_tex(self, value, name=None):
        """
        Add texture
        :param name: [Optional] The name pointing to the newly added texture address, None will be based on value
        :param value: The newly added texture address
        :return:
        """
        has_ = False
        if isinstance(value, str) and os.path.isfile(value):
            if name is not None:
                key = name
            else:
                key = os.path.splitext(os.path.basename(value))[0]
                if re.match(r'.+\s#\d+\.png', value, re.IGNORECASE):
                    has_ = True
                    key = re.split(r'\s#\d+(\[alpha\])?$', key)[0]

            # Assignment process
            val: PerInfo = self._info_dict[key]
            if value not in val.more_tex:
                val.more_tex.append(value)

            lower_path = os.path.split(value)[0].lower()
            # If non-empty, consider priority
            if 0 < val.tex_step and lower_path.endswith(self.texture_match[0]):
                val.tex_path = value
                val.tex_step = 0
            elif 1 < val.tex_step and lower_path.endswith(self.texture_match[1]):
                val.tex_path = value
                val.tex_step = 1
            else:
                val.tex_path = value
                val.tex_step = 2

            if not has_:
                val.tex_path = value

    def set_mesh(self, value, name=None):
        """
        Add mesh grid
        :param name: [optional] The name of the newly added mesh address, will be obtained from value if None
        :param value: The newly added mesh address
        :return:
        """
        has_ = False
        if isinstance(value, str) and os.path.isfile(value):
            if name is not None:
                key = name
            else:
                key = os.path.splitext(os.path.basename(value))[0]
                if re.match(r'.+\s#\d+\.obj', value, re.IGNORECASE):
                    has_ = True
                    key = re.split(r'\s#\d+(\[alpha\])?$', key)[0]

            val: PerInfo = self._info_dict[key]
            if value not in val.more_mesh:
                val.more_mesh.append(value)

            lower_path = os.path.split(value)[0].lower()
            # Consider priority if not empty
            if 0 < val.mesh_step and lower_path.endswith(self.mesh_match[0]):
                val.mesh_path = value
                val.mesh_step = 0
            elif 1 < val.mesh_step and lower_path.endswith(self.mesh_match[1]):
                val.mesh_path = value
                val.mesh_step = 1
            else:
                val.mesh_path = value
                val.mesh_step = 2
            if not has_:
                val.mesh_path = value

    def append_name(self, name, names: dict, *, has_cn=False):
        """
        Add a new object
        :param names: Preset key-value pairs
        :param name: Object index key
        :param has_cn: Whether the object has a Chinese name
        :return:
        """
        # if name == "unknown4":
        #     print(name)
        if self.is_ignore_case:
            name = name.lower()

        if name not in self._key_list:
            if name not in names.keys():
                has_cn = False
                target_cn = name
            else:
                has_cn = True
                target_cn = names[name]
            # If the Chinese name is empty, also consider it as having no Chinese name
            if target_cn == "":
                target_cn = name
                has_cn = False

            value = PerInfo(name, target_cn, has_cn)
            value.parent = self

            self[name] = value

            return name
        else:
            return name

    # Clearing section
    def clear_mesh(self):
        list(map(lambda x: x.clear_mesh(), self))

    def clear_tex(self):
        list(map(lambda x: x.clear_tex(), self))

    # Generation section
    def build_able(self):
        val = filter(lambda x: x.get_is_able_work(), self)
        value = PerWorkList(val)
        return value

    def build_unable(self):
        val = filterfalse(lambda x: x.get_is_able_work(), self)
        value = PerWorkList(val)
        return value

    def build_search(self):
        val = map(lambda x: f"{x.name}{x.cn_name}", self)
        return list(val)

    def build_filter(self):
        val = map(lambda x: f"{x.name}", self)
        val = list(enumerate(list(val), 0))
        return val

    def build_skip(self, filename):
        filename = list(map(lambda x: os.path.splitext(os.path.basename(x))[0], filename))

        val = filter(lambda x: x in filename, self)

        return PerWorkList(val)

    def build_from_indexes(self, indexes):
        val = map(lambda x: self[x], indexes)
        value = PerWorkList(val)
        return value

    def build_from_pattern(self, pattern):
        val = list(filter(lambda x: re.match(pattern, list(x)[1]), self.build_filter()))
        val = list(zip(*val))
        if len(val) == 2:
            return self.build_from_indexes(val[0])
        else:
            return PerWorkList()