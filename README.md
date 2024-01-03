# NOTE:

## Current State

This rework is still in progress and many of the proposed features are currently non-functional
The translations were done by Google, and haven't been cleaned up yet, but if you're here for the method of converting from raw texture files to pieced together pngs and back again, then the process is as follows:
1. Go to: `/storage/emulated/0/Android/data/com.YoStarEN.AzurLane/files/AssetBundles/painting/...` (see below for conversion between english ship names and file names) and grab the `_tex` files associated with it*.
2. Follow the steps found in HELP.md for processing and importing images
3. After editing the texture to your liking or if you have a new image you want to convert to a texture: Expand the Funtions section of the tree and select the final option, then navigate to the .png you want to convert. The output file will be placed in the same folder as the texture file with the word `texture` appended to the end.
4. To recombine the texture and mesh files you need to use [UABE](https://github.com/nesrak1/UABEA). Drag the `_tex` blob file into UABE and click "save to memory", then click "info", then select the file of type "texture2D", then in the right menu click "Plugins" then select "Edit Texture" then click "Ok", click "Load" at the bottom of the menu and navigate to the output file prodced in step 4. Press `CTRL+S` and exit the info menu, now press "file" in the upper ribbon menu and "save as...", ensure the name of the file is identical to the original.
5. The final step is to copy paste the modded texture file to the game files
6. Enjoy!

## Future Development

On top of revamping the original features, I plan to turn the asset conversion and editing process into a library
Better localization will come in the future, for now if you need to find the blob file name from the ship's English name go [here](https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/EN/ShareCfg/ship_skin_template.json)

## Contributions

Contributions should wait until it reaches a more stable state, stay tuned

# AzurLanePaintingExtract-v1.0
### Tools:
---------------------
| Tool | Introduction |
|:--:|:--|
| [asset studio](https://github.com/Perfare/AssetStudio) | Unpacking tool essential for home travel |
| [UABE](https://github.com/DerPopo/UABE) | Retrieves Path_ID, can also package in [Unity](https://unity.com/) |
------------------
### Features:
------------------
| Feature | Applicability | Effect | Requirements |
|:--:|:-----:|:---:|:--:|
| Basic character painting processing | Core functionality for character paintings in [Azur Lane](https://game.bilibili.com/blhx/) | Restores broken original unpacked character paintings | At least one Texure2D (.png), at least one Mesh (.obj) |
| Additional expressions for character paintings | Functionality for differential expressions of [Azur Lane](https://game.bilibili.com/blhx/) characters and characters without heads | Attaches facial expressions to character paintings (considering using Path_ID for matching) | Can be applied to a single character or a combination, meets the requirements of basic character painting processing |
| Chibi ([Spine](http://zh.esotericsoftware.com/)) character cutting | Applicable to all [Spine](http://zh.esotericsoftware.com/) atlas cutting | Cuts a single texture into a group of images | At least one Texuture2D (.png) and one Atlas (.atlas | .atlas.txt) |
| Sprite cutting | Functionality for cutting [Unity](https://unity.com/) sprites, theoretically applicable to all Unity Sprite objects | Cuts the original image based on the reference PathID and Sprite Dump file, obtaining a group of images | At least one Texture2D (.png), one Dump (.txt) |
------------
### Update History:
#### Version 1.X
* [【Azur Lane】Character Painting Processing Tool-1.4](https://www.bilibili.com/read/cv5048786)
* [【Azur Lane】Character Painting Processing Tool v1.2 Update](https://www.bilibili.com/read/cv3983757)
* [【Azur Lane】Character Painting Export Tool-1.0 Remake](https://www.bilibili.com/read/cv2801922)
--------------------------
#### Version 0.X
* [【Azur Lane】AzurLane-PaintingExtract v 0.7.0 Update](https://www.bilibili.com/read/cv1786736)
* [【Azur Lane】Character Painting, Spine Characters, Live2D](https://www.bilibili.com/read/cv1566510)
* [【Azur Lane】Character Painting Restoration Program v-0.6.0 Update](https://www.bilibili.com/read/preview/1439259)
* [Azur Lane Character Painting Restoration Update-v-0.2.0](https://www.bilibili.com/read/cv1316278)
* [Azur Lane Character Painting Restoration Program Update](https://www.bilibili.com/read/cv1127720)
* [Azur Lane Character Painting Restoration Program (GUI Version) Update](https://www.bilibili.com/read/cv1019910)
* [Azur Lane Character Painting Restoration Program (GUI Version)](https://www.bilibili.com/read/cv1013553)
* [Azur Lane Character Painting Restoration Update (Batch Processing)](https://www.bilibili.com/read/cv941333)
* [Azur Lane Character Painting Restoration Program Update (1)](https://www.bilibili.com/read/cv936784)
* [Azur Lane Character Painting Restoration Program Update](https://www.bilibili.com/read/cv933308)
* [AzurLanePaintingRestore Update](https://www.bilibili.com/read/cv911094)
* [AzurLinePaintingRestore Update](https://www.bilibili.com/read/cv893994)
* [【Azur Lane】Character Painting Restoration Program Update](https://www.bilibili.com/read/cv886956)
---------------------
#### Tutorials
* [【Azur Lane】How to Manually Extract Ship Girl Paintings](https://www.bilibili.com/read/cv1330829)
* [How to Extract Azur Lane Paintings Tutorial (Simple Version)](https://www.bilibili.com/read/cv894737)
* [How to Manually Extract Azur Lane Paintings](https://www.bilibili.com/read/cv565639)
---------------------
#### Bigfun Page
* [Currently being updated](https://www.bigfun.cn/post/219941)
---------------------
![image](https://i0.hdslb.com/bfs/bigfun/69c19a99f508849b846931cedd339d8034a9e18a.png@760w_1o_1g)