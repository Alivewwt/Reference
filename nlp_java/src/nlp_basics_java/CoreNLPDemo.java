package nlp_basics_java;

import java.util.List;

import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.trees.TypedDependency;

/*
 * 注释是保存注释器结果的数据结构。注释基本上是从注释的键到位的映射，例如解析，词性标记或命名实体标记
 */
public class CoreNLPDemo {
	private static String parserModel = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
	private static LexicalizedParser lp = LexicalizedParser.loadModel(parserModel);
	//待分析文本
	public static String str="The program was in disarray and the coach was one poorly executed plane trip away from being fired by a booster.";
	
	//程序入口函数
	public static void main(String[] args) {
		
		//CoreNLP.annotation_one();
		//CoreNLP.annotation_two();
		//处理中文
		CoreNLP.annotation_ch();
		//依存句法分析  支配词(gov) 从属词(dep)
		List<TypedDependency> tdl = CoreNLP.parser(lp,str);
		
	}

	
	
}
