# coding: utf-8
import os
import numpy as np
from gensim.models import word2vec

def _padding(document_list, max_len):
    """
    文長を揃えるためにmax_lenサイズに全ても文書をpaddingする
    """

    new_document_list = []
    for doc in document_list:
        pad_line = ['<pad>' for i in range(max_len - len(doc))] #全ての文書の単語数を合わせる
        new_document_list.append(doc + pad_line)
    return new_document_list

"""
word2vecのモデルまでPATH
"""
bin_filename = '..{sep}..{sep}corpus{sep}google-w2v-model{sep}GoogleNews-vectors-negative300.bin'.format(sep=os.sep)

def load_data(fname):
    
    print 'input file name:', fname

    print 'loading word2vec model...'
    model =  word2vec.Word2Vec.load_word2vec_format(bin_filename, binary=True)


    """
    文書リストを作成。
    ex) [[word, word, ... , word], [word, ... , word], ... ]
    """
    target = [] #ラベル
    source = [] #文書ベクトル
    document_list = []
    for l in open(fname, 'r').readlines():
        sample = l.strip().split(' ',  1)
        label = sample[0]
        target.append(label) #ラベル
        document_list.append(sample[1].split()) #文書ごとの単語リスト
    
    """
    読み込んだword2vec modelに定義されていない単語を<unk>に置換したい。
    """
    max_len = 0
    rev_document_list = [] # 未知語処理後のdocument list
    for doc in document_list:
        rev_doc = []
        for word in doc:
            try:
                word_vec = np.array(model[word]) #未知語の場合, KeyErrorが起きる(わざと起こす)
                rev_doc.append(word)
            except KeyError:
                rev_doc.append('<unk>') #未知語
        rev_document_list.append(rev_doc)
        #文書の最大長を求める(padding用)
        if len(rev_doc) > max_len:
            max_len = len(rev_doc)
    
    """
    文長をpaddingにより合わせる
    """
    rev_document_list = _padding(rev_document_list, max_len)


    """
    文書をベクトル化する
    """
    vector_length = len(model.seeded_vector('<unk>')) #単語の次元数 (embeddingの次元数)
    for doc in rev_document_list:
        doc_vec = []
        for word in doc:
            try:
                vec = model[word.decode('utf-8')]
            except KeyError:
                vec = model.seeded_vector(word)
            doc_vec.extend(vec)
        source.append(doc_vec)

    dataset = {}
    dataset['target'] = np.array(target)    
    dataset['source'] = np.array(source)    

    return dataset, max_len, vector_length


