#encoding =utf-8
import tensorflow as tf
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import json
from loader import load_datatset,batch_iter,prepare_dataset
from simModel import simModel

flags = tf.app.flags

flags.DEFINE_int("max_seq_length",251,'length for sentence')
flags.DEFINE_string("train_files","./data/train/input.txt","path for train")
flags.DEFINE_string("test_files","./data/test/input.txt",'path for test')
flags.DEFINE_string("test_labels_files",'./data/test/ground_truth.txt','path for test labels')
flags.DEFINE_float("dropout_keep_prob",0.5,'dropout rate')

FLAGS = flags.FLAGS

def create_feed_dict(model,batches,is_training):
	ab_input_id, ab_input_mask, ab_seg_ids, \
	ac_input_id, ac_input_mask, ac_seg_ids, label = batches

	feed_dict = {
		model.ab_input_ids:np.array(ab_input_id),
		model.ab_input_masks:np.array(ab_input_mask),
		model.ab_segment_ids:np.array(ab_seg_ids),
		model.ac_input_ids: np.array(ac_input_id),
		model.ac_input_masks: np.array(ac_input_mask),
		model.ac_segment_ids: np.array(ac_seg_ids),
		model.dropout_keep:1.0
	}
	if is_training:
		feed_dict[model.dropout_keep] = FLAGS.dropout_keep_prob

	return feed_dict

def train():
	data = load_datatset(1,FLAGS.train_files,flags.test_files,flags.test_labels_files)
	train_data,test_data,labels = data[0]
	logger.info("train data:{},test data:{}.,lebels:{}".format(len(train_data),
													len(test_data),len(labels)))

	text_ab,text_ac,simlabels = prepare_dataset(train_data,FLAGS.max_seq_len)

	tf_config = tf.ConfigProto()
	tf_config.gpu_options.allow_growth = True

	batches = batch_iter(text_ab,text_ac,simlabels)
	with tf.Session(config=tf_config) as sess:
		model = simModel(FLAGS.max_seq_len,2,True)
		for i in range(10):
			for batch in batches:
				feed_dict = create_feed_dict(model,batch)





