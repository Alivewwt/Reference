#encoding =utf-8
import tensorflow as tf
import numpy as np
from tensorflow.contrib.crf import crf_log_likelihood
from tensorflow.contrib.crf import viterbi_decode
import tensorflow.contrib.layers as layers
from tensorflow.contrib import rnn


class Model(object):
     def __init__(self,config):
         print(config)
         self.config = config
         self.lr = config["lr"]
         self.char_dim = config["char_dim"]

         self.lstm_dim = config["lstm_dim"]
         self.seg_dim = config["seg_dim"]
         self.subtype_dim = config["subtype_dim"]
         self.num_tags = config["num_tags"]
         self.num_chars = config["num_char"]
         self.num_steps = config["num_steps"]
         self.num_segs = 14
         self.num_subtypes = 51
         self.seq_nums = 8
         self.multi_hop = 4

         self.global_step = tf.Variable(0,trainable=False)
         self.best_dev_f1 =  tf.Variable(0.0,trainable=False)
         self.best_test_f1 = tf.Variable(0.0,trainable=False)
         self.initiaizer = layers.xavier_initializer()

         self.char_inputs = tf.placeholder(dtype=tf.int32,
                                           shape=[None, None],
                                           name="ChatInputs")
         self.seg_inputs = tf.placeholder(dtype=tf.int32,
                                          shape=[None, None],
                                          name="SegInputs")
         self.subtype_inputs = tf.placeholder(dtype=tf.int32,
                                              shape=[None, None],
                                              name="SubInputs")
         self.targets = tf.placeholder(dtype=tf.int32,
                                       shape=[None, None],
                                       name="Targets")

         self.doc_inputs = tf.placeholder(dtype=tf.int32,
                                          shape=[None, None, self.num_steps],
                                          name="doc_inputs")
         self.dropout = tf.placeholder(dtype=tf.float32, name="Dropout")

         self.char_lookup = tf.get_variable(
             name="char_embedding",
             shape=[self.num_chars, self.char_dim],
             initializer=self.initiaizer)


         used =tf.sign(tf.abs(self.char_inputs))
         length = tf.reduce_sum(used,reduction_indices=1)
         self.length = tf.cast(length,tf.int32)
         self.batch_size = tf.shape(self.char_inputs)[0]

         self.embedding = self.embedding_layer(self.char_inputs, self.seg_inputs,
                                          self.subtype_inputs, config)
         self.doc_emebedding = self.doc_embedding_layer(self.doc_inputs, self.lstm_dim,
                                          self.length, config)

     def embedding_layer(self, char_inputs, seg_inputs, subtype_inputs, config, name=None):
         embedding = []
         with tf.variable_scope("char_embedding" if not name else name), tf.device('/cpu:0'):
             embedding.append(tf.nn.embedding_lookup(self.char_lookup, char_inputs))
             if config["seg_dim"]:
                 with tf.variable_scope("seg_embedding"), tf.device('/cpu:0'):
                     self.seg_lookup = tf.get_variable(
                         name="seg_embedding",
                         shape=[self.num_segs, self.seg_dim],
                         initializer=self.initiaizer)
                     embedding.append(tf.nn.embedding_lookup(self.seg_lookup, seg_inputs))
             if config["subtype_dim"]:
                 with tf.variable_scope("subtype_embedding"), tf.device('/cpu:0'):
                     self.subtype_lookup = tf.get_variable(
                         name="subtype_embedding",
                         shape=[self.num_subtypes, self.subtype_dim],
                         initializer=self.initiaizer)
                     embedding.append(tf.nn.embedding_lookup(self.subtype_lookup, subtype_inputs))
             embed = tf.concat(embedding, axis=-1)
         return embed

     def doc_embedding_layer(self,doc_inputs,lstm_dim,lengths,config,name=None):

         def doc_LSTM_layer(inputs,lstm_dim,lengths):
             with tf.variable_scope("doc_BiLSTM",reuse=tf.AUTO_REUSE):
                 lstm_cell = {}
                 for direction in ["doc_forward","doc_backward"]:
                     with tf.variable_scope(direction):
                         lstm_cell[direction] = rnn.CoupledInputForgetGateLSTMCell(
                             lstm_dim,
                             use_peepholes=True,
                             initializer = self.initiaizer,
                             reuse=tf.AUTO_REUSE,
                             state_is_tuple=True
                         )
                 (outputs,
                  (encoder_fw_final_state,encoder_bw_final_state))=tf.nn.bidirectional_dynamic_rnn(
                     lstm_cell["doc_forward"],
                     lstm_cell["doc_backward"],
                     inputs,
                     dtype=tf.float32,
                     sequence_length = lengths
                  )
                 final_state = tf.concat((encoder_bw_final_state.h,encoder_fw_final_state.h),-1)
                 return final_state

         lstm_states = []
         doc_inputs =  tf.reshape(doc_inputs,[self.batch_size,self.seq_nums,self.num_steps])
         doc_input = tf.unstack(tf.transpose(doc_inputs,[1,0,2]),axis=0)
         for i in range(self.seq_nums):
             with tf.variable_scope("doc_embdding",reuse=tf.AUTO_REUSE),tf.device("/cpu:0"):
                 self.char_doc_lookup = tf.get_variable(
                     name="doc_emebdding",
                     shape=[self.num_chars,self.char_dim],
                     initializer=self.initiaizer
                 )
                 doc_embedding = (tf.nn.embedding_lookup(self.char_doc_lookup,doc_input[i]))
             lstm_state = doc_LSTM_layer(doc_embedding,lstm_dim,lengths)
             lstm_states.append(lstm_state)
         last_states = tf.transpose(lstm_states,[1,0,2])
         last_states = tf.reshape(last_states,[self.batch_size,self.seq_nums,self.lstm_dim*2])
         return last_states


if __name__ == '__main__':

     '''
     self.char_dim = config["char_dim"]

     self.lstm_dim = config["lstm_dim"]
     self.seg_dim = config["seg_dim"]
     self.subtype_dim = config["subtype_dim"]
     self.num_tags = config["num_tags"]
     self.num_chars = config["num_char"]
     self.num_steps = config["num_steps"]
     '''
     config = {}
     config["lr"] = 0.001
     config["char_dim"] = 100
     config["lstm_dim"] = 200
     config["seg_dim"] = 20
     config["subtype_dim"] = 20
     config["num_tags"] = 15
     config["num_char"] = 26
     config["num_steps"] = 40 #num_step #seq_size(seq_nums) 8

     # char_inputs = tf.Variable(np.reshape(np.arange(160),[4,40]))#batch_size,seq_length
     # doc_inputs = tf.Variable(np.reshape(np.arange(1280),[4,8,40]))
     # seg_inputs = tf.Variable(np.reshape(np.arange(160),[4,40]))
     # subtype_inputs = tf.Variable(np.reshape(np.arange(160),[4,40]))
     # targets =  tf.Variable(np.reshape(np.arange(160),[4,40]))

     char_inputs = np.random.randint(0,26,(4,40))#batch_size,seq_num
     doc_inputs = np.random.randint(0,26,(4,8,40))#batch_size seq_num,num_steps
     seg_inputs = np.random.randint(0,14,(4,40)) #14
     subtype_inputs = np.random.randint(0,51,(4,40)) #51
     targets =  np.random.randint(0,15,(4,40))

     print(char_inputs)
     print("===========分割线========")
     print(doc_inputs)
     with tf.Session() as sess:
        model = Model(config)
        sess.run(tf.global_variables_initializer())
        feed_dict = {model.char_inputs: char_inputs,
                     model.doc_inputs: doc_inputs,
                     model.seg_inputs: seg_inputs,
                     model.subtype_inputs: subtype_inputs,
                     model.targets: targets
                     }
        embedding, doc_emebedding= sess.run([model.embedding,model.doc_emebedding],
            feed_dict=feed_dict)
        print(embedding)
        print(doc_emebedding.shape)
        for v in tf.trainable_variables():
            print(v)

