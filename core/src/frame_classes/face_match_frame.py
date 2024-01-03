# -*- coding: utf-8 -*-
# @Author: FrozneString
# @Date:   2020-08-13 21:12:26
# @Last Modified by:   FrozneString
# @Last Modified time: 2020-08-13 21:12:26
import os
import re
from threading import Thread

import numpy
import wx
from PIL import Image, ImageChops

from core.src.static_classes.image_deal import ImageWork
from core.src.structs_classes.drop_order import FaceDragOrder
from core.src.structs_classes.extract_structs import PerInfo
from core.src.thread_classes.quick_view import QuickRestore
from .design_frame import MyDialogAddFace


class FaceMatchFrame(MyDialogAddFace):
    def __init__(self, parent, target: PerInfo, type_is=True):
        super(FaceMatchFrame, self).__init__(parent)
        if not type_is:
            self.SetSize(1920, 1080)
        # Target object and imported expressions
        self.type_is = type_is
        self.target = target
        self.input_values = {}
        self.view_list = []
        self.is_all_only = True

        # Generate target portrait
        self.target_img = ImageWork.az_paint_restore(target.mesh_path, target.tex_path,
                                                     not target.get_is_able_work() and target.must_able)
        self.target_size = self.target_img.size
        # Target expression
        self.target_face = Image.Image()
        # Main image display area size
        self.main_view_w, self.main_view_h = list(self.m_bitmap_main_view.GetSize())
        # Background canvas
        self._bg_size = self.target_size
        self.bg_paint = Image.new("RGBA", self.bg_size, (0, 0, 0, 255))
        # Portrait position on the background canvas
        self.target_paint_x = 0
        self.target_paint_y = 0
        # Background canvas size extension
        self._top_extend = 0
        self._left_extend = 0
        self._right_extend = 0
        self._button_extend = 0
        # Expression coordinates
        self._pos_x = 0
        self._pos_y = 0
        # Relative display area coordinates
        self.pos_x_a = 0
        self.pos_y_a = 0
        # Coordinates of the upper left corner of the canvas display area
        self._target_x = 0
        self._target_y = 0
        # Expression selection
        self.select_index = -1
        self.select_count = 0
        # Expression import
        self.drop_order = FaceDragOrder(self, self.callback,self.type_is)
        self.m_listBox_import_face.SetDropTarget(self.drop_order)
        # Preview image generator
        self.view_work = ...
        # Step
        self.step = 1
        self.save_path = ""

        self.is_alpha_paste = False

        self.m_bitmap_main_view.SetDoubleBuffered(True)

    @staticmethod
    def paste_face(target: Image.Image, face: Image.Image, pos: tuple):
        """
        Transparently blend background and target
        :param target: Blend background
        :param face: Blend target
        :param pos: Blend target drawing coordinates
        :return: None
        """
        target_bg = target.crop([pos[0], pos[1], pos[0] + face.width, pos[1] + face.height])
        alpha = face.getchannel("A")

        # Alpha processing
        alpha_f = alpha
        alpha_g = target_bg.getchannel("A")
        a_f = ImageChops.lighter(alpha_f, alpha_g)

        al = numpy.array(alpha, dtype=numpy.float)

        scale = al / 255

        face_a = numpy.array(face)
        bg_a = numpy.array(target_bg)
        alpha_data = numpy.array(a_f)

        bg_a[:, :, 2] = bg_a[:, :, 2] * (1 - scale)
        bg_a[:, :, 1] = bg_a[:, :, 1] * (1 - scale)
        bg_a[:, :, 0] = bg_a[:, :, 0] * (1 - scale)

        face_a[:, :, 0] = face_a[:, :, 0] * scale
        face_a[:, :, 1] = face_a[:, :, 1] * scale
        face_a[:, :, 2] = face_a[:, :, 2] * scale

        f_target = bg_a + face_a
        f_target[:, :, 3] = alpha_data

        face_e = Image.fromarray(f_target)

        target.paste(face_e, pos)

    # Background extension processing
    @property
    def bg_size(self):
        return self._bg_size

    @bg_size.setter
    def bg_size(self, value):
        if len(value) == 2:
            # Update background canvas size, redraw background image and face image
            self._bg_size = value
            print(value)
            self.paste_target_face()

    # Face drawing coordinates processing
    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_x.setter
    def pos_x(self, value):
        # Force escape to int
        value = int(value)
        # If the x coordinate point of the face drawing is less than 0, extend the canvas to the left by the corresponding pixels, and then return the x coordinate to zero
        if value < 0:
            self.left_extend += -value
            value=0
            self.m_staticText_info.SetLabel(f"Canvas expands {self.left_extend} pixels to the left")

        # If the x coordinate point of the face drawing + the width of the target face is greater than the total width of the current canvas, extend the canvas to the right, and the x value remains unchanged
        elif value + self.target_face.width - self.bg_size[0] > 0:
            self.right_extend += (value + self.target_face.width) - self.bg_size[0]

            self.m_staticText_info.SetLabel(f"Canvas extends {self.right_extend} pixels to the right")
        
        self._pos_x = value
        self.add_face()

    @pos_y.setter
    def pos_y(self, value):
        # Force escape to int
        value = int(value)
        # If the y coordinate point of the face drawing is less than 0, extend the canvas upward by the corresponding pixels, and then return the y coordinate to zero.
        if value < 0:
            self.top_extend += -value
            value=0
            self.m_staticText_info.SetLabel(f"Canvas extends upward by {self.top_extend} pixels")

        # If the face drawing y coordinate + the height of the target face is greater than the total height of the current canvas, the canvas will extend downward and the y value will remain unchanged.
        elif value + self.target_face.height - self.bg_size[1] > 0:
            self.button_extend = value + self.target_face.height - self.bg_size[1]
            self.m_staticText_info.SetLabel(f"Canvas extends downward by {self.button_extend} pixels")

        self._pos_y = value
        self.add_face()

    # Canvas coordinate processing
    @property
    def target_x(self):
        return str(self._target_x)

    @target_x.setter
    def target_x(self, value):
        if value < 0:
            value = 0
        if value + self.main_view_w > self.bg_size[0]:
            value = self.bg_size[0] - self.main_view_w
        self._target_x = value
        self.paint_move(self._target_x, self._target_y)

    @property
    def target_y(self):
        return str(self._target_y)

    @target_y.setter
    def target_y(self, value):
        if value < 0:
            value = 0
        if value + self.main_view_h > self.bg_size[1]:
            value = self.bg_size[1] - self.main_view_h
        self._target_y = value
        # self.pos_y += value - self.main_view_h
        self.paint_move(self._target_x, self._target_y)

    # Canvas extension processing
    @property
    def top_extend(self):
        return self._top_extend

    @property
    def left_extend(self):
        return self._left_extend

    @property
    def right_extend(self):
        return self._right_extend

    @property
    def button_extend(self):
        return self._button_extend

    @top_extend.setter
    def top_extend(self, value):
        self.target_paint_y = value
        self.bg_size = (self.target_size[0] + self.left_extend + self.right_extend,
                        self.target_size[1] + value + self.button_extend)
        self._top_extend = value

    @left_extend.setter
    def left_extend(self, value):
        self.target_paint_x = value
        self.bg_size = (self.target_size[0] + value + self.right_extend, self.target_size[1] +
                        self.top_extend + self.button_extend)
        self._left_extend = value

    @right_extend.setter
    def right_extend(self, value):
        self.bg_size = (self.target_size[0] + value + self.left_extend, self.target_size[1] +
                        self.top_extend + self.button_extend)
        self._right_extend = value

    @button_extend.setter
    def button_extend(self, value):
        self.bg_size = (self.target_size[0] + self.left_extend + self.right_extend,
                        self.target_size[1] + value + self.top_extend)
        self._button_extend = value

    def callback(self, values, is_all_only):
        self.input_values = values
        self.view_list = list(values.keys())
        self.m_listBox_import_face.Clear()
        self.m_listBox_import_face.Set(self.view_list)
        self.is_all_only = is_all_only

        if self.view_list:
            self.m_panel7.Enable(True)

    def paste_target_face(self):
        self.bg_paint = Image.new("RGBA", self.bg_size, (0, 0, 0, 0))
        self.bg_paint.paste(self.target_img, (self.target_paint_x, self.target_paint_y))
        if self.is_alpha_paste:
            FaceMatchFrame.paste_face(self.bg_paint, self.target_face, (self.pos_x, self.pos_y))
        else:
            self.bg_paint.paste(self.target_face, (self.pos_x, self.pos_y), 0)

    def paint_move(self, target_x, target_y):

        pic = self.bg_paint.crop((target_x, target_y, self.main_view_w + target_x, self.main_view_h + target_y))

        temp = wx.Bitmap.FromBufferRGBA(pic.width, pic.height, pic.tobytes())
        self.m_bitmap_main_view.ClearBackground()
        self.m_bitmap_main_view.SetBitmap(temp)

    def add_face(self):
        self.paste_target_face()
        self.paint_move(self._target_x, self._target_y)

    def export_all(self):
        bg_size = self.bg_size
        pos = (self.pos_x, self.pos_y)
        target_pos = (self.target_paint_x, self.target_paint_y)
        face_size = self.target_face.size
        save_path = self.save_path
        name = self.target.cn_name
        target_img = self.target_img

        os.makedirs(save_path, exist_ok=True)

        for key, values in self.input_values.items():
            count = 0
            for value in values:
                count += 1
                temp = Image.open(value)
                if temp.size == face_size:
                    pic = Image.new("RGBA", bg_size, 0)
                    pic.paste(target_img, target_pos, 0)
                    if self.is_alpha_paste:
                        FaceMatchFrame.paste_face(pic, temp, pos)
                    else:
                        pic.paste(temp, pos, 0)

                    path = os.path.join(save_path, f"{name}-{key}-{count}.png")

                    self.m_staticText_info.SetLabel(f"Connecting:{name}-{key}-{count}")
                    pic.save(path)
                else:
                    continue
        self.m_staticText_info.SetLabel(f"Joint completed")

    def initial(self, event):
        self.bg_paint.paste(self.target_img, (0, 0))
        self.paint_move(0, 0)

        self.m_panel7.Enable(False)

    def change_method(self, event):

        self.is_alpha_paste = bool(event.GetSelection())
        self.add_face()

    def select_face(self, event):
        index = event.GetSelection()
        values = self.input_values[self.view_list[index]]
        if index == self.select_index:
            if self.select_count < len(values) - 1:
                self.select_count += 1
            else:
                self.select_count = 0
        else:
            self.select_index = index
            self.select_count = 0

        guid = values[self.select_count]
        temp = PerInfo(f"{self.view_list[index]}-{self.select_count}",
                       f"{self.view_list[index]}-{self.select_count}",
                       False)
        temp.tex_path = guid

        self.view_work = QuickRestore(temp, None,
                                      size=tuple(self.m_panel_face.GetSize()),
                                      bitmap_show=self.m_bitmap_face,
                                      info_show=self.m_staticText_info)
        self.view_work.start()

        self.m_notebook_info.SetSelection(2)

        self.target_face = Image.open(guid)
        self.add_face()

    @staticmethod
    def value_check(event):
        """

        :param event:
        :return: if OK return True or return False
        """
        value = event.GetString()
        temp = re.sub(r'[^0-9\-]', "", value)
        temp.replace(".", "")
        temp.replace("-", "-0")
        # temp = re.sub(r'^-', "", temp)
        # temp = re.sub(r'\.\d+$', "", temp)
        if temp != value or temp == "":
            return False, temp
        else:
            return True, temp

    def value_check_x(self, event):
        is_ok, value = self.value_check(event)
        self.pos_x = value
        if not is_ok:
            # self.m_textCtrl_x_value.Clear()
            self.m_textCtrl_x_value.SetLabel(self.pos_x)
        else:
            pass

    def value_check_y(self, event):
        is_ok, value = self.value_check(event)
        self.pos_y = value
        if not is_ok:
            # self.m_textCtrl_y_value.Clear()
            self.m_textCtrl_y_value.SetLabel(self.pos_y)
        else:
            pass

    def value_check_px(self, event):
        is_ok, value = self.value_check(event)
        self.target_x = int(value)
        if not is_ok or value != self.target_x:
            # self.m_textCtrl_pic_x.Clear()
            self.m_textCtrl_pic_x.SetLabel(self.target_x)
        else:
            pass

    def value_check_py(self, event):
        is_ok, value = self.value_check(event)
        self.target_y = int(value)
        if not is_ok or value != self.target_y:
            # self.m_textCtrl_pic_y.Clear()
            self.m_textCtrl_pic_y.SetLabel(self.target_y)
        else:
            pass

    def wheel_x(self, event):
        angle = event.GetWheelRotation()
        guide = -angle // abs(angle)
        self.pos_x = self.pos_x + guide * self.step
        self.m_textCtrl_x_value.SetLabel(str(self.pos_x))

    def y_wheel(self, event):
        angle = event.GetWheelRotation()
        guide = -angle // abs(angle)
        self.pos_y = self.pos_y + guide * self.step
        self.m_textCtrl_y_value.SetLabel(str(self.pos_y))

    def px_wheel(self, event):
        angle = event.GetWheelRotation()
        guide = -angle // abs(angle)
        self.target_x = self._target_x + guide * self.step
        self.m_textCtrl_pic_x.SetLabel(self.target_x)

    def py_wheel(self, event):
        angle = event.GetWheelRotation()
        guide = -angle // abs(angle)
        self.target_y = self._target_y + guide * self.step
        self.m_textCtrl_pic_y.SetLabel(self.target_y)

    def set_step(self, event):
        value = event.GetString()
        self.step = int(value)

    def on_erase(self, event):
        pass

    def export(self, event):
        dialog = wx.SingleChoiceDialog(self, "Select export type", "Select export type", ("Export only the current expression combination", "Export all expression combinations of the same size"))
        if dialog.ShowModal() == wx.ID_OK:
            select = dialog.GetSelection()
            # If exporting using minimum size
            if self.m_checkBox_minosity_size.GetValue():
                begin_x = min(self.target_paint_x, self.pos_x)
                begin_y = min(self.target_paint_y, self.pos_y)
                end_x = max(self.target_paint_x + self.target_size[0], self.pos_x + self.target_face.width)
                end_y = max(self.target_paint_y + self.target_size[1], self.pos_x, +self.target_face.height)

                face_x_change = self.pos_x - begin_x
                face_y_change = self.pos_y - begin_y
                target_x_change = self.target_paint_x - begin_x
                target_y_change = self.target_paint_y - begin_y

                self.pos_x = face_x_change
                self.pos_y = face_y_change
                self.target_paint_x = target_x_change
                self.target_paint_y = target_y_change

                self.bg_size = (end_x - begin_x, end_y - begin_y)

                self.m_staticText_info.SetLabel(f"The size is modified to: {self.bg_size}")

            if select == 0:
                dialog = wx.FileDialog(self, f"Export {self.target.cn_name}-{self.select_index} expression combination", "./",
                                       f"{self.target.cn_name}-{self.select_index}.png", wildcard="*.png",
                                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dialog.ShowModal() == wx.ID_OK:
                    path = dialog.GetPath()
                    self.bg_paint.save(path)
            else:
                dialog = wx.DirDialog(self, "Export folder", "./",
                                      wx.DD_NEW_DIR_BUTTON | wx.DD_CHANGE_DIR | wx.DD_DEFAULT_STYLE)
                if dialog.ShowModal() == wx.ID_OK:
                    self.save_path = dialog.GetPath()
                    thread = Thread(target=self.export_all)
                    thread.start()
