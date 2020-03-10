import json
import os
import re
from functools import reduce

import PIL.Image
from re import match, split

from core.src.structs_classes.extract_structs import PerInfo


class ImageWork(object):
    @staticmethod
    def cut_pic_builder(size):
        """
        :param size: the input img size(wide,high)
        :return: a callable func
        """

        def cut_pic(info):
            a = [round(float(info[1]) * size[0]), round((1 - float(info[2])) * size[1])]

            return a

        return cut_pic

    @staticmethod
    def draw(pic, pos):
        pic.paste(pos[0], pos[1])
        return pic

    @staticmethod
    def division_builder(val1, val2, pic):
        def division(val):
            print_p = [val1[val[0] - 1], val1[val[1] - 1], val1[val[2] - 1]]
            cut_p = [val2[val[0] - 1], val2[val[1] - 1], val2[val[2] - 1]]

            print_area = [min(print_p[0][0], print_p[1][0], print_p[2][0]),
                          min(print_p[0][1], print_p[1][1], print_p[2][1])]

            cut_x = round(min(cut_p[0][0], cut_p[1][0], cut_p[2][0]))
            cut_y = round(min((cut_p[0][1], cut_p[1][1], cut_p[2][1])))

            end_x = round(
                (max(cut_p[0][0], cut_p[1][0], cut_p[2][0])))
            end_y = round(
                (max(cut_p[0][1], cut_p[1][1], cut_p[2][1])))

            cut_size = (cut_x, cut_y, end_x, end_y)

            cut = pic.crop(cut_size)
            return cut, print_area

        return division

    @staticmethod
    def file_analyze(size, mesh_path):
        """
        分析mesh文件，并返回数据组
        :param mesh_path: mesh文件路径
        :param size: texture图片尺寸
        :return:    draw_pic:绘制坐标
                    tex_pos:切割坐标
                    print_pos:绘制分组
        """
        tex_cuter = ImageWork.cut_pic_builder(size)
        with open(mesh_path, 'r', encoding='utf-8')as file:
            files_line = file.readlines()
        # 文件解析-1-将文件进行初步分类
        # draw_pic:绘制坐标
        # tex_pos:切割坐标
        # print_pos:绘制分组
        draw_pic = filter(lambda x: match(r'^v\s-*\d+\s-*\d+\s-*\d+\n$', x), files_line)
        tex_pos = filter(lambda x: match(r'^vt\s0\.\d+\s0\.\d+\n$', x), files_line)
        print_pos = filter(lambda x: match(r'^f\s\d+/\d+/\d+\s\d+/\d+/\d+\s\d+/\d+/\d+\n$', x), files_line)
        # 文件解析-2-将具体参数分离出来
        draw_pic = map(lambda x: split(r'\D+', x), draw_pic)
        tex_pos = map(lambda x: split(r'[^0-9.]+', x), tex_pos)
        print_pos = map(lambda x: split(r'\D+', x), print_pos)
        # 文件解析-3--将分离的参数转换为可用的参数类型
        draw_pic = (map(lambda x: [int(x[1]), int(x[2])], draw_pic))
        tex_pos = (map(tex_cuter, tex_pos))
        print_pos = (map(lambda x: [int(x[1]), int(x[4]), int(x[7])], print_pos))

        return draw_pic, tex_pos, print_pos

    @staticmethod
    def spilt_texture(draw_pic, tex_pos, print_pos, y_pic, img):

        # 计算切割坐标
        draw_pic = (map(lambda x: [(x[0]), (y_pic - x[1])], draw_pic))
        # 切割
        division = ImageWork.division_builder(list(draw_pic), list(tex_pos), img)
        restore = (map(division, print_pos))

        return restore

    @staticmethod
    def az_paint_restore(mesh_path: str, tex_path: str, must_able=False):
        """
        a higher func version for extract AzurLane painting
        :param must_able: is a must able item,just return image and do not have any action
        :param mesh_path: mesh_file address,str
        :param tex_path: texture file address
        :return: PIL.Image -> the final pic
        """
        restore, pic = ImageWork.spilt_only(mesh_path, tex_path, must_able)
        if must_able:
            return restore
        # 组装
        pic_out = reduce(ImageWork.draw, restore, pic)

        return pic_out

    @staticmethod
    def spilt_only(mesh_path: str, tex_path: str, must_able=False):
        img = PIL.Image.open(tex_path)
        if must_able:
            return img, None

        size = img.size
        draw_pic, tex_pos, print_pos = ImageWork.file_analyze(size, mesh_path)
        draw_pic = list(draw_pic)
        # 获取绘制坐标点集合
        pos = draw_pic.copy()
        x_poses, y_poses = zip(*pos)
        # 计算画布尺寸
        x_pic = (max(x_poses))
        y_pic = (max(y_poses))
        # 新建画布
        pic = PIL.Image.new("RGBA", (x_pic, y_pic), (255, 255, 255, 0))
        # 切割
        restore = ImageWork.spilt_texture(draw_pic, tex_pos, print_pos, y_pic, img)
        return restore, pic

    @staticmethod
    def restore_tool(now_info: PerInfo):
        """拼图用的函数
        """
        try:
            must_able = not now_info.get_is_able_work() and now_info.must_able
            pic = ImageWork.az_paint_restore(now_info.mesh_path, now_info.tex_path, must_able)

            pic.save(now_info.save_path)
        except RuntimeError as info:
            return False, str(info)
        except ValueError as info:
            return False, "math" + str(info)
        else:
            return True, "成功还原：%s" % now_info.cn_name

    @staticmethod
    def restore_tool_one(mesh_path, pic_path, save_as, ):
        """拼图用的函数"""

        pic = ImageWork.az_paint_restore(mesh_path=mesh_path, tex_path=pic_path)

        assert isinstance(save_as, str)
        pic.save(save_as)

    @staticmethod
    def restore_tool_no_save(mesh_path, pic_path, size: tuple):
        """拼图用的函数"""
        pic = ImageWork.az_paint_restore(mesh_path, pic_path)
        return ImageWork.pic_size_transform(pic, size)

    @staticmethod
    def pic_transform(path, size):
        pic = PIL.Image.open(path)
        return ImageWork.pic_size_transform(pic, size)

    @staticmethod
    def pic_size_transform(pic, size, is_resize=True):
        pic_size = pic.size
        bg = PIL.Image.new("RGBA", size, (255, 255, 255, 0))

        if is_resize:
            scale = min(bg.size[0] / pic.size[0], bg.size[1] / pic.size[1])
            size = (round(pic.size[0] * scale), round(pic.size[1] * scale))
            pic = pic.resize(size, PIL.Image.ANTIALIAS)

        x = round(bg.size[0] / 2 - pic.size[0] / 2)
        y = round(bg.size[1] / 2 - pic.size[1] / 2)
        bg.paste(pic, (x, y, x + pic.size[0], y + pic.size[1]))
        return bg, pic_size

    @staticmethod
    def split_only_one(target: PerInfo, save_path):
        pic_group, _ = ImageWork.spilt_only(target.mesh_path, target.tex_path, target.must_able)
        if target.must_able:
            pic_group.save(os.path.join(save_path, f"{target.cn_name}.png"))
        count = 1
        for pic in pic_group:
            pic[0].save(os.path.join(save_path, f"{target.cn_name}-{count}.png"))
            count += 1
            next(pic_group)

    @staticmethod
    def atlas_split_main(img, atlas_file):
        """
        切割小人的主要函数
        :param img: 输入的PIL图像
        :param atlas_file: atlas文件路径
        :return:
        """
        info_pattern = re.compile(r'(.+)\n'
                                  r'\s{2}rotate:\s(false|true)\n'
                                  r'\s{2}xy:\s(\d+),\s(\d+)\n'
                                  r'\s{2}size:\s(\d+),\s(\d+)\n'
                                  r'\s{2}orig:\s\d+,\s\d+\n'
                                  r'\s{2}offset:\s0,\s0\n'
                                  r'\s{2}index:\s-1')
        group = {}

        # 加载分割文件
        with open(atlas_file, 'r', encoding="utf-8")as files:
            file_work = files.read()

        info = info_pattern.findall(file_work)

        for body in info:
            mod_name = body[0]
            group[mod_name] = {}
            group[mod_name]['rotate'] = json.loads(body[1])
            group[mod_name]['xy'] = [int(body[2]), int(body[3])]
            group[mod_name]['size'] = [int(body[4]), int(body[5])]

        values = {}
        for var in group.keys():

            xy = group[var]['xy']
            size = group[var]['size']

            if group[var]['rotate']:
                rect = (xy[0], xy[1], size[1] + xy[0], size[0] + xy[1])
            else:
                rect = (xy[0], xy[1], size[0] + xy[0], size[1] + xy[1])

            val = img.crop(rect)
            if group[var]['rotate']:
                val = val.rotate(-90, expand=True)

            values[var] = val

        return values
