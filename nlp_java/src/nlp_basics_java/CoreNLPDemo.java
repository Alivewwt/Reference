package nlp_basics_java;

import java.util.List;

import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.trees.TypedDependency;


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
