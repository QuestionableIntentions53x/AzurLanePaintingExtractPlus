import json
import os

import wx

from core.src.frame_classes.design_frame import MyDialogSetting
from core.src.static_classes.image_deal import ImageWork
from core.src.static_classes.static_data import GlobalData
from core.src.structs_classes.setting_structs import SettingHolder, PerSetting
from .help_frame import HelpPageFrame
from .level_setting_frame import LevelSettingFrame


class Setting(MyDialogSetting):

    def __init__(self, parent, setting_info, work_path, names, height_setting,unnamed_value:list):
        super(Setting, self).__init__(parent)
        self.height_setting = height_setting
        self.names = names
        self.frame = parent
        self.setting = setting_info
        self.path = work_path

        self.unamed_list=unnamed_value

        self.data = GlobalData()

        pic, _ = ImageWork.pic_transform(os.path.join(self.path, "core\\assets\\img.png"),
                                         list(self.m_bitmap2.GetSize()))
        bitmap = wx.Bitmap.FromBufferRGBA(pic.width, pic.height, pic.tobytes())
        self.m_bitmap2.SetBitmap(bitmap)

        self.setting_hold = SettingHolder(setting_info)

        self.input_filter_tex = tuple(
            map(lambda v: str(v.pattern).replace("$", "(?: #\\d+)?\\.[Pp][Nn][Gg]$"), self.data.fp_pattern_group))
        self.input_filter_mesh = tuple(
            map(lambda x: str(x.pattern).replace('$', r'-mesh(?: #\d+)?\.[Oo][Bb][Jj]$'), self.data.fp_pattern_group))

    def save_info(self):
        self.setting_hold.get_value()
        self.setting = self.setting_hold.get_dict()

        data = self.data
        self.setting[data.sk_input_filter_tex] = self.input_filter_tex[self.setting[data.sk_input_filter]]
        self.setting[data.sk_input_filter_mesh] = self.input_filter_mesh[self.setting[data.sk_input_filter]]

        with open(os.path.join(self.path, "core\\assets\\setting.json"), 'w')as file:
            json.dump(self.setting, file, indent=4)

    def set_info(self, event):
        data = self.data
        val: PerSetting = self.setting_hold[data.sk_input_filter]
        val.set_link = self.m_choice_inport_filter.SetSelection
        val.get_link = self.m_choice_inport_filter.GetSelection

        val: PerSetting = self.setting_hold[data.sk_output_group]
        val.set_link = self.m_choice_export_division.SetSelection
        val.get_link = self.m_choice_export_division.GetSelection

        val: PerSetting = self.setting_hold[data.sk_use_cn_name]
        val.set_link = self.m_checkBox_ex_cn.SetValue
        val.get_link = self.m_checkBox_ex_cn.GetValue

        val: PerSetting = self.setting_hold[data.sk_open_output_dir]
        val.set_link = self.m_checkBox_open_dir.SetValue
        val.get_link = self.m_checkBox_open_dir.GetValue

        val: PerSetting = self.setting_hold[data.sk_skip_exist]
        val.set_link = self.m_checkBox_skip_exist.SetValue
        val.get_link = self.m_checkBox_skip_exist.GetValue

        val: PerSetting = self.setting_hold[data.sk_finish_exit]
        val.set_link = self.m_checkBox_finish_exit.SetValue
        val.get_link = self.m_checkBox_finish_exit.GetValue

        val: PerSetting = self.setting_hold[data.sk_clear_when_input]
        val.set_link = self.m_checkBox_clear_list.SetValue
        val.get_link = self.m_checkBox_clear_list.GetValue

        val: PerSetting = self.setting_hold[data.sk_make_new_dir]
        val.set_link = self.m_checkBox_new_dir.SetValue
        val.get_link = self.m_checkBox_new_dir.GetValue

        val: PerSetting = self.setting_hold[data.sk_export_all_while_copy]
        val.set_link = self.m_checkBox_ex_copy.SetValue
        val.get_link = self.m_checkBox_ex_copy.GetValue

        val: PerSetting = self.setting_hold[data.sk_ignore_case]
        val.set_link = self.m_checkBox_ignore_case.SetValue
        val.get_link = self.m_checkBox_ignore_case.GetValue

        self.setting_hold.initial_val()

    def height_setting_dialog(self, event):
        dialog = LevelSettingFrame(self, self.height_setting, self.names, self.path,self.unamed_list,self.path)
        dialog.ShowModal()
        self.names = dialog.get_names()
        self.height_setting = dialog.get_setting()

    def guider(self, event):
        dialog = HelpPageFrame(self.path)
        dialog.Show(True)

    def ok_press(self, event):
        self.save_info()
        self.Destroy()

    def cancel_press(self, event):
        self.Destroy()

    def apply_press(self, event):
        self.save_info()

    def get_setting(self):
        return self.setting

    def get_names(self):
        return self.names

    def get_height_setting(self):
        return self.height_setting
