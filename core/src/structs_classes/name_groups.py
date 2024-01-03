import wx

from .basic_class import BasicInfoList, BasicInfo


class NameGroups(BasicInfoList):
    def __init__(self, item):
        super(NameGroups, self).__init__(item=item)

    def show_in_tree(self, tree: wx.TreeCtrl, root: wx.TreeItemId):
        for value in self:
            value: NameInfo
            value.init_add2tree(tree, root)
            value.add2tree()

    def add_new_name(self, key, value):
        if key not in self._key_list:
            new_name = NameInfo(key, value)
            new_name.add_location(key, value)


class NameInfo(BasicInfo):
    """
    Localization processing class
    Group objects with the same suffix removed and placed together
    """

    def __init__(self, name, val):
        super(NameInfo, self).__init__(name, val)
        self.all_location = {}
        # tree id
        self.title_id = ...
        self.all_ids = []

        # self.content_id = ...
        self.tree = ...

    def add_location(self, key, name):
        """
        First check if the key is a localized object in this group
        :param key:
        :param name:
        :return: bool success or not
        """
        if key in self.all_location.keys():
            return False
        else:
            self.all_location[key] = name
            return True

    def init_add2tree(self, tree: wx.TreeCtrl, root: wx.TreeItemId):
        """
        Initialize adding to the tree [create title]
        :param tree:
        :param root:
        :return:
        """
        pass

    def add2tree(self):
        """
        Add this object to the target tree
        :return:
        """
        pass

    def add2tree_single(self, key="", value=""):
        """
        Add a single item to the tree
        :param key:
        :param value:
        :return:
        """

    def transform2dict(self):
        """
        Convert to dictionary type
        :return:
        """
        return self.all_location

    def is_self_key(self, id):
        if id == self.title_id or id in self.all_ids:
            return True
        return False
