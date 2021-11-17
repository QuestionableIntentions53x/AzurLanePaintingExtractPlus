import collections
import os
import re
import time
from itertools import filterfalse
from typing import Dict, Tuple

import wx

from core.src.static_classes.static_data import GlobalData
from core.src.structs_classes.basic_class import BasicInfo, BasicInfoList


class PerInfo(BasicInfo):
    def __init__(self, name, val, has_cn):
        super(PerInfo, self).__init__(name, val)
        self.sub_data = 1

        self.tex_step = 2
        self.mesh_step=2
        self.data = GlobalData()
        # tree储存结构组
        self._tex_path = "Empty"
        self.more_tex = ["Empty"]
        self._mesh_path = "Empty"
        self.more_mesh = ["Empty"]
        # 目标文件位置
        self.lay_in = ""
        # 是否可以使用还原
        self._is_able_work = False
        # 导出目标位置
        self._save_path: str = ""
        # 中文名称
        self.cn_name = val
        self.has_cn = has_cn
        # 父组件
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
            "change_local"
        ]
        # 是否以中文保存
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
        # 名称
        self.key = key = tree.AppendItem(self.tree_ID, f"名称：{self.cn_name}")
        if self.is_able_work:
            tree.SetItemTextColour(key, wx.Colour(253, 86, 255))
        tree.AppendItem(self.tree_ID, f"索引名称：{self.name}")
        # texture
        self.tex_id = tree.AppendItem(self.tree_ID, f"Texture文件路径：{self.tex_path}")

        more_tex_id = tree.AppendItem(self.tree_ID, f"其他Texture路径({len(self.more_tex)})")
        for each_path in self.more_tex:
            val = tree.AppendItem(more_tex_id, each_path)
            self.more_tex_per_id.append(val)
        # mesh
        self.mesh_id = tree.AppendItem(self.tree_ID, f"Mesh文件路径：{self.mesh_path}")

        more_mesh_id = tree.AppendItem(self.tree_ID, f"其他Mesh路径({len(self.more_mesh)})")
        for each_path in self.more_mesh:
            val = tree.AppendItem(more_mesh_id, each_path)
            self.more_mesh_per_id.append(val)

        action_root = tree.AppendItem(self.tree_ID, "功能按键")
        # 功能键
        independent = self.action_group[self.data.at_independent] = tree.AppendItem(action_root, "将当前的组合独立")
        tree.SetItemTextColour(independent, wx.Colour(255, 0, 166))

        face_match = self.action_group[self.data.at_face_match] = tree.AppendItem(action_root, "为当前立绘添加附加表情")
        tree.SetItemTextColour(face_match, wx.Colour(0, 16, 166))

        atlas_spilt = self.action_group[self.data.at_atlas_split] = tree.AppendItem(action_root, "进行Q版小人切割")
        tree.SetItemTextColour(atlas_spilt, wx.Colour(140, 0, 166))

        sprite_spilt = self.action_group[self.data.at_sprite_split] = tree.AppendItem(action_root, "进行Sprite切割 ")
        tree.SetItemTextColour(sprite_spilt, wx.Colour(248, 40, 255))

        set_able = self.action_group[self.data.at_set_able] = tree.AppendItem(action_root,
                                                                              f"强制转换为可还原状态【当前{self.must_able}】")
        tree.SetItemTextColour(set_able, wx.Colour(255, 177, 166))

        split_only = self.action_group[self.data.at_split_only] = tree.AppendItem(action_root, "仅进行立绘还原切割 ")
        tree.SetItemTextColour(split_only, wx.Colour(248, 66, 255))

        remove_item = self.action_group[self.data.at_remove_item] = tree.AppendItem(action_root, "删除该元素 ")
        tree.SetItemTextColour(remove_item, wx.Colour(248, 0, 255))
        
        change_local = self.action_group[self.data.at_change_local] = tree.AppendItem(action_root, "修改本地化 ")
        tree.SetItemTextColour(change_local, wx.Colour(248, 44, 255))

    def append_to_tree(self, tree: wx.TreeCtrl, tree_root: wx.TreeItemId):
        """
        添加到树，构建tree列表
        :param tree: tree 对象
        :param tree_root: 根id
        :return:
        """
        self.more_mesh_per_id.clear()
        self.more_tex_per_id.clear()

        self.tree_ID = tree.AppendItem(tree_root, self.cn_name)
        self.append_item_tree(tree)

    def get_select(self, type_is: bool):
        """
        获取选中的列表
        :param type_is: true ：texture，false：mesh
        :return: list，选中的列表
        """
        if type_is:
            return self.more_tex
        else:
            return self.more_mesh

    # 路径设置相关
    def set_tex(self, index):
        self.tex_path = self.more_tex[index]
        return self.tex_id, f"Texture文件路径：{self.tex_path}"

    def set_mesh(self, index):
        self.mesh_path = self.more_mesh[index]
        return self.mesh_id, f"Mesh文件路径：{self.mesh_path}"

    def add_save(self, path):
        self.save_path = path

    def clear_tex(self):
        self.tex_id, self.more_tex, self.tex_path, self.more_tex_per_id = None, [], "Empty", []

    def clear_mesh(self):

        self.mesh_id, self.more_mesh, self.mesh_path, self.more_mesh_per_id = None, [], "Empty", []

    def update_name(self,names:dict):
        if self.name in names.keys():
            self.has_cn=True;
            self.cn_name=names.get(self.name)
        

    def build_sub(self, value_type, file_type, index):
        """
        从自身的treeid中寻找目标
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
        # 独立
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

    # 显示部分
    def show_in_tree(self, tree, tree_root):
        list(map(lambda x: self._info_dict[x].append_to_tree(tree, tree_root), self._key_list))

    def append(self, name, cn_name, has_cn):
        value = PerInfo(name, cn_name, has_cn)

        self[value.name] = value
        return value

    def remove(self, item: collections.abc.Iterable):
        return PerWorkList(super(PerWorkList, self).remove(item))

    # 查找部分
    def find_by_id(self, id):
        values = list(filter(lambda x: self._info_dict[x].tree_ID == id, self._key_list))
        if values.__len__() == 0:
            return False, None
        return True, self[values[0]]

    def find_in_each(self, id) -> Tuple[bool, bool, bool, int, PerInfo]:
        """
        从每一个中寻找指定id
        :param id:
        :return: (是否成功，类型【单个True，列表False】，类型[tex(True),mesh(False)]，索引，对象本身)
        """
        target = None
        for value in self:
            # 如果id为以下的部分，进入
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
        查找是否为特殊动作按键
        :param id:
        :return: 是否成功【true/false】，动作类型，作用目标
        """
        target = None
        for value in self:
            # 如果id为以下的部分，进入
            if id in value.action_group:
                target = value
                break
        if target is None:
            return False, -1, target
        else:
            index = target.action_group.index(id)
            return True, index, target

    # 添加部分
    def set_tex(self, value, name=None):
        """
        添加贴图
        :param name: [可选]新添加的texture地址的指向项目名称，为None会根据value获取
        :param value: 新添加的texture地址
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

            # 赋值过程
            val: PerInfo = self._info_dict[key]
            if value not in val.more_tex:
                val.more_tex.append(value)

            lower_path = os.path.split(value)[0].lower()
            # 如果非空考虑优先级
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
               添加mesh网格
               :param name: [可选]新添加的mesh地址的指向项目名称，为None会根据value获取
               :param value: 新添加的mesh地址
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
            # 如果非空考虑优先级
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
        添加新对象
        :param names: 预设键-值对应组
        :param name: 对象索引key
        :param has_cn: 对象是否有中文名
        :return:
        """
        # if name == "unknown4":
        #     print(name)
        if self.is_ignore_case:
            name=name.lower()

        if name not in self._key_list:
            if name not in names.keys():
                has_cn = False
                target_cn = name
            else:
                has_cn = True
                target_cn = names[name]
            # 如果中文名为空，也认为没有中文名
            if target_cn == "":
                target_cn = name
                has_cn = False

            value = PerInfo(name, target_cn, has_cn)
            value.parent = self

            self[name] = value

            return name
        else:
            return name

    # 清空部分
    def clear_mesh(self):
        list(map(lambda x: x.clear_mesh(), self))

    def clear_tex(self):
        list(map(lambda x: x.clear_tex(), self))

    # 生成部分
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
