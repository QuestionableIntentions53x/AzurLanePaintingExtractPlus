# 【Azur Lane】Auxiliary Painting Processing Tool (ALPE+) Tutorial

## Author: 凊弦凝绝Official

------------

### Requirements

* This tutorial requires Unity unpacking tools other than AZPTP (choose one of the two, you can use both):

   1. [UABE(Unity Assets Bundle Extractor)](https://github.com/nesrak1/UABEA)

   2. [Assets Studio(原Unity Studio)](https://github.com/Perfare/AssetStudio)

* Main repository：[碧蓝航线立绘辅助处理工具(AzurLanePaintingTool)](https://github.com/azurlane-doujin/AzurLanePaintingExtract-v1.0)

### Download

![image](https://i0.hdslb.com/bfs/bigfun/febdbde6ba1a03d918fc28e43452da9f33d42fc0.png@760w_1o_1g)

<font color = ff000>To download the corresponding tools, please go to the release page to download (the arrow in the picture points). Do not use "clone or download" which is to download the source code.
</font>

ALPT[下载页面](https://ci.appveyor.com/project/Perfare/assetstudio/branch/master/artifacts)

Assets Studio[下载界面](https://ci.appveyor.com/project/Perfare/assetstudio/branch/master/artifacts)


------------

### Resource preparation (only use Unity unpacking tool, Assets Studio is recommended for this part)

#### Resource location

* The game resources of Azur Lane are divided into 2 parts. Some of them are in the game installation package; the other part are in the hot update game resource package.

#### Process

##### For resource files located in the installation package

1. You can download the installation package directly from Azur Lane’s official website（*.apk）Then use compression software (if the computer's built-in compression software cannot decompress, you can try changing the extension to *.zip) to decompress the file and obtain the decompressed folder.

2. In the folder obtained after decompression, find the "assets" folder and enter; then find the "AssetBundles" folder. This folder is the folder where Azur Lane's in-game materials are located. You can copy this folder to another place for later use. use.

##### For hot-updated game resource packages, the following operations only support Android phones or Android emulators.

> <font color=#ff0000> Note that the Azur Lane hot update resource package is stored inside the phone, not externally.（SDK）</font>

1. Find the following path "/storage/emulated/0/Android/data/com.biliblili.azurlane/files/AssetBundles" in the mobile resource manager. You can package the whole or part of the folder and send it through QQ My Device, etc. to computer for backup.

#### Resouce Types

---

* activity_painting 活动立绘
* activitybanner 活动横幅
* aircrafticon 飞机图标
* battlescore 战斗得分
* bg 背景
* box 框
* boxprefab 框
* chapter 章节地图纹理图
* > pic 图
* char Q版小人结构图
* chargeicon 氪金图标
* chargo 大飞机图标
* clouds 云贴图
* clutter 活动宣传图
* commanderhrz 指挥喵放技能横图
* commandericon 指挥喵头像
* commanderrarity 指挥喵稀有度
* commanderskillicon 指挥喵技能图标
* commandertalenticon 指挥喵天赋
* commonbg 常用背景
* cue 语音
* dailylevelicon 每日副本图标
* dormbase 宿舍基地
* dutyicon 职位图标
* effect 效果
* > img 效果图
* >mat_anim
* emblem 军衔
* emoji 表情
* enemies 敌舰
* equips 装备
* event type 事件结果
* extra 附加
* font 字体图片
* furniture 家具
* furnitureicon 家具图标
* helpbg 帮助
* herohrzicon 放技能横图
* item 外观装备
* levelmap 地图
* live2d live2d
* loadingbg 过场图
* lotterybg 奖池背景
* map 贴图
* mapres 贴图资源
* >sea_single 海
* >sky_single 天
* memoryicon 回忆 剧情
* numbericon 数字图标
* painting 立绘
* paintingface 表情差分
* prints 阵营
* props 道具
* puzzla 拼图
* qicon Q版头像
* sfurniture 家具贴图
* shipdesignicon 科研图标
* shipmodels 小人
* shiprarity 舰船稀有度
* shipyardicon 船坞图标
* skillicon 技能图标
* squareicon 方形图标
* strategyicon 阵型图标
* ui 用户界面

---

* by Crayonkun

> <font color = ffoxe0>（If it only applies to this tool, just keep “char”,"painting","paintingface"）</font>

---

#### Begin Unpacking

* Run AssetsStudio，the process is as shown in the figure：

![image](https://i0.hdslb.com/bfs/bigfun/902cc4c7245d984a7e584008d5d114ff1f1c7f42.png@760w_1o_1g)

##### 【Import】

* Use "file"->"load file"/"load folder" to load files; when importing files in painting, you may find that there are two files of the same ship girl portrait in the folder ( The picture shows the original Tashkent skin as an example)

![inage](https://i0.hdslb.com/bfs/bigfun/41ac888697026754cc8fe9b5820b31e305480600.png@760w_1o_1g)
> In actual operation, the original vertical drawing and restoration parameter files of some vertical paintings will be distributed in these two files, so they are usually imported at the same time.

* After the import is completed, click "Asset List" to display the file list, as shown below:

![mage](https://i0.hdslb.com/bfs/bigfun/5b5d577e615c2685d58cc6b834f203c0d94028af.png@760w_1o_1g)

* The selected element in the picture is the requirement file for restoring the vertical painting.

![image](https://i0.hdslb.com/bfs/bigfun/6ad4039d7b83ca641610a317cbb945e9d9f4b604.png@760w_1o_1g)

##### 【Export】

* Click "Export"->"Select assets", select the export folder, and wait for the export to complete. If the default settings are not changed, the export target folder will automatically open after the export is completed, as shown in the figure.

![image](https://i0.hdslb.com/bfs/bigfun/b69228fd15ebdde1d273a59b9c630e26c6bb9d29.png@760w_1o_1g)

> Two folders appear in the export directory, textures (.png) in Texture2D and cutting information files (.obj) in Mesh. The resources are ready!

----

### Features

> <font color=ff234d>If you want to get started directly, you can skip this part</font>

* Unzip the downloaded 7Z file, find the exe file, and double-click to run it (please unzip it first!)

![image](https://i0.hdslb.com/bfs/bigfun/ca2dc12cbfeb0afde48b81e31bba24dd595427b6.png@760w_1o_1g)

* The interface is as shown in the figure：

![image](https://i0.hdslb.com/bfs/bigfun/c987ec964dabb177ddb1f1e7ecf94df881660c44.png@760w_1o_1g)
##### Regional introduction
| Label | Information |
|:----:|:---|
| ① | It is the material import and data display area. In this area, you can drag and import materials (supports mixed import of multi-level folders and file folders), and display the elements after the import is completed |
| ② | is the image preview area. In this area, you can display the original file preview and restoration effect preview of the imported material. |
 | ③ | is the progress bar. Show import and export progress during import, export |
 | ④ | is the information box. Information such as the number of imported elements, preview type, export status, etc. will be displayed |

##### other parts:
| Label | Information |
|:----:|:---|
| ① |The upper left side of the ① area is a filter, which will filter and display objects that meet the conditions |
| ② | There is a search box on the right side above the ① area. Entering characters will immediately search and display the search results |
| ③ | "Export" button. Clicking to export will pop up the export type window |
| ④ | "Select the corresponding file" button. Used to modify the Texture2D file and Mesh file for restoration to the object |
| ⑤ | "Settings" button. Enter the setting interface |

>In order to show the complete functionality, I first import the material
 
![image](https://i0.hdslb.com/bfs/bigfun/8e1df4b50404e924183318abbb8eb46061a48be4.png@760w_1o_1g) 

* 如图，导入完成。

---
> I fully expanded the information in the Tashkent element, as shown in the figure

![image](https://i0.hdslb.com/bfs/bigfun/6cc592f06132fd9f362b7bffdf26443e0e115e1f.png@760w_1o_1g)

>Number from top to bottom

| Label | Name | Function introduction |
|:----:|:---|:---|
| ① | Element root tag | Clicking will restore the preview. If preview is not available, the original file will be displayed |
| ② | Element localized name | If the font color of the label is pink (in the picture), the element is a reducible object |
| ③ | Element index name | That is, the file name of the imported element |
| ④ | The currently used Texture2D file path (priority: files in Texture2D > files in Sprite > files containing #\d + file identification stamp with the same name) | Click to preview the element file |
| ⑤⑥⑦ | Texture2D available for selection | There may be a longer list in actual use. After selecting an element, you can preview the element file (if you can preview it), and you can also click "Select Corresponding File" to set the currently selected file Is the currently used Texture2D. If modified to "Empty", Texture2D will be disabled (this element will become "irreducible") |
| ⑧ | Currently used Mesh file path (priority: file in Mesh > file containing #\d + file identification stamp with the same name) | None |
| ⑨⑩⑾ | Available Mesh | There may be a longer list in actual use. You can also click "Select Corresponding File" to set the currently selected file as the currently used Mesh. If modified to "Empty", Mesh will be disabled (this element will become "irreducible") |
| ⑿~⒆ | It is an additional functional area | I will not focus on it here |
---

* Click "Export" to pop up the export window, as shown in the figure

![image](https://i0.hdslb.com/bfs/bigfun/7790d67205998f5e74b62246f066e983c82c7340.png@760w_1o_1g)

###### Export type:

| Label | Name | Function introduction |
|:----:|:---|:---|
| ① | "Export all restoreable" | will export all restoreable imported elements to the target folder (available when there is at least one restoreable object) |
| ② | "Copy all non-restorable" | The non-restorable objects will be copied directly to the target folder (at least one non-restorable object is available) |
| ③ | "Export Selection" | will export the currently selected element (you can also select the sub-elements within each element) to the specified path |
| ④ | "Export current list items" | Export the elements in the current list to the target folder (available after using the search function or filter function) |
---
* Click "Settings" to open the setting interface, as shown in the figure

![image](https://i0.hdslb.com/bfs/bigfun/cbc556ba89b3802b00029811c987f25f264d7814.png@760w_1o_1g)

> Numbered from top to bottom, from left to right

| Label | Name | Function introduction |
|:----:|:---|:---|
| ① | "Use Chinese name as export file name (if available)" | If checked, the localized name of the vertical painting will be used as the export file name (using "Export Selection" will not be affected) |
| ② | "Create a new export folder in the export destination directory" | If checked, a new "Azur Lane-Export" folder will be created in the export destination folder, and the export file will be placed in the above folder |
| ③ | "Open destination folder when finished" | This feature has been deprecated, please do not check |
| ④ | "Skip files with the same name that already exist in the target directory" | If checked, existing files in the target folder will be skipped (unchecked will overwrite) |
| ⑤ | "Clear original files when importing" | If checked, the original list will be cleared each time it is imported. If not checked, the import effect will be additional |
| ⑥ | "Exit after completing the task" | When the export task is completed, it will automatically exit |
| ⑦ | "Export and copy all at the same time and cannot be restored" | This is equivalent to selecting "Export all for restoration" and "Copy all for restoration" at the same time when exporting |
| ⑧ | "Import file filter" | Similar to the main interface filter, but it filters files that do not meet the conditions when importing |
| ⑨ | "Export file classification" | The exported files will be classified by "type" or by "ship girl" according to the selected method |
| ⑩ | "Update localization resources", "Edit localization resources" | For online updates and manual editing, adding localization resources |

---
* Click "Update Localization Resources" to enter the "Update Localization Resources Interface", as shown in the figure

![image](https://i0.hdslb.com/bfs/bigfun/596c7eb238117f2fd5b3c8fdba89233d9da87fd5.png@760w_1o_1g)

①The area is a selection area. Use the "+" and "-" in the upper part to add and delete localized resource sources; double-click the localized resource source in the upper part to load the localized resource (which may cause lag). After the loading is completed , the results will be displayed in ②, you can also choose to directly use "Load File" to select the target json file

②It is the localized loading result, which can be expanded to view specific information.

③ is the update application type. "Apply - All" will directly overwrite the original files with new localized resource files; "Apply - New" will only add new resources to the original localized files; "Apply - Overwrite" will only Portions of the loaded resource that differ from the original localized resource are replaced with the loaded resource

Click "Edit Localization Resources" to enter the "Edit Localization Resources" interface, as shown in the figure

![image](https://i0.hdslb.com/bfs/bigfun/883ebde1f5bf19b09b7c1e4fed128ee5f5e1c262.png@760w_1o_1g)

| Label | Information |
|:----:|:---|
| ① | is a list of existing localization resources. Click to select to add the selected localization content to ②. Double-click to select and the selected localization resources will be displayed in a pop-up window |
| ② | You can edit the key (index name of the imported element) and value (localized name of the imported element). The key can exist in the existing localized resource list or it can be new. The value can be the same as the localized resource list. The median is the same (but this is not recommended) |
| "Clear" | will clear the corresponding contents in the current "key" and "value" |
| "Add" | will add the current "key" and "value" to the existing localized resources. If the key already exists, a pop-up window will pop up to ask |
| "+" | The function is the same as "Load file" in "Update localized resources", but the effect is to directly apply all |
#### Introduction completed!

---

### Introduction to additional functional areas
> Stay tuned

---

### Tool usage

1. [Import] Select the file or folder exported using Assets Studio and drag it to the red box in the picture. (Don’t worry about whether there are other interfering files. This tool has complete entry detection and will automatically filter files that do not meet the conditions. Yes, you can even drag all the files on the entire disk into it, but it may be stuck for a long time)

![image](https://i0.hdslb.com/bfs/bigfun/f0ac35077a2db8ef7b515683284d437319d98028.png@760w_1o_1g)

2. After the import is completed, you can click on a few elements to preview.

![image](https://i0.hdslb.com/bfs/bigfun/8d1aae843fdf6be5d848f13c3aec08dc81f85fd7.png@760w_1o_1g)

3. Click "Export" -> "Export All Recoverable", select the export folder, and wait for completion

![image](https://i0.hdslb.com/bfs/bigfun/c29ef1c6bda34f726baa415187acc5c53c748ec6.png@760w_1o_1g)

4. Wait for completion

> You can see the exported vertical painting in the export directory!

![image](https://i0.hdslb.com/bfs/bigfun/c6d1c042a3786f0fdc5a82a26d383d6943db3db3.png@760w_1o

