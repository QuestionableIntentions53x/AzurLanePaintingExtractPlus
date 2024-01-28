import json
import os
import queue
from re import S
import shutil
import threading

import wx

from core.src.frame_classes.SpriteSpiltFrame import SpriteSplitFrame
from core.src.frame_classes.atlas_spilt_frame import AtlasSpiltFrame
from core.src.frame_classes.design_frame import MainFrame as Mf
from core.src.frame_classes.face_match_frame import FaceMatchFrame
from core.src.frame_classes.setting_frame import Setting
from core.src.static_classes.file_read import FileFilter
from core.src.static_classes.update_localization import NameLocalization
from core.src.static_classes.image_deal import ImageWork
from core.src.static_classes.search_order import SearchOrder
from core.src.static_classes.static_data import GlobalData
from core.src.structs_classes.drop_order import DropOrder
from core.src.structs_classes.extract_structs import PerWorkList
from core.src.structs_classes.extract_structs import PerInfo
from core.src.thread_classes.extract_thread import WorkThread, WatchDogThread, SideWorkThread
from core.src.thread_classes.quick_view import QuickRestore

from core.src.static_classes.locale import Translator

import gettext
_ = gettext.gettext

class MainFrame(Mf):
    """
    Main window class
    """

    def __init__(self, parent, path=os.getcwd()):
        super(MainFrame, self).__init__(parent)

        # Constant parameter storage class
        self.data = GlobalData()

        # Add icon
        icon = wx.Icon(os.path.join(path, "core\\assets\\sf_icon.ico"))
        self.SetIcon(icon)

        # Shipgirl name file
        self.names = {}
        with open(os.path.join(path, "core\\assets\\names.json"), "r")as file:
            self.names = json.load(file)

        # Settings file
        with open(os.path.join(path, "core\\assets\\setting.json"), 'r')as file:
            self.setting_info: dict = json.load(file)
        with open(os.path.join(path, "core\\assets\\height_setting.json"), 'r')as file:
            self.height_setting: dict = json.load(file)

        # Localization
        self.tl = Translator()
        self.tl.set_locale_from_index(self.setting_info[self.data.sk_locale])
        _ = self.tl.t

        # Initalize main UI
        self.build(self.tl)

        # Set root folder
        self.root = self.m_treeCtrl_info.AddRoot(_("Azur Lane"))

        # Final processing work list
        self.painting_work = PerWorkList(self, mesh_match=self.height_setting[self.data.sk_mash_match],
                                         texture_match=self.height_setting[self.data.sk_texture_match],
                                         is_ignore_case=self.setting_info[self.data.sk_ignore_case])
        
        # UI processing work list
        self.view_work = PerWorkList(self)

        # Find the information of the tree index, pos->[single true, false in the list]; type_is->type [texture, mesh], name->object at the clicked position
        self.is_single, self.type_is, self.name = None, None, None
        self.index = -1

        # Set drag binding
        self.drop = DropOrder(self.painting_work,
                              self.view_work, self, self.get_input_data)
        self.m_treeCtrl_info.SetDropTarget(self.drop)

        # Vertical painting restoration thread
        self.thread_quick = None
        self.thread_main = None
        self.thread_main_groups = []
        self.thread_main_name = (
            "thread-1", "thread-2", "thread-3", "thread-4")
        self.thread_watch_dog = None
        self.thread_side_work = None

        # Thread lock, queue
        self.locker = threading.Lock()
        self.work_queue = queue.Queue()
        self.err_queue = queue.Queue(10)

        # Enter the exit state
        self.enter_exit = False

        # Save path, script path
        self.save_path = ""
        self.work_path = path

        # window (only one)
        self.__dialog = None

        # Update names
        if self.setting_info["automatic_name_update"] == True:
            dialog = NameLocalization(self, self.setting_info)
            do_update, _ = dialog.CheckVersion()
            if do_update:
                dialog.ShowModal()
            else:
                dialog.cancel(None)

        # search, filter
        self.search_type = False
        self.filter_type = False

        # Search data
        self.select_data = None

        self.frame_size = self.Size

        self.pipe = ...

    @staticmethod
    def run(path):
        """
        Run entry function
        :return:
        """
        app = wx.App()
        frame = MainFrame(None, path)

        frame.Show()

        app.MainLoop()

    # Setter, passed as a parameter
    def get_input_data(self, view_work, painting_group):
        self.view_work = view_work
        #self.painting_work = painting_group

    """ COMPONENT MODIFICATION """

    def change_path(self, is_single: bool, type_is: bool, target: PerInfo, index: int):
        """
        Modify the method pointing to the file
        :param index:
        :param is_single: Whether the element in the selected tree is an element outside the list
        :param type_is: selected type (tex, mesh)
        :param target: points to the target method type: PerInfo
        :return: bool
        """
        _ = self.tl.t
        if is_single is None:
            return False
        # When the selected object is a single object, not an item in the list (the tags of other files)
        #The selected one is texture
        if type_is:
            if is_single:
                dialog = wx.SingleChoiceDialog(
                    self, _("Select Texture File"), _("Select file"), target.get_select(type_is))
                if dialog.ShowModal() == wx.ID_OK:
                    index = dialog.GetSelection()
                # Redirect texture files
            try:
                id, data = target.set_tex(index)
                self.m_treeCtrl_info.SetItemText(id, data)
            except:
                return False

        #The selected one is mesh
        else:
            if is_single:
                dialog = wx.SingleChoiceDialog(
                    self, _("Select Mesh File"), _("Select file"), target.get_select(type_is))
                if dialog.ShowModal() == wx.ID_OK:
                    index = dialog.GetSelection()
                # Redirect mesh files
            try:
                id, data = target.set_mesh(index)
                self.m_treeCtrl_info.SetItemText(id, data)
            except:
                return False

        if target.check_restorable():
            self.m_treeCtrl_info.SetItemTextColour(
                target.key, wx.Colour(253, 86, 255))
        else:
            self.m_treeCtrl_info.SetItemTextColour(
                target.key, wx.Colour(255, 255, 255))
        return True

    """ EVENT FUNCTIONS """

    def independent_target(self, target: PerInfo):
        """
        Create a new independent target (create a new independent object that is the same as the target)
        :param target: the target to be created
        :return: None
        """
        _ = self.tl.t

        self.__dialog = wx.TextEntryDialog(parent=None, message='', caption=_("Name of duplicated ship instance"),
                                           value=f"{target.name}-#{target.sub_data}", )

        is_ok = self.__dialog.ShowModal()

        if is_ok == wx.ID_OK:
            name = self.__dialog.GetValue()
            if name in self.painting_work:
                wx.MessageBox(_("The name already exists!"), _("Error"), wx.OK | wx.ICON_ERROR)
                self.independent_target(target)
            else:
                target.independent(name, self.m_treeCtrl_info, self.root)

    def face_match_target(self, target: PerInfo):
        _ = self.tl.t
        if not target.restorable:
            self.m_staticText_info.SetLabel(_("Face change failed! Must be a restoreable object"))
            return
        self.m_staticText_info.SetLabel(_("Started changing face"))
        data = wx.SingleChoiceDialog(self, "", _("Select Accessory Type:"), [
                                     _("Facial expression (680x470)"), _("Ship decoration (1920x1080)")]) #TODO: add custom?
        if wx.ID_OK == data.ShowModal():
            info = data.GetSelection()
            type_is = False
            if info == 0:
                type_is = True
            self.__dialog = FaceMatchFrame(self, target, type_is)
            self.__dialog.ShowModal()

    def atlas_split_target(self, target: PerInfo):
        _ = self.tl.t
        if not os.path.isfile(target.tex_path):
            self.m_staticText_info.SetLabel(_("Cutting failed, there must be an available Texture2D file"))
            return
        else:
            self.m_staticText_info.SetLabel(_("Start changing the head!"))
            self.__dialog = AtlasSpiltFrame(self, target)
            self.__dialog.ShowModal()

    def set_able_target(self, target: PerInfo):
        _ = self.tl.t
        target.transform_able()
        self.m_treeCtrl_info.DeleteChildren(target.tree_ID)
        target.append_item_tree(self.m_treeCtrl_info)
        self.m_staticText_info.SetLabel(
            _("{} has been converted and is now {}").format(target.cn_name, target.force_restorable)) #TODO: Figure out what must-able means

    def remove_target(self, target: PerInfo):
        _ = self.tl.t
        info = wx.MessageBox(
            _("Are you sure you want to remove\n{}").format(target), _("Information"), wx.YES_NO | wx.ICON_INFORMATION)
        if info == wx.YES:
            self.m_treeCtrl_info.Delete(target.tree_ID)
            self.painting_work.remove([target])
            self.view_work.remove([target])
            if self.search_type or self.filter_type:
                self.select_data.remove([target])

    def split_target_only(self, target: PerInfo):
        _ = self.tl.t
        if not target.restorable:
            self.m_staticText_info.SetLabel(_("{} cannot be cut and is a non-reducible object").format(target))
            return
        self.__dialog = wx.DirDialog(
            self, _("Select output folder"), self.work_path, wx.DD_NEW_DIR_BUTTON | wx.DD_DIR_MUST_EXIST)
        if wx.ID_OK == self.__dialog.ShowModal():
            path = self.__dialog.GetPath()
            if self.setting_info[self.data.sk_make_new_dir]:
                path = os.path.join(path, "Azur Lane-Export")
                os.makedirs(path, exist_ok=True)
                ImageWork.split_only_one(target, path)
                self.m_staticText_info.SetLabel(
                    _("{} cutting completed, saved to path: {}").format(target.cn_name, path))

    def sprite_split(self, target: PerInfo):
        _ = self.tl.t
        if not os.path.isfile(target.tex_path):
            self.m_staticText_info.SetLabel(_("{} cannot be cut, at least one Texture2D is required").format(target))
            return
        self.m_staticText_info.SetLabel(_("Start Sprite cutting!"))
        self.__dialog = SpriteSplitFrame(self, target)
        self.__dialog.ShowModal()

    """def change_local(self, target: PerInfo):
        src_name = target.name
        local_name = target.cn_name

        info = f"Change localization: {'Modify old localization' if src_name in self.names.keys() else 'Add localization' } {src_name}"

        d = wx.TextEntryDialog(self, info, "Change localization", local_name)
        if d.ShowModal() == wx.ID_OK:
            data = str(d.GetValue())
            if data == local_name or data == "":
                return
            else:
                target.cn_name = data
                self.names[src_name] = data
                self.refeash(None)"""

    def import_png(self, target: PerInfo):
        _ = self.tl.t
        
        dialog = wx.FileDialog(parent=self, message=_("PNG Path"), defaultDir=target.tex_path[:target.tex_path.rfind('\\')],
                                wildcard="*.png",style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            success, info = ImageWork.deconstruct_tool(target, dialog.GetPath())
            self.m_staticText_info.SetLabel(info)
            
        return

    """ CONTROL FLOW FUNCTIONS """

    def restart(self, size, able, unable):
        """
        Reset restore thread
        :return:
        """
        self.thread_main_groups.clear()
        for name in self.thread_main_name:
            self.thread_main_groups.append(
                WorkThread(name, self.work_queue, self.err_queue, self.locker, self, self.setting_info, self.names,
                           self.save_path, size, self.setting_info[self.data.sk_ignore_case]))
        self.thread_side_work = SideWorkThread(
            unable, self.setting_info, self, self.save_path)
        self.thread_main_groups.append(self.thread_side_work)
        self.thread_watch_dog = WatchDogThread(self.work_queue, self.err_queue, able, self.locker, self,
                                               self.setting_info, len(unable) + size, self.thread_main_groups)

        # self.thread_main = RestoreThread(1, 'restore', self.painting_work.build_able(),
        #                                 self.painting_work.build_unable(), self, self.setting_info,
        #                                 self.names, self.save_path, self.setting_info[self.data.sk_ignore_case])

        self.m_staticText_info.SetLabel(_("Reset restoration progress!"))

        self.m_gauge_state.SetValue(0)

    """ FILE EXPORT FUNCTIONS """

    def export_choice(self):
        """
        Export selections
        :return: none
        """
        _ = self.tl.t
        target = self.name
        self.__dialog = wx.FileDialog(self, _("Save-Azur Lane"), os.getcwd(), f'{target.sanitize_file_name(target.cn_name)}.png', "*.png",
                                      wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_PREVIEW)

        if self.__dialog.ShowModal() == wx.ID_OK:
            self.m_gauge_state.SetValue(0)
            self.save_path = self.__dialog.GetPath()

            target.set_single_path(self.__dialog.GetPath())
            ImageWork.restore_tool(target)

        self.m_gauge_state.SetValue(100)

        if self.setting_info[self.data.sk_finish_exit]:
            self.exit()

    def export_all(self, path, for_work: PerWorkList = None):
        """
        Export all
        :param path:Export target directory
        :param for_work: list structure for export
        :return:
        """
        data = self.data

        if self.setting_info[data.sk_make_new_dir]:
            path += r"\Azur Lane-Export"

        os.makedirs(path, exist_ok=True)
        #Reset progress
        # self.restart()
        self.save_path = path
        self.m_gauge_state.SetValue(0)

        if isinstance(for_work, PerWorkList):
            able = for_work.build_able()
        else:
            able = self.painting_work.build_able()

        # Skip existing processing
        if self.setting_info[data.sk_skip_exist]:
            target_path_list = FileFilter.all_file(path)

            skip = able.build_skip(target_path_list)
            able.remove(skip)

        # Start thread
        # self.thread_main.add_save_path(self.save_path)
        # self.thread_main.update_value(able, for_work.build_unable())
        # if self.thread_main.is_alive():
        #    self.thread_main.stop_(True)
        #    while self.thread_main.is_alive():
        #        time.sleep(1)
        #    self.thread_main.start()
        # else:
        #    self.thread_main.start()
        self.restart(len(able), able, for_work.build_unable())
        self.thread_watch_dog.start()
        # self.thread_side_work.start()
        for thread in self.thread_main_groups:
            thread.start()

        # Test multiple processes
        # apply_work(able, self.save_path, self, self.data)

    def copy_file(self):
        """
        Export the non-restorable part (copy)
        :return: none
        """
        _ = self.tl.t
        data = self.data
        self.__dialog = wx.DirDialog(self, _("Save"), os.getcwd(),
                                     style=wx.DD_DIR_MUST_EXIST | wx.DD_CHANGE_DIR | wx.DD_NEW_DIR_BUTTON
                                           | wx.DD_DEFAULT_STYLE)
        if self.__dialog.ShowModal() == wx.ID_OK:
            unable = self.painting_work.build_unable()
            path = self.__dialog.GetPath()
            if self.setting_info[data.sk_output_group] == data.feg_by_type:
                path += "\\copy"
            num = 0
            self.m_gauge_state.SetValue(0)
            for name in unable:
                num += 1
                name.add_save(path)
                shutil.copyfile(name.tex_path, name.save_path)

                self.m_gauge_state.SetValue(round(100 * (num / len(unable))))

        if self.setting_info[data.sk_open_output_dir]:
            os.system(r'start "%s"' % self.save_path)
        if self.setting_info[data.sk_finish_exit]:
            self.exit()

    """ CALLBACK FUNCTIONS """

    def refresh_PerInfo_tree(self):
        self.m_treeCtrl_info.DeleteAllItems()
        for asset in self.view_work:
            asset.append_to_tree(self.m_treeCtrl_info, self.root)

    def on_info_select(self, event: wx.TreeEvent):
        _ = self.tl.t
        """
        tree element selection response method
        :param event: event
        :return:
        """
        # If it is not in the exit state (the tree will behave strangely when exiting)
        if not self.enter_exit:

            # Select modifier key to reset
            self.m_bpButton_change.Enable(False)
            self.m_treeCtrl_info.Unselect()
            # Get the id of the selected element
            val = event.GetItem()

            # If no search or filter is used, use the default storage class
            # Find the id, whether it is a title tag
            if not self.search_type and not self.filter_type:
                is_ok, name = self.painting_work.find_by_id(val)
            else:
                is_ok, name = self.view_work.find_by_id(val)

            # If yes, show preview image
            if is_ok:
                self.m_staticText_info.SetLabel(_("Choose:{}").format(name.cn_name))
                
                self.select_data = self.name = name
                self.thread_quick = QuickRestore(name, self)
                self.thread_quick.start()

            # Find tex or mesh path handle or trigger button
            else:
                # Find the id from each element
                if not self.search_type and not self.filter_type:
                    is_ok, pos, type_is, index, name = self.painting_work.find_in_each(
                        val)
                else:
                    is_ok, pos, type_is, index, name = self.view_work.find_in_each(
                        val)
                
                # found it
                if is_ok:
                    # Available modifications
                    self.m_bpButton_change.Enable(True)
                    self.is_single, self.type_is, self.name = pos, type_is, name
                    self.index = index
                    # Generate objects for display
                    is_able, value = name.build_sub(pos, type_is, index)
                    if is_able:
                        # The texture file that generates the object is a normal file
                        self.thread_quick = QuickRestore(value, self)
                        self.thread_quick.start()
                        self.select_data = value
                        is_able = _("Previewable")
                    else:
                        is_able = _("Not previewable")

                    if pos:
                        pos = _("Single type")
                    else:
                        pos = _("List")
                    if type_is:
                        type_is = _("Texture file")
                    else:
                        type_is = _("Mesh file")

                    self.m_staticText_info.SetLabel(
                        _("Select: {}{} in {}: {}, {}").format(pos, type_is, name.cn_name, self.m_treeCtrl_info.GetItemText(val), is_able))

                # Not found, search for function buttons
                else:
                    if not self.search_type and not self.filter_type:
                        is_ok, type_is, target = self.painting_work.find_action(
                            val)
                    else:
                        is_ok, type_is, target = self.view_work.find_action(
                            val)
                    
                    if is_ok:
                        """if type_is == self.data.at_independent:
                            self.independent_target(target)"""
                        if type_is == self.data.at_face_match:
                            self.face_match_target(target)
                        if type_is == self.data.at_atlas_split:
                            self.atlas_split_target(target)
                        """if type_is == self.data.at_set_able:
                            self.set_able_target(target)"""
                        if type_is == self.data.at_remove_item:
                            self.remove_target(target)
                        if type_is == self.data.at_split_only:
                            self.split_target_only(target)
                        """if type_is == self.data.at_sprite_split:
                            self.sprite_split(target)"""
                        """if type_is == self.data.at_change_local:
                            self.change_local(target)"""
                        if type_is == self.data.at_import_sprite:
                            self.import_png(target)
                        if type_is == self.data.at_tex_path:
                            self.is_single, self.type_is = True, True
                            self.choice_file(None)
                        if type_is == self.data.at_mesh_path:
                            self.is_single, self.type_is = True, False
                            self.choice_file(None)

    def choice_file(self, event):
        #Select the corresponding file
        _ = self.tl.t
        is_ok = self.change_path(
            self.is_single, self.type_is, self.name, self.index)
        if not is_ok:
            wx.MessageBox(_("No data!"), _("Error"), wx.OK | wx.ICON_ERROR)
            return

        self.thread_quick = QuickRestore(self.name, self)
        self.thread_quick.run()

    def work(self, event):
        """
        Export file tool
        :param event:
        :return:
        """
        _ = self.tl.t
        data = self.data
        show = [_("Export restored assets"), _("Export unrestorable assets"), _("Export selected asset"), _("Export all")]
        #Add unavailable suffix
        if len(self.painting_work.build_able()) == 0:
            show[data.et_all] += _("(unavailable)")
        if len(self.painting_work.build_unable()) == 0:
            show[data.et_copy_only] += _("(unavailable)")
        if self.name is None:
            show[data.et_select] += _("(unavailable)")
        if self.filter_type or self.search_type:
            if self.view_work.__len__() == 0:
                show[data.et_list_item] += _("(unavailable)")
        else:
            if len(self.painting_work) == 0:
                show[data.et_list_item] += _("(unavailable)")

        self.__dialog = wx.SingleChoiceDialog(self, "", _("Choose export type"), show)

        if self.__dialog.ShowModal() == wx.ID_OK:
            index = self.__dialog.GetSelection()
            #Export all
            if index == data.et_all:
                # If no list is available, exit export
                if len(self.painting_work.build_able()) == 0:
                    wx.MessageBox(_("Not available!"), _("Error"))
                    return
                # Start exporting target folder selection
                title = _("Save-Azur Lane")
                address = os.getcwd()
                dialog = wx.DirDialog(
                    self, title, address, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

                if dialog.ShowModal() == wx.ID_OK:
                    temp = dialog.GetPath()
                    if self.painting_work.build_able().__len__() > 0:
                        # Start exporting
                        self.export_all(temp, self.painting_work)
            #Copy cannot be restored
            if index == data.et_copy_only:
                if len(self.painting_work.build_unable()) == 0:
                    wx.MessageBox(_("Not available!"), _("Error"))
                    return
                self.copy_file()
            #Export selections
            if index == data.et_select:
                if self.name is None:
                    wx.MessageBox(_("Not available!"), _("Error"))
                    return
                self.export_choice()

            #Export the current list item
            if index == data.et_list_item:
                if self.filter_type or self.search_type:
                    if self.view_work.__len__() == 0:
                        wx.MessageBox(_("Not available!"), _("Error"))
                        return
                else:
                    if len(self.painting_work) == 0:
                        wx.MessageBox(_("Not available!"), _("Error"))
                        return
                title = _("Save-Azur Lane")
                address = os.getcwd()
                dialog = wx.DirDialog(
                    self, title, address, style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
                if dialog.ShowModal() == wx.ID_OK:
                    temp = dialog.GetPath()
                    if self.view_work.build_able().__len__() > 0:
                        self.export_all(temp, self.view_work)

    def filter_work(self, event):
        """
        filter behavior
        :param event:
        :return:
        """
        index = event.GetSelection()
        value = self.data.fp_pattern_group[index]

        # If the filter selects all, reset to show all
        if index == self.data.tf_all:
            self.filter_type = False

            self.enter_exit = True
            self.m_treeCtrl_info.DeleteChildren(self.root)
            self.painting_work.show_in_tree(self.m_treeCtrl_info, self.root)
            self.enter_exit = False
        else:
            # Displayed differently depending on status
            if self.search_type:
                self.view_work = self.view_work.build_from_pattern(value)
            else:
                self.view_work = self.painting_work.build_from_pattern(value)

            self.filter_type = True

            self.enter_exit = True
            self.m_treeCtrl_info.DeleteChildren(self.root)
            self.view_work.show_in_tree(self.m_treeCtrl_info, self.root)
            self.enter_exit = False

    def search(self, event):
        """
        Finder behavior
        :param event:
        :return:
        """
        # Get search keywords
        if event is None:
            value = self.m_searchCtrl1.GetValue()
        else:
            value = event.GetString()

        # If the search keyword is not empty
        if value != '':

            if not self.filter_type:
                indexes = SearchOrder.find(
                    value, self.painting_work.build_search())
                self.view_work = self.painting_work.build_from_indexes(indexes)
            else:
                indexes = SearchOrder.find(
                    value, self.view_work.build_search())
                self.view_work = self.view_work.build_from_indexes(indexes)

            self.search_type = True

            self.enter_exit = True
            self.m_treeCtrl_info.DeleteChildren(self.root)
            self.view_work.show_in_tree(self.m_treeCtrl_info, self.root)
            self.enter_exit = False
       # If search is empty, reset the list
        else:
            self.search_type = False

            self.enter_exit = True
            self.m_treeCtrl_info.DeleteChildren(self.root)
            self.painting_work.show_in_tree(self.m_treeCtrl_info, self.root)
            self.enter_exit = False

    def setting(self, event):
        """
        Open settings
        :param event:
        :return:
        """
        unamed_list = list(map(lambda x: x.name, filter(
            lambda x: not x.has_cn, self.painting_work)))

        self.__dialog = Setting(self, self.setting_info,
                                self.work_path, self.names, self.height_setting, unamed_list)

        self.__dialog.ShowModal()
        # reset settings
        self.setting_info = self.__dialog.get_setting()
        self.names = self.__dialog.get_names()

    def refeash(self, event):
        list(
            map(lambda x: x.update_name(self.names), self.painting_work))
        list(
            map(lambda x: x.update_name(self.names), self.view_work))

        self.enter_exit = True
        self.m_treeCtrl_info.DeleteChildren(self.root)
        if not self.search_type:
            self.painting_work.show_in_tree(self.m_treeCtrl_info, self.root)
        else:
            self.view_work.show_in_tree(self.m_treeCtrl_info, self.root)
        self.enter_exit = False

    def resize(self, event):
        """
        Reset window size (useless)
        :param event:
        :return:
        """
        if self.frame_size != self.GetSize():
            self.thread_quick = QuickRestore(self.select_data, self)
            self.thread_quick.start()

    def exit(self, event=None):
        # quit
        #        self.thread_watch_dog.
        if self.thread_watch_dog is not None:
            self.thread_watch_dog.stop()
        # self.thread_watch_dog.join()
        self.enter_exit = True
        self.m_treeCtrl_info.DeleteChildren(self.root)
        self.m_treeCtrl_info.Destroy()
        self.Destroy()

        with open(os.path.join(self.work_path, "core\\assets\\names.json"), "w")as file:
            json.dump(self.names, file, indent=4)
        # sys.exit()
