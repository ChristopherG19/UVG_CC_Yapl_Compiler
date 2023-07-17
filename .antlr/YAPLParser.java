// Generated from c:\Users\Usuario\Desktop\8vo. Semestre UVG 2023\Compiladores\UVG_CC_Yapl_Compiler\YAPL.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class YAPLParser extends Parser {
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
	public static final int
		RULE_prog = 0, RULE_class_def = 1, RULE_feature = 2, RULE_formal = 3, 
		RULE_expr = 4;
	private static String[] makeRuleNames() {
		return new String[] {
			"prog", "class_def", "feature", "formal", "expr"
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

	@Override
	public String getGrammarFileName() { return "YAPL.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public YAPLParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class ProgContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(YAPLParser.EOF, 0); }
		public List<Class_defContext> class_def() {
			return getRuleContexts(Class_defContext.class);
		}
		public Class_defContext class_def(int i) {
			return getRuleContext(Class_defContext.class,i);
		}
		public ProgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prog; }
	}

	public final ProgContext prog() throws RecognitionException {
		ProgContext _localctx = new ProgContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_prog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(13); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(10);
				class_def();
				setState(11);
				match(T__0);
				}
				}
				setState(15); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==CLASS_N );
			setState(17);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Class_defContext extends ParserRuleContext {
		public TerminalNode CLASS_N() { return getToken(YAPLParser.CLASS_N, 0); }
		public List<TerminalNode> TYPE() { return getTokens(YAPLParser.TYPE); }
		public TerminalNode TYPE(int i) {
			return getToken(YAPLParser.TYPE, i);
		}
		public TerminalNode INHERITS() { return getToken(YAPLParser.INHERITS, 0); }
		public List<FeatureContext> feature() {
			return getRuleContexts(FeatureContext.class);
		}
		public FeatureContext feature(int i) {
			return getRuleContext(FeatureContext.class,i);
		}
		public Class_defContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_class_def; }
	}

	public final Class_defContext class_def() throws RecognitionException {
		Class_defContext _localctx = new Class_defContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_class_def);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(19);
			match(CLASS_N);
			setState(20);
			match(TYPE);
			setState(23);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==INHERITS) {
				{
				setState(21);
				match(INHERITS);
				setState(22);
				match(TYPE);
				}
			}

			setState(25);
			match(T__1);
			setState(31);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==ID) {
				{
				{
				setState(26);
				feature();
				setState(27);
				match(T__0);
				}
				}
				setState(33);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(34);
			match(T__2);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class FeatureContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(YAPLParser.ID, 0); }
		public TerminalNode TYPE() { return getToken(YAPLParser.TYPE, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public List<FormalContext> formal() {
			return getRuleContexts(FormalContext.class);
		}
		public FormalContext formal(int i) {
			return getRuleContext(FormalContext.class,i);
		}
		public TerminalNode ASSIGNMENT() { return getToken(YAPLParser.ASSIGNMENT, 0); }
		public FeatureContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_feature; }
	}

	public final FeatureContext feature() throws RecognitionException {
		FeatureContext _localctx = new FeatureContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_feature);
		int _la;
		try {
			setState(62);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(36);
				match(ID);
				setState(37);
				match(T__3);
				setState(46);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ID) {
					{
					setState(38);
					formal();
					setState(43);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__4) {
						{
						{
						setState(39);
						match(T__4);
						setState(40);
						formal();
						}
						}
						setState(45);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
				}

				setState(48);
				match(T__5);
				setState(49);
				match(T__6);
				setState(50);
				match(TYPE);
				setState(51);
				match(T__1);
				setState(52);
				expr(0);
				setState(53);
				match(T__2);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(55);
				match(ID);
				setState(56);
				match(T__6);
				setState(57);
				match(TYPE);
				setState(60);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ASSIGNMENT) {
					{
					setState(58);
					match(ASSIGNMENT);
					setState(59);
					expr(0);
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class FormalContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(YAPLParser.ID, 0); }
		public TerminalNode TYPE() { return getToken(YAPLParser.TYPE, 0); }
		public FormalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_formal; }
	}

	public final FormalContext formal() throws RecognitionException {
		FormalContext _localctx = new FormalContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_formal);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(64);
			match(ID);
			setState(65);
			match(T__6);
			setState(66);
			match(TYPE);
			setState(67);
			match(T__0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ExprContext extends ParserRuleContext {
		public Token bool;
		public Token op;
		public List<TerminalNode> ID() { return getTokens(YAPLParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(YAPLParser.ID, i);
		}
		public List<TerminalNode> ASSIGNMENT() { return getTokens(YAPLParser.ASSIGNMENT); }
		public TerminalNode ASSIGNMENT(int i) {
			return getToken(YAPLParser.ASSIGNMENT, i);
		}
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public TerminalNode IF() { return getToken(YAPLParser.IF, 0); }
		public TerminalNode THEN() { return getToken(YAPLParser.THEN, 0); }
		public TerminalNode ELSE() { return getToken(YAPLParser.ELSE, 0); }
		public TerminalNode FI() { return getToken(YAPLParser.FI, 0); }
		public TerminalNode WHILE() { return getToken(YAPLParser.WHILE, 0); }
		public TerminalNode LOOP() { return getToken(YAPLParser.LOOP, 0); }
		public TerminalNode POOL() { return getToken(YAPLParser.POOL, 0); }
		public TerminalNode LET() { return getToken(YAPLParser.LET, 0); }
		public List<TerminalNode> TYPE() { return getTokens(YAPLParser.TYPE); }
		public TerminalNode TYPE(int i) {
			return getToken(YAPLParser.TYPE, i);
		}
		public TerminalNode IN() { return getToken(YAPLParser.IN, 0); }
		public TerminalNode NEW() { return getToken(YAPLParser.NEW, 0); }
		public TerminalNode ISVOID() { return getToken(YAPLParser.ISVOID, 0); }
		public TerminalNode NOT() { return getToken(YAPLParser.NOT, 0); }
		public TerminalNode INT() { return getToken(YAPLParser.INT, 0); }
		public TerminalNode STRING() { return getToken(YAPLParser.STRING, 0); }
		public TerminalNode TRUE() { return getToken(YAPLParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(YAPLParser.FALSE, 0); }
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
	}

	public final ExprContext expr() throws RecognitionException {
		return expr(0);
	}

	private ExprContext expr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExprContext _localctx = new ExprContext(_ctx, _parentState);
		ExprContext _prevctx = _localctx;
		int _startState = 8;
		enterRecursionRule(_localctx, 8, RULE_expr, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(148);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				{
				setState(70);
				match(ID);
				setState(71);
				match(ASSIGNMENT);
				setState(72);
				expr(19);
				}
				break;
			case 2:
				{
				setState(73);
				match(ID);
				setState(74);
				match(T__3);
				{
				setState(75);
				expr(0);
				setState(80);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__4) {
					{
					{
					setState(76);
					match(T__4);
					setState(77);
					expr(0);
					}
					}
					setState(82);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
				setState(83);
				match(T__5);
				}
				break;
			case 3:
				{
				setState(85);
				match(IF);
				setState(86);
				expr(0);
				setState(87);
				match(THEN);
				setState(88);
				expr(0);
				setState(89);
				match(ELSE);
				setState(90);
				expr(0);
				setState(91);
				match(FI);
				}
				break;
			case 4:
				{
				setState(93);
				match(WHILE);
				setState(94);
				expr(0);
				setState(95);
				match(LOOP);
				setState(96);
				expr(0);
				setState(97);
				match(POOL);
				}
				break;
			case 5:
				{
				setState(99);
				match(T__1);
				setState(103); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(100);
					expr(0);
					setState(101);
					match(T__0);
					}
					}
					setState(105); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__3) | (1L << T__9) | (1L << NOT) | (1L << ISVOID) | (1L << IF) | (1L << WHILE) | (1L << LET) | (1L << NEW) | (1L << TRUE) | (1L << FALSE) | (1L << STRING) | (1L << INT) | (1L << ID))) != 0) );
				setState(107);
				match(T__2);
				}
				break;
			case 6:
				{
				setState(109);
				match(LET);
				setState(110);
				match(ID);
				setState(111);
				match(T__6);
				setState(112);
				match(TYPE);
				setState(115);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ASSIGNMENT) {
					{
					setState(113);
					match(ASSIGNMENT);
					setState(114);
					expr(0);
					}
				}

				setState(127);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__4) {
					{
					{
					setState(117);
					match(T__4);
					setState(118);
					match(ID);
					setState(119);
					match(T__6);
					setState(120);
					match(TYPE);
					setState(123);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ASSIGNMENT) {
						{
						setState(121);
						match(ASSIGNMENT);
						setState(122);
						expr(0);
						}
					}

					}
					}
					setState(129);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(130);
				match(IN);
				setState(131);
				expr(13);
				}
				break;
			case 7:
				{
				setState(132);
				match(NEW);
				setState(133);
				match(TYPE);
				}
				break;
			case 8:
				{
				setState(134);
				match(T__9);
				setState(135);
				expr(11);
				}
				break;
			case 9:
				{
				setState(136);
				match(ISVOID);
				setState(137);
				expr(10);
				}
				break;
			case 10:
				{
				setState(138);
				match(NOT);
				setState(139);
				expr(6);
				}
				break;
			case 11:
				{
				setState(140);
				match(T__3);
				setState(141);
				expr(0);
				setState(142);
				match(T__5);
				}
				break;
			case 12:
				{
				setState(144);
				match(ID);
				}
				break;
			case 13:
				{
				setState(145);
				match(INT);
				}
				break;
			case 14:
				{
				setState(146);
				match(STRING);
				}
				break;
			case 15:
				{
				setState(147);
				((ExprContext)_localctx).bool = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==TRUE || _la==FALSE) ) {
					((ExprContext)_localctx).bool = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(180);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,17,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(178);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,16,_ctx) ) {
					case 1:
						{
						_localctx = new ExprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(150);
						if (!(precpred(_ctx, 9))) throw new FailedPredicateException(this, "precpred(_ctx, 9)");
						setState(151);
						((ExprContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==T__10 || _la==T__11) ) {
							((ExprContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(152);
						expr(10);
						}
						break;
					case 2:
						{
						_localctx = new ExprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(153);
						if (!(precpred(_ctx, 8))) throw new FailedPredicateException(this, "precpred(_ctx, 8)");
						setState(154);
						((ExprContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==T__12 || _la==T__13) ) {
							((ExprContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(155);
						expr(9);
						}
						break;
					case 3:
						{
						_localctx = new ExprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(156);
						if (!(precpred(_ctx, 7))) throw new FailedPredicateException(this, "precpred(_ctx, 7)");
						setState(157);
						((ExprContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__14) | (1L << T__15) | (1L << T__16))) != 0)) ) {
							((ExprContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(158);
						expr(8);
						}
						break;
					case 4:
						{
						_localctx = new ExprContext(_parentctx, _parentState);
						pushNewRecursionContext(_localctx, _startState, RULE_expr);
						setState(159);
						if (!(precpred(_ctx, 18))) throw new FailedPredicateException(this, "precpred(_ctx, 18)");
						setState(162);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if (_la==T__7) {
							{
							setState(160);
							match(T__7);
							setState(161);
							match(TYPE);
							}
						}

						setState(164);
						match(T__8);
						setState(165);
						match(ID);
						setState(166);
						match(T__3);
						setState(175);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__3) | (1L << T__9) | (1L << NOT) | (1L << ISVOID) | (1L << IF) | (1L << WHILE) | (1L << LET) | (1L << NEW) | (1L << TRUE) | (1L << FALSE) | (1L << STRING) | (1L << INT) | (1L << ID))) != 0)) {
							{
							setState(167);
							expr(0);
							setState(172);
							_errHandler.sync(this);
							_la = _input.LA(1);
							while (_la==T__4) {
								{
								{
								setState(168);
								match(T__4);
								setState(169);
								expr(0);
								}
								}
								setState(174);
								_errHandler.sync(this);
								_la = _input.LA(1);
							}
							}
						}

						setState(177);
						match(T__5);
						}
						break;
					}
					} 
				}
				setState(182);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,17,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 4:
			return expr_sempred((ExprContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean expr_sempred(ExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 9);
		case 1:
			return precpred(_ctx, 8);
		case 2:
			return precpred(_ctx, 7);
		case 3:
			return precpred(_ctx, 18);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3)\u00ba\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\2\6\2\20\n\2\r\2\16\2\21\3\2"+
		"\3\2\3\3\3\3\3\3\3\3\5\3\32\n\3\3\3\3\3\3\3\3\3\7\3 \n\3\f\3\16\3#\13"+
		"\3\3\3\3\3\3\4\3\4\3\4\3\4\3\4\7\4,\n\4\f\4\16\4/\13\4\5\4\61\n\4\3\4"+
		"\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4?\n\4\5\4A\n\4\3\5\3\5"+
		"\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6Q\n\6\f\6\16\6T\13"+
		"\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6"+
		"\3\6\3\6\3\6\6\6j\n\6\r\6\16\6k\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6v\n"+
		"\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6~\n\6\7\6\u0080\n\6\f\6\16\6\u0083\13\6"+
		"\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3"+
		"\6\5\6\u0097\n\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6\u00a5"+
		"\n\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6\u00ad\n\6\f\6\16\6\u00b0\13\6\5\6\u00b2"+
		"\n\6\3\6\7\6\u00b5\n\6\f\6\16\6\u00b8\13\6\3\6\2\3\n\7\2\4\6\b\n\2\6\3"+
		"\2#$\3\2\r\16\3\2\17\20\3\2\21\23\2\u00d5\2\17\3\2\2\2\4\25\3\2\2\2\6"+
		"@\3\2\2\2\bB\3\2\2\2\n\u0096\3\2\2\2\f\r\5\4\3\2\r\16\7\3\2\2\16\20\3"+
		"\2\2\2\17\f\3\2\2\2\20\21\3\2\2\2\21\17\3\2\2\2\21\22\3\2\2\2\22\23\3"+
		"\2\2\2\23\24\7\2\2\3\24\3\3\2\2\2\25\26\7\25\2\2\26\31\7\'\2\2\27\30\7"+
		"\37\2\2\30\32\7\'\2\2\31\27\3\2\2\2\31\32\3\2\2\2\32\33\3\2\2\2\33!\7"+
		"\4\2\2\34\35\5\6\4\2\35\36\7\3\2\2\36 \3\2\2\2\37\34\3\2\2\2 #\3\2\2\2"+
		"!\37\3\2\2\2!\"\3\2\2\2\"$\3\2\2\2#!\3\2\2\2$%\7\5\2\2%\5\3\2\2\2&\'\7"+
		"(\2\2\'\60\7\6\2\2(-\5\b\5\2)*\7\7\2\2*,\5\b\5\2+)\3\2\2\2,/\3\2\2\2-"+
		"+\3\2\2\2-.\3\2\2\2.\61\3\2\2\2/-\3\2\2\2\60(\3\2\2\2\60\61\3\2\2\2\61"+
		"\62\3\2\2\2\62\63\7\b\2\2\63\64\7\t\2\2\64\65\7\'\2\2\65\66\7\4\2\2\66"+
		"\67\5\n\6\2\678\7\5\2\28A\3\2\2\29:\7(\2\2:;\7\t\2\2;>\7\'\2\2<=\7)\2"+
		"\2=?\5\n\6\2><\3\2\2\2>?\3\2\2\2?A\3\2\2\2@&\3\2\2\2@9\3\2\2\2A\7\3\2"+
		"\2\2BC\7(\2\2CD\7\t\2\2DE\7\'\2\2EF\7\3\2\2F\t\3\2\2\2GH\b\6\1\2HI\7("+
		"\2\2IJ\7)\2\2J\u0097\5\n\6\25KL\7(\2\2LM\7\6\2\2MR\5\n\6\2NO\7\7\2\2O"+
		"Q\5\n\6\2PN\3\2\2\2QT\3\2\2\2RP\3\2\2\2RS\3\2\2\2SU\3\2\2\2TR\3\2\2\2"+
		"UV\7\b\2\2V\u0097\3\2\2\2WX\7\30\2\2XY\5\n\6\2YZ\7\32\2\2Z[\5\n\6\2[\\"+
		"\7\33\2\2\\]\5\n\6\2]^\7\31\2\2^\u0097\3\2\2\2_`\7\34\2\2`a\5\n\6\2ab"+
		"\7 \2\2bc\5\n\6\2cd\7!\2\2d\u0097\3\2\2\2ei\7\4\2\2fg\5\n\6\2gh\7\3\2"+
		"\2hj\3\2\2\2if\3\2\2\2jk\3\2\2\2ki\3\2\2\2kl\3\2\2\2lm\3\2\2\2mn\7\5\2"+
		"\2n\u0097\3\2\2\2op\7\35\2\2pq\7(\2\2qr\7\t\2\2ru\7\'\2\2st\7)\2\2tv\5"+
		"\n\6\2us\3\2\2\2uv\3\2\2\2v\u0081\3\2\2\2wx\7\7\2\2xy\7(\2\2yz\7\t\2\2"+
		"z}\7\'\2\2{|\7)\2\2|~\5\n\6\2}{\3\2\2\2}~\3\2\2\2~\u0080\3\2\2\2\177w"+
		"\3\2\2\2\u0080\u0083\3\2\2\2\u0081\177\3\2\2\2\u0081\u0082\3\2\2\2\u0082"+
		"\u0084\3\2\2\2\u0083\u0081\3\2\2\2\u0084\u0085\7\36\2\2\u0085\u0097\5"+
		"\n\6\17\u0086\u0087\7\"\2\2\u0087\u0097\7\'\2\2\u0088\u0089\7\f\2\2\u0089"+
		"\u0097\5\n\6\r\u008a\u008b\7\27\2\2\u008b\u0097\5\n\6\f\u008c\u008d\7"+
		"\26\2\2\u008d\u0097\5\n\6\b\u008e\u008f\7\6\2\2\u008f\u0090\5\n\6\2\u0090"+
		"\u0091\7\b\2\2\u0091\u0097\3\2\2\2\u0092\u0097\7(\2\2\u0093\u0097\7&\2"+
		"\2\u0094\u0097\7%\2\2\u0095\u0097\t\2\2\2\u0096G\3\2\2\2\u0096K\3\2\2"+
		"\2\u0096W\3\2\2\2\u0096_\3\2\2\2\u0096e\3\2\2\2\u0096o\3\2\2\2\u0096\u0086"+
		"\3\2\2\2\u0096\u0088\3\2\2\2\u0096\u008a\3\2\2\2\u0096\u008c\3\2\2\2\u0096"+
		"\u008e\3\2\2\2\u0096\u0092\3\2\2\2\u0096\u0093\3\2\2\2\u0096\u0094\3\2"+
		"\2\2\u0096\u0095\3\2\2\2\u0097\u00b6\3\2\2\2\u0098\u0099\f\13\2\2\u0099"+
		"\u009a\t\3\2\2\u009a\u00b5\5\n\6\f\u009b\u009c\f\n\2\2\u009c\u009d\t\4"+
		"\2\2\u009d\u00b5\5\n\6\13\u009e\u009f\f\t\2\2\u009f\u00a0\t\5\2\2\u00a0"+
		"\u00b5\5\n\6\n\u00a1\u00a4\f\24\2\2\u00a2\u00a3\7\n\2\2\u00a3\u00a5\7"+
		"\'\2\2\u00a4\u00a2\3\2\2\2\u00a4\u00a5\3\2\2\2\u00a5\u00a6\3\2\2\2\u00a6"+
		"\u00a7\7\13\2\2\u00a7\u00a8\7(\2\2\u00a8\u00b1\7\6\2\2\u00a9\u00ae\5\n"+
		"\6\2\u00aa\u00ab\7\7\2\2\u00ab\u00ad\5\n\6\2\u00ac\u00aa\3\2\2\2\u00ad"+
		"\u00b0\3\2\2\2\u00ae\u00ac\3\2\2\2\u00ae\u00af\3\2\2\2\u00af\u00b2\3\2"+
		"\2\2\u00b0\u00ae\3\2\2\2\u00b1\u00a9\3\2\2\2\u00b1\u00b2\3\2\2\2\u00b2"+
		"\u00b3\3\2\2\2\u00b3\u00b5\7\b\2\2\u00b4\u0098\3\2\2\2\u00b4\u009b\3\2"+
		"\2\2\u00b4\u009e\3\2\2\2\u00b4\u00a1\3\2\2\2\u00b5\u00b8\3\2\2\2\u00b6"+
		"\u00b4\3\2\2\2\u00b6\u00b7\3\2\2\2\u00b7\13\3\2\2\2\u00b8\u00b6\3\2\2"+
		"\2\24\21\31!-\60>@Rku}\u0081\u0096\u00a4\u00ae\u00b1\u00b4\u00b6";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}