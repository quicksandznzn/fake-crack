from fontTools.ttLib import TTFont


def base_font_object_list():
    """
        基础object
    :return:
    """
    font = TTFont("../file/font/basefont.woff2")
    uni_list = font.getGlyphOrder()[2:]
    # font.saveXML('font_template.xml')
    # cmap = font.getBestCmap()
    font_list = ["", "", "7", "4", "1", "", "9", "2", "8", "5", "0", "3", "6", "", "7"]
    # 取出每个unicode所对应的字形对象
    font_objs = []
    for i in uni_list:
        font_objs.append(font["glyf"][i])
    # 将每个数字和它对应的字形对象以元组的形式放在列表中[字形对象永远不会变]
    base_font_object_list = []
    for i in range(len(uni_list)):
        base_font_object_list.append((font_objs[i], font_list[i]))
    return base_font_object_list


def base_font_cmap(key):
    """
        基础映射
    :param key:
    :return:
    """
    font_dic_list = [
        {"id": "&#57808;", "uni": "uniE1D0", "num": "7"},
        {"id": "&#58149;", "uni": "uniE325", "num": "4"},
        {"id": "&#58397;", "uni": "uniE41D", "num": "1"},
        {"id": "&#58585;", "uni": "uniE4D9", "num": ""},
        {"id": "&#58670;", "uni": "uniE52E", "num": "9"},
        {"id": "&#58928;", "uni": "uniE630", "num": "2"},
        {"id": "&#59246;", "uni": "uniE76E", "num": "8"},
        {"id": "&#59537;", "uni": "uniE891", "num": "5"},
        {"id": "&#59854;", "uni": "uniE9CE", "num": "0"},
        {"id": "&#60146;", "uni": "uniEAF2", "num": "3"},
        {"id": "&#60492;", "uni": "uniEC4C", "num": "6"},
        {"id": "&#63426;", "uni": "uniF7C2", "num": ""},
        {"id": "&#63626;", "uni": "uniF88A", "num": "7"},
    ]

    for font_dic in font_dic_list:
        if font_dic["uni"] == key:
            return font_dic["id"]


def font_map(font_path):
    font_new = TTFont(font_path)
    # 获取所有unicode编码信息
    uni_new_list = font_new.getGlyphOrder()[2:]

    font_lis = []
    for new_uni in uni_new_list:
        # 获取字体对应的字型对象
        obj_uni = font_new["glyf"][new_uni]
        # 循环我们之前保存的映射关系uni_cmap[("字形对象",数字),]
        for obj in base_font_object_list():
            # 判断新下载的字形对象与uni_cmap中的字形对象是否相同
            if obj[0] == obj_uni:
                if base_font_cmap(new_uni):
                    font_lis.append({"id": base_font_cmap(new_uni), "num": obj[1]})

    return font_lis


if __name__ == "__main__":
    # 1.4
    test_str = "&#58397;.&#60492;"
    font_list = font_map("../file/font/gzfont2.woff2", )
    print(font_list)
    for font in font_list:
        test_str = test_str.replace(font["id"], font["num"])
    print(test_str)
