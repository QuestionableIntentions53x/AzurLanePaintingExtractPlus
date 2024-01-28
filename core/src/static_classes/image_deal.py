import json
import os
import re
from functools import reduce

import PIL.Image
from re import match, split

import wx

import gettext
_ = gettext.gettext

from core.src.structs_classes.extract_structs import PerInfo


class ImageWork(object):
    @staticmethod
    def show_in_bitmap_contain(img, bitmap):
        temp = wx.Bitmap.FromBufferRGBA(img.width, img.height, img.tobytes())
        bitmap.ClearBackground()
        bitmap.SetBitmap(temp)

    """ IMAGE PROCESSING """

    @staticmethod
    def cut_pic_builder(size):
        """
        :param size: the input img size(width, height)
        :return: a callable function
        """
        #TODO: Get rid of this builder function, replace it with an inline lambda

        def cut_pic(info):
            a = [round(float(info[1]) * size[0]), round((1 - float(info[2])) * size[1])]

            return a

        return cut_pic

    @staticmethod
    def draw(pic, pos):
        """
        Function intended to be used with reduce(), draws the image onto itself at the position provided
        :param pic: The image segment
        :param pos: The position to displace the image by
        """
        pic.paste(pos[0], pos[1])
        return pic

    @staticmethod
    def division_builder(output, input, pic):
        """
        Constructs a function that returns segments of the given image based on the texture and mesh data provided
        :param draw_pic_list: List of output corners corners
        :param tex_pos_list: List of input corners
        :param pic: Input image
        :returns: Function that returns the requested segment
        """
        def division(val):
            """
            :param val: The three element tuple containing three corners 
            :return:    cut: The requested segment
                        print_area: The position it needs to be placed at
            """
            # Get the three corners of input and output
            #   (they are stored with (1,1) as the origin so they need to be offset)
            output_corners = [output[val[0] - 1], output[val[1] - 1], output[val[2] - 1]]
            input_corners  = [input[val[0] - 1],  input[val[1] - 1],  input[val[2] - 1]]

            # Of the three output corners, find the smallest x and y coordinates (top left)
            print_pos =  [min(output_corners[0][0], output_corners[1][0], output_corners[2][0]),
                          min(output_corners[0][1], output_corners[1][1], output_corners[2][1])]

            # Of the three input corners, find the smallest x and y coordinates (top left)
            cut_x = round(min(input_corners[0][0], input_corners[1][0], input_corners[2][0]))
            cut_y = round(min((input_corners[0][1], input_corners[1][1], input_corners[2][1])))

            # Of the three input corners, find the largest x and y coordinates (bottom right)
            end_x = round((max(input_corners[0][0], input_corners[1][0], input_corners[2][0])))
            end_y = round((max(input_corners[0][1], input_corners[1][1], input_corners[2][1])))

            # The rect defining the segment to cut out
            cut_size = (cut_x, cut_y, end_x, end_y)

            # Crop the specified area
            cut = pic.crop(cut_size)
            return cut, print_pos

        return division

    @staticmethod
    def file_analyze(size, mesh_path):
        """
        Analyze the mesh file and return data groups
        :param mesh_path: mesh file path
        :param size: texture image size
        :return:    draw_pic: drawing coordinates
                    tex_pos: cutting coordinates
                    print_pos: drawing groups
        """

        # Read raw mesh data
        with open(mesh_path, 'r', encoding='utf-8') as file:
            files_line = file.readlines()
        
        # TODO: improve explanation, provide example
        # Collect raw data for processing
        draw_pic = filter(lambda x: match(r'^v\s-*\d+\s-*\d+\s-*\d+\n$', x), files_line)
        tex_pos = filter(lambda x: match(r'^vt\s0\.\d+\s0\.\d+\n$', x), files_line)
        print_pos = filter(lambda x: match(r'^f\s\d+/\d+/\d+\s\d+/\d+/\d+\s\d+/\d+/\d+\n$', x), files_line)
        
        # Split raw data into individual numbers
        draw_pic = map(lambda x: split(r'\D+', x), draw_pic)
        tex_pos = map(lambda x: split(r'[^0-9.]+', x), tex_pos)
        print_pos = map(lambda x: split(r'\D+', x), print_pos)
        
        # Convert strings into their respective types
        draw_pic = (map(lambda x: [int(x[1]), int(x[2])], draw_pic))
        tex_pos = (map(ImageWork.cut_pic_builder(size), tex_pos))
        print_pos = (map(lambda x: [int(x[1]), int(x[4]), int(x[7])], print_pos))

        # Return the result
        return draw_pic, tex_pos, print_pos

    @staticmethod
    def spilt_texture(draw_pic, tex_pos, print_pos, y_pic, img):
        """
        :param draw_pic: The output corners to place the split segments at
        :param tex_pos: The input corner to split the image allong
        :param print_pos: Tuple storing three indexes to points in draw_pic and tex_pos, each segment has two entries
        :param img: The output image to edit
        :return: restore: A map containing the split image segments paired with the position they need to be drawn to 
        """
        # Build a devider and store the result of calling that devider with each value in the print_pos list
        division = ImageWork.division_builder(list(draw_pic), list(tex_pos), img)
        restore = (map(division, print_pos))
        
        return restore

    @staticmethod
    def az_paint_restore(mesh_path: str, tex_path: str, force_restorable=False):
        """
        A higher function version for extracting AzurLane paintings
        :param force_restorable: is a must-able item, just return the image and do not perform any action
        :param mesh_path: mesh_file address, str
        :param tex_path: texture file address
        :return: PIL.Image -> the final pic
        """
        # Get the components of the image
        restore, pic = ImageWork.spilt_only(mesh_path, tex_path, force_restorable)
        if force_restorable:
            return restore
        # Assemble by passing the draw function along with the image components and output image
        pic_out = reduce(ImageWork.draw, restore, pic)

        return pic_out

    @staticmethod
    def spilt_only(mesh_path: str, tex_path: str, force_restorable=False):
        """
        Split the raw mesh and texture and initalize the output image
        :param mesh_path: The absolute path to the mesh (.obj) file
        :param tex_path: The absolute path to the texture (.png) file
        :param force_restorable: returns the texture as an image as is
        :returns:   restore: A map of the split image segments paired with the position they need to be drawn to
                    pic: The propery sized output image
        """
        
        # img: Raw scrambled texture
        img = PIL.Image.open(tex_path)
        if force_restorable:
            return img, None
        
        # size: input image size (stored as powers of 2 for memory allignment)
        size = img.size
        
        # Get the current four corners of the texture (tex_pos) and the four corners they will be moved to (draw_pic)
        # Print pos is a tuple of image source and destination corners
        draw_pic, tex_pos, print_pos = ImageWork.file_analyze(size, mesh_path)
        draw_pic = list(draw_pic)

        # Get drawing coordinate point set
        pos = draw_pic.copy()
        x_poses, y_poses = zip(*pos)
        
        # Calculate canvas size
        x_pic = (max(x_poses))
        y_pic = (max(y_poses))
        
        # Create a new canvas
        pic = PIL.Image.new("RGBA", (x_pic, y_pic), (255, 255, 255, 0))
        
        # TODO: Skip every other print_pos entry since the data is redundant 
        # The draw_pic positions are stored with their y values inverted, so they need to be inverted
        draw_pic = (map(lambda x: [(x[0]), (y_pic - x[1])], draw_pic))

        # Cut
        restore = ImageWork.spilt_texture(draw_pic, tex_pos, print_pos, y_pic, img)
        
        return restore, pic
    
    @staticmethod
    def az_paint_deconstruct(mesh_path: str, tex_path: str, img_path: str, force_restorable=False):
        """
        A function that scrambles a given string using the provided mesh and texture
        :param force_restorable: If the image is unable to be converted, just return the image and do not perform any action
        :param mesh_path: Absolute path to the mesh file
        :param tex_path: Absolute path to the texture file
        :return: pic_out [PIL.Image] final scrambled image 
        """
        # Get the components of the image
        restore, pic = ImageWork.deconstruct_only(mesh_path, tex_path, img_path, force_restorable)
        if force_restorable:
            return restore
        # Assemble by passing the draw function along with the image components and output image
        pic_out = reduce(ImageWork.draw, restore, pic)

        return pic_out

    @staticmethod
    def deconstruct_only(mesh_path: str, tex_path: str, img_path: str, force_restorable=False):
        """
        Revert the image to it's original state
        :param mesh_path: The absolute path to the mesh (.obj) file
        :param tex_path: The absolute path to the texture (.png) file
        :param force_restorable: returns the texture as an image as is
        :returns:   restore: A map of the split image segments paired with the position they need to be drawn to
                    pic: The propery sized output image
        """
        
        # img: Restored image
        img = PIL.Image.open(img_path)
        
        if force_restorable:
            return img, None
        
        # img: Raw scrambled texture
        texture = PIL.Image.open(tex_path)
        
        # Get the current four corners of the texture (tex_pos) and the four corners they will be moved to (draw_pic)
        # Print pos is a tuple of image source and destination corners
        draw_pic, tex_pos, print_pos = ImageWork.file_analyze(texture.size, mesh_path)
        
        # Create a new canvas
        pic = PIL.Image.new("RGBA", texture.size, (255, 255, 255, 0))
        
        # Skip every other print_pos entry since the data is redundant 
        print_pos = list(filter(lambda x: (x[1] % 4 == 2), list(print_pos)))

        # The draw_pic positions are stored with their y values inverted, so they need to be inverted
        draw_pic = list(map(lambda x: [(x[0]), (img.size[1] - x[1])], list(draw_pic)))
        
        tex_pos = list(tex_pos)
        
        # I have no clue why each section ends up being croped on all sides and offset by one, but it is...

        for pos in range(int(len(tex_pos) / 4)):
            tex_pos[pos * 4 + 0][0] -= 1
            tex_pos[pos * 4 + 2][1] -= 1
            tex_pos[pos * 4 + 3][1] -= 1
            tex_pos[pos * 4 + 3][0] -= 1
        
        for pos in range(int(len(draw_pic) / 4)):
            draw_pic[pos * 4 + 0][0] -= 1
            draw_pic[pos * 4 + 0][1] += 1
            draw_pic[pos * 4 + 1][0] -= 1
            draw_pic[pos * 4 + 1][1] -= 1
            draw_pic[pos * 4 + 2][0] += 1
            draw_pic[pos * 4 + 2][1] -= 1
            draw_pic[pos * 4 + 3][0] += 1
            draw_pic[pos * 4 + 3][1] += 1
        
        # TODO: just keep these three as lists instead of sending them as maps
        draw_pic = map(lambda x: (x), draw_pic)
        tex_pos = map(lambda x: (x), tex_pos)
        print_pos = map(lambda x: (x), print_pos)

        # Cut
        restore = ImageWork.spilt_texture(tex_pos, draw_pic, print_pos, texture.size[1], img)
        
        return restore, pic

    """ IMAGE RESTORATION """

    @staticmethod
    def restore_tool(now_info: PerInfo):
        """
        Restores an initalized asset, stores the result into the provided PerInfo
        :param now_info: The asset's parsed information
        :return:    success: True if the image was successfully restored
                    messsage: Info about the process
        """
        try:
            # Check the status of the asset
            #  If it is unable to perform a restoration will return the raw texture as an image
            force_restorable = not now_info.get_restorable() and now_info.force_restorable
            pic = ImageWork.az_paint_restore(now_info.mesh_path, now_info.tex_path, force_restorable)

            pic.save(now_info.sanitize_file_name(now_info.save_path))
        except RuntimeError as info:
            # System error
            return False, str(info)
        except ValueError as info:
            # Math error
            return False, str(info)
        else:
            # Successfull restoration
            return True, _("Successfully restored: {}").format(now_info.cn_name)

    @staticmethod
    def restore_tool_one(mesh_path, pic_path, save_as):
        """DEPRICATED"""

        pic = ImageWork.az_paint_restore(mesh_path=mesh_path, tex_path=pic_path)

        assert isinstance(save_as, str)
        pic.save(save_as)

    @staticmethod
    def restore_tool_no_save(mesh_path, pic_path, size: tuple):
        """
        Restore and resize without saving it
        :param mesh_path: The absolute path to the mesh
        :param pic_path: The absolute path to the texture
        :param size: The size to change the restored image to
        """
        #TODO: Make this the default version of this function and move the save function to PerInfo
        pic = ImageWork.az_paint_restore(mesh_path, pic_path)
        return ImageWork.pic_size_transform(pic, size)

    """ IMAGE DECONSTRUCTION """

    @staticmethod
    def deconstruct_tool(now_info: PerInfo, pic_path: str):
        """
        Scrambles a provided asset and stores it in an output directory
        :param now_info: The asset's parsed information
        :param str: The absolute path to the overwriting asset
        :return:    success: True if the image was successfully restored
                    messsage: Info about the process
        """
        try:
            # Check the status of the asset
            #  If it is unable to perform a restoration will return the raw texture as an image
            force_restorable = not now_info.get_restorable() and now_info.force_restorable
            pic = ImageWork.az_paint_deconstruct(now_info.mesh_path, now_info.tex_path, pic_path, force_restorable)
            pic.save(now_info.tex_path.removesuffix(".png") + "_texture.png")
        except RuntimeError as info:
            # System error
            return False, str(info)
        except ValueError as info:
            # Math error
            return False, str(info)
        else:
            # Successfull restoration
            return True, _("Successfully saved to: {}").format(now_info.tex_path.removesuffix(".png") + "_texture.png")

    @staticmethod
    def deconstruct_tool_no_save(now_info: PerInfo, pic_path: str):
        """
        Scrambles a provided asset and stores it in an output directory
        :param now_info: The asset's parsed information
        :param str: The absolute path to the overwriting asset
        :return:    success: True if the image was successfully restored
                    messsage: Info about the process
        """
        try:
            # Check the status of the asset
            #  If it is unable to perform a restoration will return the raw texture as an image
            force_restorable = not now_info.get_restorable() and now_info.force_restorable
            pic = ImageWork.az_paint_deconstruct(now_info.mesh_path, now_info.tex_path, pic_path, force_restorable)
            pic.save(now_info.save_path)
        except RuntimeError as info:
            # System error
            return False, str(info)
        except ValueError as info:
            # Math error
            return False, str(info)
        else:
            # Successfull restoration
            return True, _("Successfully saved to: {}").format(now_info.save_path)

    """ IMAGE EDITING """

    @staticmethod
    def pic_transform(path, size):
        """
        Load and resize the image found at the given path
        :param path: The absolute path of the image
        :param size: The size to change the image to
        """
        pic = PIL.Image.open(path)
        return ImageWork.pic_size_transform(pic, size)

    @staticmethod
    def pic_size_transform(pic, size, is_resize=True):
        """
        Resize the given image
        :param pic: The image to resize
        :param size: The size to change the image to
        :parm is_reize: Resize the image or crop it, true by default
        """
        pic_size = pic.size
        bg = PIL.Image.new("RGBA", size, (255, 255, 255, 0))

        if is_resize:
            scale = min(bg.size[0] / pic.size[0], bg.size[1] / pic.size[1])
            size = (round(pic.size[0] * scale), round(pic.size[1] * scale))
            pic = pic.resize(size, PIL.Image.LANCZOS)

        x = round(bg.size[0] / 2 - pic.size[0] / 2)
        y = round(bg.size[1] / 2 - pic.size[1] / 2)
        bg.paste(pic, (x, y, x + pic.size[0], y + pic.size[1]))
        return bg, pic_size

    """ MISC """

    @staticmethod
    def split_only_one(target: PerInfo, save_path):
        """
        Export the split image to the given path
        :param target: The target to split
        :param save_path: the path to output to
        """
        pic_group, _ = ImageWork.spilt_only(target.mesh_path, target.tex_path, target.force_restorable)
        if target.force_restorable:
            pic_group.save(os.path.join(save_path, f"{target.cn_name}.png"))
        count = 1
        for pic in pic_group:
            pic[0].save(os.path.join(save_path, f"{target.cn_name}-{count}.png"))
            count += 1
            next(pic_group)

    @staticmethod
    def atlas_split_main(img, atlas_file):
        """
        Splitting the main function of the sprite
        :param img: Input PIL image
        :param atlas_file: Atlas file path
        :return:
        """
        # TODO: Provide a better explanation of the atlas splitting process

        info_pattern = re.compile(r'(.+)\n'
                                  r'\s{2}rotate:\s(false|true)\n'
                                  r'\s{2}xy:\s(\d+),\s(\d+)\n'
                                  r'\s{2}size:\s(\d+),\s(\d+)\n'
                                  r'\s{2}orig:\s\d+,\s\d+\n'
                                  r'\s{2}offset:\s0,\s0\n'
                                  r'\s{2}index:\s-1')
        group = {}

        # Load the splitting file
        with open(atlas_file, 'r', encoding="utf-8") as files:
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

    group_type = 0
    data_type = 1

    @staticmethod
    def match_code(tab_count: int, key: str, target_string, type_is=group_type):
        #TODO: Comment
        tabs = ''
        count = 0
        while count < int(tab_count):
            tabs += r'\s'
            count += 1
        if type_is == ImageWork.group_type:
            pattern = re.compile(f"{tabs}(?:\\d\\s)?{key}\\n(?:{tabs}\\s.+\\n)+")
        elif type_is == ImageWork.data_type:
            pattern = re.compile(f"{tabs}(?:\\d\\s)?{key} = (.+)\\n")
        else:
            pattern = re.compile(r'.+')
        group = pattern.findall(target_string)
        if group:
            return group[0]
        else:
            return ''

    @staticmethod
    def dump_work_json(file, use_id, id_num, pic):
        #TODO: Comment
        with open(file, "r") as f:
            f_info = json.load(f)

        render_data = f_info["0 Sprite Base"]["1 SpriteRenderData m_RD"]
        if use_id:
            path_id = render_data["0 PPtr<Texture2D> texture"]["0 SInt64 m_PathID"]
            if str(path_id) != id_num:
                return False, None
        try:
            offset = render_data["0 Rectf textureRect"]
            x_pos = round(float(offset['0 float x']))
            y_pos = round(float(offset['0 float y']))
            width = round(float(offset['0 float width']))
            height = round(float(offset['0 float height']))

            y_pos = pic.height - y_pos - height
            box = [x_pos, y_pos, width + x_pos, height + y_pos]
            data = pic.crop(box)
        except Exception as err_info:
            wx.MessageBox(_("Error") + file + "\n" + err_info, _("Error"), wx.ICON_ERROR)
            return False, None
        else:
            return True, data

    @staticmethod
    def dump_work_text(file, use_id, id_num, pic):
        #TODO: Comment
        with open(file, "r") as f:
            f_info = f.read()
        base = ImageWork.match_code(0, 'Sprite Base', f_info)
        render_data = ImageWork.match_code(1, 'SpriteRenderData m_RD', base)
        if use_id:
            texture = ImageWork.match_code(2, 'PPtr<Texture2D> texture', render_data)
            path_id = ImageWork.match_code(3, 'SInt64 m_PathID', texture, ImageWork.data_type)
            if path_id != id_num:
                return False, None
        try:
            offset = ImageWork.match_code(2, "Rectf textureRect", render_data)
            x_pos = round(float(ImageWork.match_code(3, 'float x', offset, ImageWork.data_type)))
            y_pos = round(float(ImageWork.match_code(3, 'float y', offset, ImageWork.data_type)))
            width = round(float(ImageWork.match_code(3, 'float width', offset, ImageWork.data_type)))
            height = round(float(ImageWork.match_code(3, 'float height', offset, ImageWork.data_type)))
            y_pos = pic.height - y_pos - height
            box = [x_pos, y_pos, width + x_pos, height + y_pos]
            data = pic.crop(box)
        except Exception as err_info:
            wx.MessageBox(f"Error occurred while processing\n【{file}】\n({err_info})", "Error", wx.ICON_ERROR)
            return False, None
        else:
            return True, data

    @staticmethod
    def split_sprite(target: PerInfo, files: list, id_num: str, dump_file: int):
        """
        Debug function to dump texture json or text data
        :param target: The asset to dump info about
        :param files: The files to parse
        :param id_num: The id number to check against
        :param dump_file: 0 = dump text file, 1 = dump json file 
        """
        if id_num == '':
            use_id = False
        else:
            use_id = True
        pic = PIL.Image.open(target.tex_path)
        info = {}
        match = 0
        if dump_file == 0:
            func = ImageWork.dump_work_text
        else:
            func = ImageWork.dump_work_json
        for file in files:
            name = os.path.splitext(os.path.basename(file))[0]
            #
            is_able, data = func(file, use_id, id_num, pic)
            if is_able:
                info[name] = data
                match += 1

        return info, match