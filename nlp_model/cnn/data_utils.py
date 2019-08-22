#! -*- coding: utf-8 -*-
import numpy as np
import json,re,os,pickle
from gensim.models import KeyedVectors

embeddingspath = "../Word2Vec/GoogleNews-vectors-negative300.bin"


def clean_str(string):
	"""
	Tokenization/string cleaning for all datasets except for SST.
	Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
	"""
	string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
	string = re.sub(r"\'s", " \'s", string)
	string = re.sub(r"\'ve", " \'ve", string)
	string = re.sub(r"n\'t", " n\'t", string)
	string = re.sub(r"\'re", " \'re", string)
	string = re.sub(r"\'d", " \'d", string)
	string = re.sub(r"\'ll", " \'ll", string)
	string = re.sub(r",", " , ", string)
	string = re.sub(r"!", " ! ", string)
	string = re.sub(r"\(", " \( ", string)
	string = re.sub(r"\)", " \) ", string)
	string = re.sub(r"\?", " \? ", string)
	string = re.sub(r"\s{2,}", " ", string)
	return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
	# Load data from files
	positive_examples = list(open(positive_data_file, "r", encoding='utf-8',errors='ignore').readlines())
	positive_examples = [s.strip() for s in positive_examples]
	negative_examples = list(open(negative_data_file, "r", encoding='utf-8',errors='ignore').readlines())
	negative_examples = [s.strip() for s in negative_examples]
	# Split by words
	x_text = positive_examples + negative_examples
	x_text = [clean_str(sent) for sent in x_text]
	#x_text = [s.split(" ") for s in x_text]
    # Generate labels
	positive_labels = [0 for _ in positive_examples]
	negative_labels = [1 for _ in negative_examples]
	y = np.concatenate([positive_labels, negative_labels], 0)
	return [x_text, y]

#数据对齐
def pad_sentences(sentences,padding_word="pad"):
	seq_length = max[len(x.split(" ")) for x in sentences]
	print("max seq_length",seq_length)
	padded_sentence = []
	for i,sen in enumerate(sentences):
		x = sen.split(" ")
		num_padding =seq_length-len(sen.split())
		new_sen = x+[padding_word]*num_padding
		padded_sentence.append(new_sen)
	return padded_sentence

#获得文本的所有词,建立字典
def build_vocab(sentences):
	#词典
	vocabs = {}
	if not os.path.exists('./all_chars_me.json'):
		for i,sen in enumerate(sentences):
			for word in sen.split(" "):
				vocabs[word] = vocabs.get(word,0)+1
		id2word = {i+2:j for i,j in enumerate(vocabs)} # 0: mask, 1: padding
		id2word[0] = 'mask'
		id2word[1] = 'pad'
		word2id = {j:i for i,j in id2word.items()}
		json.dump([id2word, word2id], open('./all_word_me.json', 'w'))
	
	else:
		id2word,word2id = json.load(open('./all_word_me.json','r'))

	return word2id,id2word

def build_input(sentences,label,vocabs):
	data = [] 
	for sen in sentences:
		x = [vocabs[word if word in vocabs else "pad"]for word in sen]
		data.append(x)
	np.array(data,dtype='int32')
	y = np.array(label,dtype='int32')
	return data,y

def load_wv(id2word):
	#加载向量
	c_found = 0
	c_lower = 0
	c_zeros = 0
	n_words = len(id2word)
	pre_trained = KeyedVectors.load_word2vec_format(embeddingspath,binary=True,unicode_errors='ignore')
	wordEmbeddings = np.zeros((len(id2word),300));
	for idx,word in id2word.items():
		if(idx==0):
			wordEmbeddings[idx] = np.random.uniform(-1,1,300)
		if(idx==1):
			wordEmbeddings[idx] = np.zeros(300)
		if word in pre_trained:
			wordEmbeddings[idx] = pre_trained[word]
			c_found+=1
		elif word.lower() in pre_trained:
			wordEmbeddings[idx] = pre_trained[word.lower()]
			c_lower+=1
		elif re.sub('\d','0',word.lower()) in pre_trained:
			wordEmbeddings[idx] = pre_trained[re.sub('\d','0',word.lower())]
			c_zeros+=1
	print("%i found directly, %i after lowercasing, %i after lowercasing + zero." %(c_found,c_lower,c_zeros))
	return wordEmbeddings


if __name__ == '__main__':
	data_folder = ["./data/rt-polarity.pos","./data/rt-polarity.neg"]
	data = load_data_and_labels(data_folder[0],data_folder[1])
	sentences = data[0]
	labels = data[1]
	word2id,id2word = build_vocab(sentences)
	print('word index',len(word2id))
	padd_sentences = pad_sentences(sentences)
	wordEmbeddings = load_wv(id2word)
	x,y = build_input(padd_sentences,labels,word2id)

	data = {"wordEmbeddings":wordEmbeddings,"sen":x,"labels":y}
	pickle.dump(data,open('./data/data.bin','wb'))
