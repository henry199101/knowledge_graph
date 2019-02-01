from pypinyin import lazy_pinyin


def chinese_words2pinyins(chinese_words):

    pinyins = ''

    for pinyin in lazy_pinyin(chinese_words):
        better_pinyin = ''
        for char in pinyin:
            better_pinyin += char if char.isalnum() else '_'

        pinyins += better_pinyin

    return pinyins


if __name__ == '__main__':
    assert chinese_words2pinyins('你好') == 'nihao'
    assert chinese_words2pinyins('你好！') == 'nihao_'
    assert chinese_words2pinyins('你好!') == 'nihao_'
    assert chinese_words2pinyins('你好32') == 'nihao32'
    assert chinese_words2pinyins('铬(Cr)') == 'ge_Cr_'
    print('Pass!')
