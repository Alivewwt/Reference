package nlp_basics_java;

import java.io.PrintWriter;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.coref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.PropertiesUtils;

/*
 * 注释是保存注释器结果的数据结构。注释基本上是从注释的键到位的映射，例如解析，词性标记或命名实体标记
 */
public class CoreNLPDemo {
	
	//程序入口函数
	public static void main(String[] args) {
	
		annotation_one();
		annotation_two();
		annotation_ch();
	}
	
	public static void annotation_one(){
		PrintWriter out= new PrintWriter(System.out);
		// 创建一个stanfordCoreNLP 对象,可以对句子分词，词性标注，词原形，实体命名标注，句法分析，
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        String text = "Joe Smith was born in California. ";

        // 对给定的文本创建一个空Annotation对象
        Annotation document = new Annotation(text);

        pipeline.annotate(document);
        pipeline.prettyPrint(document, out);
	}
	
	public static void annotation_two(){

		StanfordCoreNLP pipeline = new StanfordCoreNLP(
			PropertiesUtils.asProperties(
				"annotators", "tokenize,ssplit,pos,lemma,parse,natlog",
				"ssplit.isOneSentence", "true",
				"parse.model", "edu/stanford/nlp/models/srparser/englishSR.ser.gz",
				"tokenize.language", "en"));

		String text = "After hearing about Joe's trip, Jane decided she might go to France one day."; 
		Annotation document = new Annotation(text);

		pipeline.annotate(document);
		// CoreMap是一种Map类型的数据结构,键值对的保存形式
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);
		
		for(CoreMap sentence: sentences) {
		  for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
		    // 文本的词
		    String word = token.get(TextAnnotation.class);
		    // 词性标签
		    String pos = token.get(PartOfSpeechAnnotation.class);
		    // 词的实体标签
		    String ne = token.get(NamedEntityTagAnnotation.class);
		    // 输出格式
		    System.out.println("word\t"+word+"\tpos\t"+pos+"\tner\t"+ne);
		  }
		  
		  // 对当前句进行句法树分析
		  Tree tree = sentence.get(TreeAnnotation.class);
		  System.out.println("tree\n"+tree);
		  // 对当前句进行依存关系分析
		  SemanticGraph dependencies = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation.class);

		  System.out.println("dependencies \n"+dependencies);
		}

		Map<Integer, CorefChain> graph = document.get(CorefChainAnnotation.class);

//		for (Map.Entry<Integer, CorefChain> entry: graph.entrySet()){
//			System.out.println("key = "+entry.getKey()+", value = "+entry.getValue());
//		}
	}
	
	public static void annotation_ch(){
		 String props="StanfordCoreNLP-chinese.properties";
	     StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
	     Annotation annotation = new Annotation("欢迎使用使用斯坦福大学自然语言处理工具包！");

	     pipeline.annotate(annotation);
	     pipeline.prettyPrint(annotation, System.out);

	}
}
