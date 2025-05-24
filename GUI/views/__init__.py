"""
Views package initialization file
"""
from GUI.views.editor_view import EditorView
from GUI.views.config_view import ConfigView
from GUI.views.credits_view import CreditsView
from GUI.views.grammar_view import GrammarView
from GUI.views.lexical_analysis_view import LexicalAnalysisView
from GUI.views.syntactic_analysis_view import SyntacticAnalysisView
from GUI.views.semantic_analysis_view import SemanticAnalysisView
from GUI.views.symbol_table_view import SymbolTableView
from GUI.views.ir_view import IRView
from GUI.views.optimizer_view import OptimizerView
from GUI.views.code_generator_view import CodeGeneratorView
from GUI.views.report_view import ReportView

__all__ = ['EditorView', 'ConfigView', 'CreditsView',
           'GrammarView', 'LexicalAnalysisView', 'SyntacticAnalysisView',
           'SemanticAnalysisView', 'SymbolTableView', 'IRView', 'OptimizerView',
           'CodeGeneratorView','ReportView']

