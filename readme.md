stanford corenlp的源代码是使用java写的，提供了server方式进行交互。 stanfordcorenlp是一个对Stanford CoreNLP进行了封装的Python工具包，使用起来非常方便。

安装stanfordcorenlp包之前：

1.下载安装JDK1.8及以上版本。

2.下载Stanford CoreNLP文件，解压。

3.处理中文还需要下载中文的模型jar文件，然后放到stanford-corenlp-2017-06-09根目录。

process_one的输出

#Tokenize

['which', 'you', 'step', 'on', 'to', 'activate', 'it']

# part of speech



[('which', 'WDT'), ('you', 'PRP'), ('step', 'VB'), ('on', 'IN'), ('to', 'TO'), ('activate', 'VB'), ('it', 'PRP')]

#Named Entities

[('which', 'O'), ('you', 'O'), ('step', 'O'), ('on', 'O'), ('to', 'O'), ('activate', 'O'), ('it', 'O')]

# Constituency Parsing



    (ROOT
      (SBAR
    (WHNP (WDT which))
    (S
      (NP (PRP you))
      (VP (VB step)
        (ADVP (IN on))
        (S
          (VP (TO to)
            (VP (VB activate)
              (NP (PRP it)))))))))
# Dependency Parsing



[('ROOT', 0, 3), ('dobj', 3, 1), ('nsubj', 3, 2), ('mark', 6, 4), ('mark', 6, 5), ('advcl', 3, 6), ('dobj', 6, 7)]



