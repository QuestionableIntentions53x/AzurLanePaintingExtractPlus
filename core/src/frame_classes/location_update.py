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

    # TODO: Load localization file found in height_setting.json for all languages
    def request_info(self, event):
        index = event.GetString()

        def work():
            try:
                r = requests.get(self.available_list[index], timeout=1000)
                # TODO: Place this in a config file too
                f = requests.get("https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/EN/ShareCfg/painting_filte_map.json", timeout=1000)
                if r.status_code == 200 and f.status_code == 200:
                    raw = json.loads(r.text)
                    names = dict()
                    
                    # Load base ship varieties
                    for ship in raw:
                        file_name = str(raw[ship]["painting"].lower())
                        name = raw[ship]["name"]
                        # Add the ship's name after the skin's name (exclude retrofits since it already has their name)
                        if name.find("(Retrofit)") == -1:
                            if file_name[:file_name.find("_")] in names:
                                name += " (" + names[file_name[:file_name.find("_")]] + ")"
                            elif file_name[:file_name.find("_", file_name.find("_") + 1)] in names:
                                name += " (" + names[file_name[:file_name.find("_", file_name.find("_") + 1)]] + ")"
                        names[file_name] = name
                    
                    extra_textures_raw = json.loads(f.text)
                    
                    # Load all other assets related to the ship (backgrounds, rigging, etc)
                    for ship in extra_textures_raw:
                        if(ship == "all"):
                            continue
                        for skin in extra_textures_raw[ship]["res_list"]:
                            if skin.endswith("_tex"):
                                names[skin.removeprefix("painting/").removesuffix("_tex").lower()] = names[extra_textures_raw[ship]["key"]]

                    self.load_data = names
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
