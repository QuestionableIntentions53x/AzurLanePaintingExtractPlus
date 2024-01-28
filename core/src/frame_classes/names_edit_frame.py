import json
import os
from collections import OrderedDict

import wx
from wx.core import MessageBox

import gettext
_ = gettext.gettext

from core.src.frame_classes.design_frame import MyDialogKetValueSetting

class NamesEditFrame(MyDialogKetValueSetting):
    def __init__(self, parent, names, path, miss_list: list):
        super(NamesEditFrame, self).__init__(parent, parent.frame.frame.tl)
        self.names = names
        self.edit_group = OrderedDict(self.names)
        self.key_group = list(self.edit_group.keys())
        self.show_list = []
        self.path = path
        self.is_changed = False

        self.miss_list = miss_list
        self.miss_temp = miss_list.copy()

    @staticmethod
    def string_format(key, value):
        return f'"{key}"->"{value}"'

    def get_names(self):
        return self.names

    def clear_data(self):
        self.m_textCtrl_new_value.Clear()
        self.m_textCtrl_new_key.Clear()

    def editor_init(self, event):
        for key, item in self.edit_group.items():
            self.show_list.append(f'"{key}"->"{item}"')

        self.m_listBox_name_exist.Clear()
        self.m_listBox_name_exist.Set(self.show_list)

    def view_item(self, event):
        index = event.GetSelection()
        key = self.key_group[index]
        value = self.edit_group.get(key)
        wx.MessageBox("'{}'->'{}'".format(key, value), "information")

    def edit_exist_item(self, event):
        index = event.GetSelection()
        key = self.key_group[index]
        value = self.edit_group.get(key)

        self.m_textCtrl_new_key.SetValue(key)
        self.m_textCtrl_new_value.SetValue(value)

    def add_item(self, event):
        key = self.m_textCtrl_new_key.GetValue()
        value = self.m_textCtrl_new_value.GetValue()

        if key == "" or value == "":
           wx.MessageBox(_("Key or value cannot be blank!"), _("Error"), wx.ICON_ERROR)

        else:
            if key in self.key_group:
                index = self.key_group.index(key)
                feedback = wx.MessageBox(
                    _("[{}] already exists in the key group. Clicking [Confirm] will overwrite it with the new value").format(key), _("Information"), wx.YES_NO | wx.ICON_INFORMATION)
                if feedback == wx.YES:
                    self.edit_group[key] = value
                    self.m_listBox_name_exist.SetString(
                        index, f'"{key}"->"{value}"')
                    self.is_changed = True

            else:
                self.key_group.append(key)
                self.edit_group[key] = value
                self.is_changed = True
                self.m_listBox_name_exist.Append(f'"{key}"->"{value}"')

            self.clear_data()

    def clear_item(self, event):
        self.clear_data()

    def import_names(self, event):
        overwrite = 0
        new_item = 0
        dialog = wx.FileDialog(self, _("Select localization file (.json)"), os.path.join(self.path, "core\\assets"), "names.json", "*json",
                               wx.FD_FILE_MUST_EXIST | wx.FD_OPEN)
        is_ok = dialog.ShowModal()
        if is_ok == wx.ID_OK and is_ok != wx.ID_CANCEL and is_ok != wx.ID_ABORT:
            try:
                with open(dialog.GetPath(), "r")as file:
                    temple = json.load(file)
                for key, item in temple.items():
                    if not isinstance(item, str):
                        raise TypeError(_("Invalid file"))
                    self.edit_group[key] = item
                    if key in self.key_group:
                        overwrite += 1
                        index = self.key_group.index(key)
                        self.m_listBox_name_exist.SetString(
                            index, self.string_format(key, item))
                    else:
                        new_item += 1
                        self.m_listBox_name_exist.Append(
                            self.string_format(key, item))

                wx.MessageBox(
                    _("Import key-value pair file successfully!\n\tOverwrite: {}\n\tAdd: {}").format(overwrite, new_item), _("Information"))
                self.is_changed = True
            except Exception as info:
                wx.MessageBox(_("Error importing key-value pair file!\n{}").format(info.__str__()))

    def close_save(self, event):
        if self.is_changed:
            feedback = wx.MessageBox(
                _("Apply these changes?"), _("Information"), wx.ICON_INFORMATION | wx.YES_NO)
            if feedback == wx.YES:
                save_data = {k.lower(): v for k, v in self.edit_group.items()}
                with open(os.path.join(self.path, "core\\assets\\names.json"), "w")as file:
                    json.dump(save_data, file, indent=4)

                self.names = dict(self.edit_group)

        super(NamesEditFrame, self).close_save(event)

    def next_miss(self, event):
        key = self.m_textCtrl_new_key.GetValue()
        value = self.m_textCtrl_new_value.GetValue()

        if not (key == '' and value == ''):

            self.add_item(event)

        if len(self.miss_list) > 0:
            data = self.miss_list.pop()
            self.m_textCtrl_new_key.SetValue(str(data))
        else:
            MessageBox(_("The unnamed localization queue has been emptied"),_("Warning"),wx.OK|wx.ICON_WARNING)