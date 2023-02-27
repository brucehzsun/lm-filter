# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from src.utils import en_dict_util as en_dict
from src.lm import wk_zh_2019_filter as wk

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    dict_path = 'cet4_dict.txt'
    en_dict: dict = en_dict.read_en_dict(dict_path)

    corpus_list = ['i am teacher', '1.面积147km²好大呀',
                   '２.王双骏现时的妻子为电子音乐组合PixelToy前主音胡咏丝Candy',
                   '３．推出志云饭局 Live on Stage舞台剧',
                   '使得该党下议院席次增至18席',
                   '特科斯卡在2011年2月表示',
                   '并且于2015年3月31日在美服举行测试', '初版剪辑版本长达3小时',
                   '其中有30分钟围绕在美国队长如何从冰封解冻与认知所处的现今世界',
                   "我的电话号码是18601291823可以打这个电话",
                   "公司的电话是0571-26888999",
                   "18601291823",
                   "客服电话400-1130099",
                   "Rokid Air联系电话是4001130099",
                   "苹果手机售价9989元,小米手机售价2999元",
                   "1.筑后史谈会／编，《筑后人物便覧》，福冈県文化会馆、筑后史谈会　昭和１０年刊の复制，１９３５年：10页", "位于国徽下部的是国名阿富汗افغانستان与阿拉伯数字一二九八١٢٩٨",
                   '正规化子的名字来源于如果我们令 < S > 为一个由S生成的子群',
                   '则 < p q > 还生成整数集在加法下的群根据贝祖等式',
                   '<is gemaak> 意 味 著 某 事 已 经 被 完 成 且 今 天 仍 然 存 在 著',
                   '矩震级高达8.1,震源深度15千米',
                   '关东大地震死亡人数估计大约介于100,000至142,000人',
                   '日本时间12时1分与3分又分别发生规模7.3与7.2的余震'
                   ]

    result = [
        '面 积 一 百 四 十 七 平 方 米 好 大 呀',
        '王 双 骏 现 时 的 妻 子 为 电 子 音 乐 组 合 前 主 音 胡 咏 丝 Candy',
        '推 出 志 云 饭 局 Live on Stage 舞 台 剧',
        '使 得 该 党 下 议 院 席 次 增 至 十 八 席',
        '特 科 斯 卡 在 二 零 一 一 年 二 月 表 示',
        '并 且 于 二 零 一 五 年 三 月 三 十 一 日 在 美 服 举 行 测 试',
        '初 版 剪 辑 版 本 长 达 三 小 时',
        '其 中 有 三 十 分 钟 围 绕 在 美 国 队 长 如 何 从 冰 封 解 冻 与 认 知 所 处 的 现 今 世 界',
        '我 的 电 话 号 码 是 一 八 六 零 一 二 九 一 八 二 三 可 以 打 这 个 电 话',
        '公 司 的 电 话 是 零 五 七 一 二 六 八 八 八 九 九 九',
        '客 服 电 话 四 零 零 一 一 三 零 零 九 九',
        'Air 联 系 电 话 是 四 零 零 一 一 三 零 零 九 十 九',
        '苹 果 手 机 售 价 九 千 九 百 八 十 九 元',
        '小 米 手 机 售 价 二 千 九 百 九 十 九 元',
        '筑 后 史 谈 会',
        '筑 后 人 物 便 覧',
        '福 冈 県 文 化 会 馆',
        '筑 后 史 谈 会 昭 和 一 零 年 刊 复 制',
        '一 九 三 五 年',
        '十 页',
        '位 于 国 徽 下 部 的 是 国 名 阿 富 汗 与 阿 拉 伯 数 字 一 二 九 八',
        '正 规 化 子 的 名 字 来 源 于 如 果 我 们 令 S 为 一 个 由 S 生 成 的 子 群',
        '则 p q 还 生 成 整 数 集 在 加 法 下 的 群 根 据 贝 祖 等 式',
        'is 意 味 著 某 事 已 经 被 完 成 且 今 天 仍 然 存 在 著',
        '矩 震 级 高 达 八 点 一',
        '震 源 深 度 十 五 千 米',
        '关 东 大 地 震 死 亡 人 数 估 计 大 约 介 于 十 万 至 十 四 万 二 千 人',
        '日 本 时 间 十 二 时 一 分 与 三 分 又 分 别 发 生 规 模 七 点 三 与 七 点 二 的 余 震',
    ]

    results = []
    for corpus in corpus_list:
        text_list, raw_data = wk.filter_raw_text(corpus, en_dict)
        for text in text_list:
            results.append(text)

    for i, text in enumerate(results):
        ret = result[i]
        if text != ret:
            print(f"出现错误，text={text}")
            exit(-1)
    print("=========全部正确==========")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
