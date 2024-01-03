import json
import os

import requests
import wx

from .design_frame import MyDialogUpdateLocation
from ..structs_classes.location_group import LocationList


class LocationUpdate(MyDialogUpdateLocation):
    def __init__(self, parent, names, path, local_data):
        super(LocationUpdate, self).__init__(parent)
        self.path = path
        self.names = names
        self.load_data = {}

        self.root = self.m_treeCtrl_info.AddRoot("")

        self.local_work = LocationList()

        self.available_list = local_data
        self.exist_size = 0

    def MyDialogUpdateLocationOnInitDialog(self, event):
        names = [a for a in self.available_list.keys()]
        self.m_listBox_select.Set(names)
        self.exist_size = len(names)

    def compare(self):
        self.local_work = LocationList()
        self.local_work.compare(self.names, self.load_data)
        self.m_treeCtrl_info.DeleteChildren(self.root)
        self.local_work.add_to_tree(self.m_treeCtrl_info, self.root)

    def update(self, data):
        self.m_staticText_info.SetLabel("Updating data...")
        for key, item in data.items():
            self.names[key] = item
        with open(os.path.join(self.path, "core\\assets\\names.json"), "w")as file:
            json.dump(self.names, file)

        wx.MessageBox("Done!", "Message", wx.ICON_INFORMATION)
        self.Destroy()

    def request_info(self, event):
        index = event.GetString()

        def work():
            try:
                r = requests.get(self.available_list[index], timeout=1000)
                if r.status_code == 200:
                    self.load_data = json.loads(r.text)
                self.compare()
                self.m_staticText_info.SetLabel(f"Loading completed! From the localization solution provided by {event.GetString()}")
            except Exception as info:
                wx.MessageBox(f"{info.__str__()}")

        self.m_staticText_info.SetLabel(f"Loading, please wait~~")
        work()

    def load_file(self, event):
        dialog = wx.FileDialog(self, "Select json file", self.path, "Names.json", "*.json",
                               wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST)

        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()

            with open(path, "r")as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.load_data = data

            self.m_staticText_info.SetLabel("Loading completed! From local file")

            self.compare()

    def add_local(self, event):
        is_new_name = False
        canceled = False
        name = ''
        while not is_new_name:
            dialog = wx.TextEntryDialog(parent=self, message="New localized resource label (cannot have the same name as an existing localized resource label)", caption="Add label",
                                        value=f"Localized resources-{self.exist_size + 1}")
            if dialog.ShowModal() == wx.ID_OK:
                name = dialog.GetValue()
                if name not in self.available_list.keys():
                    is_new_name = True
                else:
                    wx.MessageBox("This label already exists!", "Error", wx.ICON_ERROR)
            else:
                canceled = True
                break
        if canceled:
            return
        dialog_url = wx.TextEntryDialog(parent=self, message="Add localized resource address", caption="Add address", value='')
        if dialog_url.ShowModal() == wx.ID_OK:
            url = dialog_url.GetValue()
            self.available_list[name] = url
            self.m_listBox_select.Append(name)
            self.exist_size += 1

    def remove_data(self, event):
        key = self.m_listBox_select.GetStringSelection()
        del self.available_list[key]
        self.m_listBox_select.Clear()
        self.MyDialogUpdateLocationOnInitDialog(event)

    def apply_all(self, event):
        data = self.local_work.transform_all()
        self.update(data)

    def apply_cover(self, event):
        data = self.local_work.transform_cover()
        self.update(data)

    def apply_new(self, event):
        data = self.local_work.transform_new()
        self.update(data)

    def cancel(self, event):
        self.Destroy()

    def get_local_data(self):
        return self.available_list
