from pypinyin import lazy_pinyin


def transfer_chinese_words_to_pinyins(chinese_words):

    pinyins = ''.join(lazy_pinyin(chinese_words))

    pinyins_with_underline = ''
    for char in pinyins:
        pinyins_with_underline += char if char.isalnum() else '_'

    return pinyins_with_underline


if __name__ == '__main__':
    assert transfer_chinese_words_to_pinyins('你好') == 'nihao'
    assert transfer_chinese_words_to_pinyins('你好！') == 'nihao_'
    assert transfer_chinese_words_to_pinyins('你好!') == 'nihao_'
    assert transfer_chinese_words_to_pinyins('你好32') == 'nihao32'
    assert transfer_chinese_words_to_pinyins('铬(Cr)') == 'ge_Cr_'

    print('Pass!')
