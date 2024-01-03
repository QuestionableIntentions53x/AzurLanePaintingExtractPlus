# Azur Lane Painting Extract Plus (ALPEP) v0.1:

## Current State

Hey there! QI here. This is a fork of [AzurLanePaintingExtract-v1.0](https://github.com/azurlane-doujin/AzurLanePaintingExtract-v1.0) that I plan to fully localize and add some minor improvements on top of. Currently, many of the features are non-functional, so expect to encounter some jank. The strings and comments were all translated from Chinese with a translator, but I haven't had the chance to clean it up yet.

## Help

The whole process as of right now is as follows:
1. Go to: `/storage/emulated/0/Android/data/com.YoStarEN.AzurLane/files/AssetBundles/painting/...` and grab the `tex` files for the ship (e.g. `kaxin_tex` is Cassin's texture file).
    * Note that many ships have multiple `tex` files, but the ones you should care about are as follows:

    | Postfix | Meaning |
    |:--:|:--|
    | `_rw_` or no tags | Default skin |
    | `_#_` or `_#` | Premium skin |
    | `_n_` | Retrofit |
    | `_g_` | Oath |
    | `_alter_` | META |
    | `_ex_` | Research ships |
    | `_idol_` or `_idolns_` | MUSE |
    | `_younv_` | Child ships |

    * You can find the conversion between English ship names and the file names [here](https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/EN/ShareCfg/ship_skin_template.json), just use `CTRL+F` to search for the ship name. There should be an entry called "painting" somewhere below it. (e.g. "Universal Bulin" -> "gin")
2. Now you need to download [AssetStudio](https://github.com/Perfare/AssetStudio) to extract the texture and mesh data. Drag the `tex` files into AssetStudio and navigate to the AssetList tab, download the `Texture2D` and `Mesh` files (select the two files,  right-click, and choose `Export selected assets`.
3. They will be exported into two separate folders, combine them into a single folder. Now, `open ALPEP.exe`, drag the `Texture2D` (`ship_name.png`) and `Mesh` (`ship_name.obj`) files onto the left menu area. It should display the repaired asset on the right. To export the repaired asset, click the `Export` button in the lower left corner.
4. After editing the texture to your liking (or if you have a different image you want to convert to a texture): Expand the Funtions section of the tree and select the final option called `Import PNG`, then navigate to the `.png` you want to convert. The output file will be placed in the same folder as the texture file with the word `texture` appended to the end.
5. To recombine the texture and mesh files you need to use [UABE](https://github.com/nesrak1/UABEA). Drag the `tex` blob file into UABE and click `save to memory`, then click `info`, then select the file of type `texture2D`, then in the right menu click `Plugins` then select `Edit Texture` then click `Ok`, click `Load` at the bottom of the menu and navigate to the output file prodced in step 4. Press `CTRL+S` and exit the info menu, now press `file` in the upper ribbon menu and `save as...`, ensure the name of the file is identical to the original.
6. The final step is to copy paste the modded texture file to the game files
7. Enjoy!

## Future Development

On top of revamping the original features, I plan to turn the asset conversion and editing process into a library
Better localization will come in the future

## Contributions

Contributions should wait until it reaches a more stable state, stay tuned