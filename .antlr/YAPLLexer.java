// Generated from c:\Users\Usuario\Desktop\8vo. Semestre UVG 2023\Compiladores\UVG_CC_Yapl_Compiler\YAPL.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class YAPLLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		WS=18, CLASS_N=19, NOT=20, ISVOID=21, IF=22, FI=23, THEN=24, ELSE=25, 
		WHILE=26, LET=27, IN=28, INHERITS=29, LOOP=30, POOL=31, NEW=32, TRUE=33, 
		FALSE=34, STRING=35, INT=36, TYPE=37, ID=38, ASSIGNMENT=39;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "T__16", 
			"WS", "CLASS_N", "NOT", "ISVOID", "IF", "FI", "THEN", "ELSE", "WHILE", 
			"LET", "IN", "INHERITS", "LOOP", "POOL", "NEW", "TRUE", "FALSE", "STRING", 
			"INT", "TYPE", "ID", "ASSIGNMENT", "ESC", "UNICODE", "HEX"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "';'", "'{'", "'}'", "'('", "','", "')'", "':'", "'@'", "'.'", 
			"'~'", "'*'", "'/'", "'+'", "'-'", "'<='", "'<'", "'='", null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, "'<-'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, "WS", "CLASS_N", "NOT", "ISVOID", 
			"IF", "FI", "THEN", "ELSE", "WHILE", "LET", "IN", "INHERITS", "LOOP", 
			"POOL", "NEW", "TRUE", "FALSE", "STRING", "INT", "TYPE", "ID", "ASSIGNMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public YAPLLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "YAPL.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2)\u00ff\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\3"+
		"\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n"+
		"\3\13\3\13\3\f\3\f\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20\3\20\3\21\3\21"+
		"\3\22\3\22\3\23\6\23|\n\23\r\23\16\23}\3\23\3\23\3\24\3\24\3\24\3\24\3"+
		"\24\3\24\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26\3\26\3\26\3\26\3\27\3"+
		"\27\3\27\3\30\3\30\3\30\3\31\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3"+
		"\32\3\33\3\33\3\33\3\33\3\33\3\33\3\34\3\34\3\34\3\34\3\35\3\35\3\35\3"+
		"\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\36\3\37\3\37\3\37\3\37\3\37\3"+
		" \3 \3 \3 \3 \3!\3!\3!\3!\3\"\3\"\3\"\3\"\3\"\3#\3#\3#\3#\3#\3#\3$\3$"+
		"\3$\7$\u00d5\n$\f$\16$\u00d8\13$\3$\3$\3%\6%\u00dd\n%\r%\16%\u00de\3&"+
		"\3&\7&\u00e3\n&\f&\16&\u00e6\13&\3\'\3\'\7\'\u00ea\n\'\f\'\16\'\u00ed"+
		"\13\'\3(\3(\3(\3)\3)\3)\3)\5)\u00f6\n)\3*\3*\3*\3*\3*\3*\3+\3+\2\2,\3"+
		"\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37"+
		"\21!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36;\37="+
		" ?!A\"C#E$G%I&K\'M(O)Q\2S\2U\2\3\2\33\5\2\13\f\16\17\"\"\4\2EEee\4\2N"+
		"Nnn\4\2CCcc\4\2UUuu\4\2PPpp\4\2QQqq\4\2VVvv\4\2KKkk\4\2XXxx\4\2FFff\4"+
		"\2HHhh\4\2JJjj\4\2GGgg\4\2YYyy\4\2TTtt\4\2RRrr\4\2WWww\4\2$$^^\3\2\62"+
		";\3\2C\\\6\2\62;C\\aac|\3\2c|\b\2\61\61ddhhppttvv\5\2\62;CHch\2\u0103"+
		"\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2"+
		"\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2"+
		"\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2"+
		"\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2"+
		"\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3"+
		"\2\2\2\2=\3\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2"+
		"\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\3W\3\2\2\2\5Y\3\2\2\2\7"+
		"[\3\2\2\2\t]\3\2\2\2\13_\3\2\2\2\ra\3\2\2\2\17c\3\2\2\2\21e\3\2\2\2\23"+
		"g\3\2\2\2\25i\3\2\2\2\27k\3\2\2\2\31m\3\2\2\2\33o\3\2\2\2\35q\3\2\2\2"+
		"\37s\3\2\2\2!v\3\2\2\2#x\3\2\2\2%{\3\2\2\2\'\u0081\3\2\2\2)\u0087\3\2"+
		"\2\2+\u008b\3\2\2\2-\u0092\3\2\2\2/\u0095\3\2\2\2\61\u0098\3\2\2\2\63"+
		"\u009d\3\2\2\2\65\u00a2\3\2\2\2\67\u00a8\3\2\2\29\u00ac\3\2\2\2;\u00af"+
		"\3\2\2\2=\u00b8\3\2\2\2?\u00bd\3\2\2\2A\u00c2\3\2\2\2C\u00c6\3\2\2\2E"+
		"\u00cb\3\2\2\2G\u00d1\3\2\2\2I\u00dc\3\2\2\2K\u00e0\3\2\2\2M\u00e7\3\2"+
		"\2\2O\u00ee\3\2\2\2Q\u00f1\3\2\2\2S\u00f7\3\2\2\2U\u00fd\3\2\2\2WX\7="+
		"\2\2X\4\3\2\2\2YZ\7}\2\2Z\6\3\2\2\2[\\\7\177\2\2\\\b\3\2\2\2]^\7*\2\2"+
		"^\n\3\2\2\2_`\7.\2\2`\f\3\2\2\2ab\7+\2\2b\16\3\2\2\2cd\7<\2\2d\20\3\2"+
		"\2\2ef\7B\2\2f\22\3\2\2\2gh\7\60\2\2h\24\3\2\2\2ij\7\u0080\2\2j\26\3\2"+
		"\2\2kl\7,\2\2l\30\3\2\2\2mn\7\61\2\2n\32\3\2\2\2op\7-\2\2p\34\3\2\2\2"+
		"qr\7/\2\2r\36\3\2\2\2st\7>\2\2tu\7?\2\2u \3\2\2\2vw\7>\2\2w\"\3\2\2\2"+
		"xy\7?\2\2y$\3\2\2\2z|\t\2\2\2{z\3\2\2\2|}\3\2\2\2}{\3\2\2\2}~\3\2\2\2"+
		"~\177\3\2\2\2\177\u0080\b\23\2\2\u0080&\3\2\2\2\u0081\u0082\t\3\2\2\u0082"+
		"\u0083\t\4\2\2\u0083\u0084\t\5\2\2\u0084\u0085\t\6\2\2\u0085\u0086\t\6"+
		"\2\2\u0086(\3\2\2\2\u0087\u0088\t\7\2\2\u0088\u0089\t\b\2\2\u0089\u008a"+
		"\t\t\2\2\u008a*\3\2\2\2\u008b\u008c\t\n\2\2\u008c\u008d\t\6\2\2\u008d"+
		"\u008e\t\13\2\2\u008e\u008f\t\b\2\2\u008f\u0090\t\n\2\2\u0090\u0091\t"+
		"\f\2\2\u0091,\3\2\2\2\u0092\u0093\t\n\2\2\u0093\u0094\t\r\2\2\u0094.\3"+
		"\2\2\2\u0095\u0096\t\r\2\2\u0096\u0097\t\n\2\2\u0097\60\3\2\2\2\u0098"+
		"\u0099\t\t\2\2\u0099\u009a\t\16\2\2\u009a\u009b\t\17\2\2\u009b\u009c\t"+
		"\7\2\2\u009c\62\3\2\2\2\u009d\u009e\t\17\2\2\u009e\u009f\t\4\2\2\u009f"+
		"\u00a0\t\6\2\2\u00a0\u00a1\t\17\2\2\u00a1\64\3\2\2\2\u00a2\u00a3\t\20"+
		"\2\2\u00a3\u00a4\t\16\2\2\u00a4\u00a5\t\n\2\2\u00a5\u00a6\t\4\2\2\u00a6"+
		"\u00a7\t\17\2\2\u00a7\66\3\2\2\2\u00a8\u00a9\t\4\2\2\u00a9\u00aa\t\17"+
		"\2\2\u00aa\u00ab\t\t\2\2\u00ab8\3\2\2\2\u00ac\u00ad\t\n\2\2\u00ad\u00ae"+
		"\t\7\2\2\u00ae:\3\2\2\2\u00af\u00b0\t\n\2\2\u00b0\u00b1\t\7\2\2\u00b1"+
		"\u00b2\t\16\2\2\u00b2\u00b3\t\17\2\2\u00b3\u00b4\t\21\2\2\u00b4\u00b5"+
		"\t\n\2\2\u00b5\u00b6\t\t\2\2\u00b6\u00b7\t\6\2\2\u00b7<\3\2\2\2\u00b8"+
		"\u00b9\t\4\2\2\u00b9\u00ba\t\b\2\2\u00ba\u00bb\t\b\2\2\u00bb\u00bc\t\22"+
		"\2\2\u00bc>\3\2\2\2\u00bd\u00be\t\22\2\2\u00be\u00bf\t\b\2\2\u00bf\u00c0"+
		"\t\b\2\2\u00c0\u00c1\t\4\2\2\u00c1@\3\2\2\2\u00c2\u00c3\t\7\2\2\u00c3"+
		"\u00c4\t\17\2\2\u00c4\u00c5\t\20\2\2\u00c5B\3\2\2\2\u00c6\u00c7\t\t\2"+
		"\2\u00c7\u00c8\t\21\2\2\u00c8\u00c9\t\23\2\2\u00c9\u00ca\t\17\2\2\u00ca"+
		"D\3\2\2\2\u00cb\u00cc\t\r\2\2\u00cc\u00cd\t\5\2\2\u00cd\u00ce\t\4\2\2"+
		"\u00ce\u00cf\t\6\2\2\u00cf\u00d0\t\17\2\2\u00d0F\3\2\2\2\u00d1\u00d6\7"+
		"$\2\2\u00d2\u00d5\5Q)\2\u00d3\u00d5\n\24\2\2\u00d4\u00d2\3\2\2\2\u00d4"+
		"\u00d3\3\2\2\2\u00d5\u00d8\3\2\2\2\u00d6\u00d4\3\2\2\2\u00d6\u00d7\3\2"+
		"\2\2\u00d7\u00d9\3\2\2\2\u00d8\u00d6\3\2\2\2\u00d9\u00da\7$\2\2\u00da"+
		"H\3\2\2\2\u00db\u00dd\t\25\2\2\u00dc\u00db\3\2\2\2\u00dd\u00de\3\2\2\2"+
		"\u00de\u00dc\3\2\2\2\u00de\u00df\3\2\2\2\u00dfJ\3\2\2\2\u00e0\u00e4\t"+
		"\26\2\2\u00e1\u00e3\t\27\2\2\u00e2\u00e1\3\2\2\2\u00e3\u00e6\3\2\2\2\u00e4"+
		"\u00e2\3\2\2\2\u00e4\u00e5\3\2\2\2\u00e5L\3\2\2\2\u00e6\u00e4\3\2\2\2"+
		"\u00e7\u00eb\t\30\2\2\u00e8\u00ea\t\27\2\2\u00e9\u00e8\3\2\2\2\u00ea\u00ed"+
		"\3\2\2\2\u00eb\u00e9\3\2\2\2\u00eb\u00ec\3\2\2\2\u00ecN\3\2\2\2\u00ed"+
		"\u00eb\3\2\2\2\u00ee\u00ef\7>\2\2\u00ef\u00f0\7/\2\2\u00f0P\3\2\2\2\u00f1"+
		"\u00f5\7^\2\2\u00f2\u00f6\t\31\2\2\u00f3\u00f6\5S*\2\u00f4\u00f6\7$\2"+
		"\2\u00f5\u00f2\3\2\2\2\u00f5\u00f3\3\2\2\2\u00f5\u00f4\3\2\2\2\u00f6R"+
		"\3\2\2\2\u00f7\u00f8\7w\2\2\u00f8\u00f9\5U+\2\u00f9\u00fa\5U+\2\u00fa"+
		"\u00fb\5U+\2\u00fb\u00fc\5U+\2\u00fcT\3\2\2\2\u00fd\u00fe\t\32\2\2\u00fe"+
		"V\3\2\2\2\n\2}\u00d4\u00d6\u00de\u00e4\u00eb\u00f5\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}