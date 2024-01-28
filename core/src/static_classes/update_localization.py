import json
import os

import requests
import wx

import gettext
_ = gettext.gettext

class NameUpdaterFrame ( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "Ship Name Updater", pos = wx.DefaultPosition, size = wx.Size( 512,256 ), style = wx.DEFAULT_DIALOG_STYLE )
        self.build(parent.tl)

    def __del__( self ):
        pass

    def build(self, translation):
        _ = translation.t

        self.SetTitle(_("Ship Name Updater"))

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        # Main

        bSizer_main = wx.BoxSizer( wx.VERTICAL )
        
        # = Side Menu

        bSizer_container = wx.BoxSizer( wx.HORIZONTAL )
        
        # == Name Tree

        bSizer_name_tree = wx.BoxSizer( wx.VERTICAL )

        self.m_treeCtrl_info = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_TWIST_BUTTONS )
        bSizer_name_tree.Add( self.m_treeCtrl_info, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_gauge_state = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge_state.SetValue( 0 )
        bSizer_name_tree.Add( self.m_gauge_state, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer_container.Add( bSizer_name_tree, 1, wx.EXPAND, 5 )

        self.m_staticline22 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
        bSizer_container.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )

        # == Side Menu Buttons

        bSizer_side_menu_buttons = wx.BoxSizer( wx.VERTICAL )

        self.m_button_apply_all = wx.Button( self, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer_side_menu_buttons.Add( self.m_button_apply_all, 0, wx.ALL, 5 )

        self.m_button_cancel = wx.Button( self, wx.ID_ANY, _("Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer_side_menu_buttons.Add( self.m_button_cancel, 0, wx.ALL, 5 )

        self.m_button_disable_updates = wx.Button( self, wx.ID_ANY, _("Disable Updates"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer_side_menu_buttons.Add( self.m_button_disable_updates, 0, wx.ALL, 5 )

        bSizer_container.Add( bSizer_side_menu_buttons, 0, wx.EXPAND, 5 )

        bSizer_main.Add( bSizer_container, 1, wx.EXPAND, 5 )

        self.m_staticline24 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer_main.Add( self.m_staticline24, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText_info = wx.StaticText( self, wx.ID_ANY, _("Loading..."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_info.Wrap( -1 )

        bSizer_main.Add( self.m_staticText_info, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer_main )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_UPDATE_UI, self.OnUpdateWindow )
        self.m_button_apply_all.Bind( wx.EVT_BUTTON, self.apply_all )
        self.m_button_cancel.Bind( wx.EVT_BUTTON, self.cancel )
        self.m_button_disable_updates.Bind( wx.EVT_BUTTON, self.disable )

    # Virtual event handlers, overide them in your derived class
    def OnUpdateWindow( self, event ):
        event.Skip()

    def apply_all( self, event ):
        event.Skip()

    def disable( self, event ):
        event.Skip()

    def cancel( self, event ):
        event.Skip()


class NameLocalization ( NameUpdaterFrame ):
    def __init__(self, parent, settings: map, check_version: bool = True):
        super(NameLocalization, self).__init__(parent)
        _ = parent.tl.t
        self.parent = parent
        self.settings = settings
        self.path = os.getcwd()

        self.check_version = check_version
        self.version = str(settings["locale_name_version"])
        self.source = "https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/{}/ShareCfg/ship_skin_template.json"
        self.namecode_source = "https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/{}/ShareCfg/name_code.json"
        self.skin_source = "https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/{}/ShareCfg/painting_filte_map.json"
        self.version_source = "https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/versions/{}.txt"

        self.source_format_list = ["EN", "CN", "KR", "JP", "TW"]
        self.source_language_map = dict({"en": "EN", "zh": "CN", "ko": "KR", "ja": "JP", "zh-tw": "TW"})
        self.default = "EN"

        self.tex_suffix = dict({
            "n": _("Transparent"),
            "wjz": _("Transparent"),
            "h": _("Oath"),
            "bj": _("Rigging"),
            "jz": _("Rigging"),
            "mid": _("Rigging"),
            "middle": _("Rigging"),
            "fornt": _("Rigging"),
            "front": _("Rigging"),
            "tx": _("Rigging"),
            "bg": _("Rigging"),
            "f": _("Rigging")
        })

        self.tex_suffix_exclude = dict({
            "": "",
            "g": _("Retrofit"),
            "rw": _("Default")
        })

        self.names = dict()
        self.updating = -100
        self.out_message = str("")
        self.progress = 0.0
        
        self.root = self.m_treeCtrl_info.AddRoot("")
        self.exist_count = 0
        self.existing_root = self.m_treeCtrl_info.AppendItem(self.root, _("Update Existing Localization Resources ({})").format(self.exist_count))
        self.new_count = 0
        self.new_root = self.m_treeCtrl_info.AppendItem(self.root, _("New Localization Resources ({})").format(self.new_count))

    def CheckVersion(self):
        _ = self.parent.tl.t
        lang = self.source_language_map.get(self.parent.tl.selected_language, self.default)
        try:
            with requests.get(self.version_source.format(lang), timeout=10) as version_raw:
                if version_raw.status_code != 200:
                    return bool(False), _("Error ({}) when connecting to [{}]").format(version_raw.status_code, self.version_source.format(lang))
                if self.version != lang + "." + version_raw.text:
                    return bool(True), str(lang + "." + version_raw.text)
                return bool(False), str(self.version + " = " + lang + "." + version_raw.text)
        except Exception as e:
            return bool(False), e.__str__()
    
    def AppendShipsFromPath(self, path, namecode_path, names):
        _ = self.parent.tl.t
        with requests.get(path, timeout=10) as source_raw, requests.get(namecode_path, timeout=10) as namecode_raw:

            if source_raw.status_code != 200:
                return _("Error ({}) when connecting to [{}]").format(source_raw.status_code, path)
            
            if namecode_raw.status_code != 200:
                return _("Error ({}) when connecting to [{}]").format(namecode_raw.status_code, namecode_path)
            
            source_json = json.loads(source_raw.text)
            namecode_json = json.loads(namecode_raw.text)
            
            try:
                # Load base ship varieties
                for ship in source_json:
                    file_name = str(source_json[ship]["painting"].lower())

                    # If a translation has already been found durring this check, skip (only for exclusive skin/ship checks)
                    if file_name in names:
                        continue

                    # Translated name stored in the "name" value
                    name = source_json[ship]["name"]

                    # Ship names sometimes contain (namecode:###) which reference a separate namecode file
                    while name.find("namecode") != -1:
                        start = name.find("{")
                        end = name.find("}")
                        begin = name[:start]
                        index = name[name.find(":", start) + 1:end]
                        mid = namecode_json[index]["name"]
                        end = "" if len(name) == end else name[end + 1:]
                        name = begin + mid + end
                    
                    # Add the ship's name after the skin's name (exclude retrofits since it already has their name)
                    if name.find("(Retrofit)") == -1:
                        if file_name[:file_name.find("_")] in names:
                            name += " (" + names[file_name[:file_name.find("_")]].removesuffix(" ") + ")"
                        elif file_name[:file_name.find("_", file_name.find("_") + 1)] in names:
                            name += " (" + names[file_name[:file_name.find("_", file_name.find("_") + 1)]].removesuffix(" ") + ")"
                    
                    if name == "" or file_name == "":
                        continue

                    names[file_name] = name
            except Exception as e:
                return _("Error ({}) when parsing data").format(e.__str__())
    
    def AppendExtraTexFromPath(self, path, names):
        _ = self.parent.tl.t
        with requests.get(path, timeout=10) as extra_textures_raw:

            if extra_textures_raw.status_code != 200:
                return _("Error ({}) when connecting to [{}]").format(extra_textures_raw.status_code, path)
            
            extra_textures_json = json.loads(extra_textures_raw.text)
            
            # Load all other assets related to the ship (backgrounds, rigging, etc)
            for ship in extra_textures_json:
                if(ship == "all"):
                    continue
                for skin in extra_textures_json[ship]["res_list"]:
                    if skin.endswith("_tex"):
                        # File name format: painting/[shipname][tags][_tex]
                        file_name = skin.removeprefix("painting/").removesuffix("_tex").lower()

                        # If a translation has already been found durring this check, skip (only for exclusive skin/ship checks)
                        if file_name in names:
                            continue
                        
                        # Split extra data and get rid of name
                        extra = skin.removeprefix("painting/").removesuffix("_tex").split("_")
                        extra[0] = ""
                        
                        extra_str = " ["
                        for data in extra:
                            # Find it in regular list
                            if data in self.tex_suffix:
                                if not (self.tex_suffix[data] in extra_str):
                                    extra_str += self.tex_suffix[data] + "-"
                                continue
                            # Exclude uncessesary ones
                            if data in self.tex_suffix_exclude:
                                continue
                            # Exclude skin numbers
                            if data.isnumeric():
                                continue
                            # Check if it has numbers on either side (bad code, I know)
                            remainder = 999
                            match = "Other"
                            for suffix in self.tex_suffix:
                                if suffix in data and len(suffix) - len(data) < remainder:
                                    remainder = len(data) - len(suffix)
                                    match = self.tex_suffix[suffix]
                            if not (match in extra_str):
                                if match == _("Other"):
                                    extra_str += match + "-"
                                elif data[0].isnumeric() or data[len(data) - 1].isnumeric():
                                    extra_str += match + "-"
                                elif not (_("Other") in extra_str):
                                    extra_str += _("Other") + "-"
                        
                        # If no extra was found, zero it out
                        extra_str = extra_str.removesuffix("-") + "]"
                        if extra_str == " []":
                            extra_str = ""
                        
                        # If it contains the "rw" tag, that means that this is the ship itself and the base file with no tags is background
                        # Doesn't make much sense, but that's the way it is...
                        if "rw" in extra and extra_str == "" and self.names[extra_textures_json[ship]["key"]].find(" [{}]".format(_("Rigging"))) == -1:
                            self.names[extra_textures_json[ship]["key"]] = self.names[extra_textures_json[ship]["key"]] + " [{}]".format(_("Rigging"))

                        # Set the name, trim extra rigging tag if need be
                        name = self.names[extra_textures_json[ship]["key"]].removesuffix(" [{}]".format(_("Rigging"))) + extra_str

                        # Sanity check
                        if name == "" or file_name == "":
                            continue
                        
                        names[file_name] = name

    def UpdateFromSource(self):
        _ = self.parent.tl.t
        max_progress = len(self.source_format_list) * 2.0
        lang = self.source_language_map.get(self.parent.tl.selected_language, self.default)
        try:
            if self.updating == 0:
                if not self.check_version:
                    self.progress += 1
                    self.m_gauge_state.SetValue(int(100.0 * (self.progress / max_progress)))
                    self.updating += 1
                    return False, None

                self.m_staticText_info.SetLabel(_("Checking version..."))
                do_update, self.out_message = self.CheckVersion()
                
                if not do_update:
                    return False, self.out_message
                
                self.m_staticText_info.SetLabel(_("Begin updating from {} to {}").format(self.version, self.out_message))
                self.version = self.out_message
                self.out_message = str("")
                self.progress += 1
                self.m_gauge_state.SetValue(int(100.0 * (self.progress / max_progress)))
                self.updating += 1
                return False, None
            elif self.updating == 1:
                print(_("Fetching {} ships from {}...").format(lang, self.source.format(lang)))
                result = self.AppendShipsFromPath(self.source.format(lang), self.namecode_source.format(lang), self.names)
                if result != None:
                    self.out_message += result + "\n"
                self.progress += 1
                
                print(_("Fetching {} textures from {}...").format(lang, self.skin_source.format(lang)))
                result = self.AppendExtraTexFromPath(self.skin_source.format(lang), self.names)
                if result != None:
                    self.out_message += result + "\n"
                self.progress += 1
                self.m_gauge_state.SetValue(int(100.0 * (self.progress / max_progress)))
                self.updating += 1
                return False, None
            elif self.updating >= 2 and self.updating < 2 + len(self.source_format_list):
                # Append exclusive ships and skins
                key = self.source_format_list[self.updating - 2]
                if key == lang:
                    self.updating += 1
                    return False, None
                
                print(_("Fetching {} ships from {}...").format(key, self.source.format(key)))
                result = self.AppendShipsFromPath(self.source.format(key), self.namecode_source.format(key), self.names)
                if result != None:
                    self.out_message += result + "\n"
                self.progress += 1
                self.m_gauge_state.SetValue(int(100.0 * (self.progress / max_progress)))
                
                print(_("Fetching {} textures from {}...").format(key, self.skin_source.format(key)))
                result = self.AppendExtraTexFromPath(self.skin_source.format(key), self.names)
                if result != None:
                    self.out_message += result + "\n"
                self.progress += 1
                self.m_gauge_state.SetValue(int(100.0 * (self.progress / max_progress)))
                self.updating += 1
                return False, None
            else:
                if self.out_message == "":
                    self.out_message = None
                return True, self.out_message
        except Exception as e:
            self.m_staticText_info.SetLabel(_("Critical ship name update failure:{}").format(e.__str__()))
            return False, _("Critical ship name update failure:{}").format("\n" + e.__str__())
    
    def UpdateTree(self):
        _ = self.parent.tl.t
        for tex, name in self.names.items():
            if tex in self.parent.names:
                if name != self.parent.names[tex]:
                    self.AppendToTree(0, name, self.parent.names[tex], tex)
            else:
                self.AppendToTree(1, name, "", tex)
        self.m_treeCtrl_info.SetItemText(self.existing_root, _("Update Existing Localization Resources ({})").format(self.exist_count))
        self.m_treeCtrl_info.SetItemText(self.new_root, _("New Localization Resources ({})").format(self.new_count))

    def AppendToTree(self, type: int, new: str, old: str, file_name: str):
        _ = self.parent.tl.t
        if type == 0:
            self.exist_count += 1
        else:
            self.new_count += 1
        item_root = self.m_treeCtrl_info.AppendItem(self.existing_root if type == 0 else self.new_root, file_name + "->" + new)
        if type == 0: self.m_treeCtrl_info.AppendItem(item_root, _("Original Name: \"{}\"").format(old))
        self.m_treeCtrl_info.AppendItem(item_root, _("Updated Name:  \"{}\"").format(new))

    def OnUpdateWindow(self, event):
        _ = self.parent.tl.t
        # I had to delay the begining of the process in order for the progress bar to appear
        if self.updating < 0:
            self.updating += 1
        # Does it in steps so the progress bar updates in real time
        elif self.updating >= 0 and self.updating < 100:
            success, message = self.UpdateFromSource()
            if success:
                self.updating = 100
                self.UpdateTree()
                self.m_staticText_info.SetLabel(_("Done!"))
            elif message != None:
                self.updating = 200
                wx.MessageDialog(self, message, _("Message") if success else _("Error"), wx.OK).ShowModal()
                self.cancel()
        return

    def ExportNames(self):
        _ = self.parent.tl.t
        if self.new_count > 0 or self.exist_count > 0:
            self.m_staticText_info.SetLabel(_("Saving data..."))
            with open(os.path.join(self.path, "core\\assets\\names.json"), "w") as file:
                json.dump(self.names, file, indent=4)
        self.Destroy()

    def ExportSettings(self):
        with open(os.path.join(self.path, "core\\assets\\setting.json"), 'w') as file:
            json.dump(self.settings, file, indent=4)

    def apply_all( self, event ):
        self.parent.names = self.names
        self.ExportNames()
        self.settings['locale_name_version'] = self.version
        self.ExportSettings()
        self.Destroy()
    
    def disable( self, event ):
        self.settings['automatic_name_update'] = False
        self.ExportSettings()
        self.Destroy()

    def cancel( self, event ):
        self.Destroy()
    