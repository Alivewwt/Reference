from stanfordcorenlp import StanfordCoreNLP
import requests,json

nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2017-06-09/')

#简单处理模式
def process_one():
	#待处理的句子
	sentence = 'which you step on to activate it'
	#分词
	print(nlp.word_tokenize(sentence)) 
	#词形标注
	print(nlp.pos_tag(sentence))
	#命名实体识别
	print(nlp.ner(sentence))
	#句法树分析
	print(nlp.parse(sentence))
	#依存句法分析
	print(nlp.dependency_parse(sentence))
	#记得及时关闭，否则非常耗费资源


#在python环境下还可以使用请求服务的形式，调用stanford corenlp，返回json格式
#首先要启动server服务，假设在windows下，首先打开cmd命令窗口，进入到stanford-corenlp-full-2017-06-09的目录下，
#输入一下命令 java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
#服务开启后，才可以调用方法
def process_two():
	#文章分句，每个词都有起始位置 加入依存句法分析
	#doc 一般为处理后的文章（多个句子，通常是一篇短文）
	rq=requests.post('http://localhost:9000?properties={"annotators":"tokenize,ssplit,parser","outputFormat":"json"}',
		data=doc)
	parsed_json = json.loads(rq.text)
	#print(parsed_json)
	sentences=parsed_json['sentences']
	#遍历每一个句子
	for sentence in sentences:
		tokens=sentence['tokens']
		dependency=sentence['basicDependencies']
		for token,dep in zip(tokens,dependency):
			#原文中起始位置
			start=token['characterOffsetBegin']
			end=token['characterOffsetEnd']
			#word
			word=token['originalText']
			gover,g_index,depen,d_index=dep['governorGloss'],dep['governor'],dep['dependentGloss'],dep['dependent']
			re=dep['dep']
			print(word,start,end)
			print(gover,depen,re)


if __name__ == '__main__':
	process_one()
	process_two()
	nlp.close()


