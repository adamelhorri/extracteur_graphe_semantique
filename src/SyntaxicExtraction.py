from Tokenizer.DependencyExtractor import DependencyExtractor
from Tokenizer.Disambiguator import Disambiguator
from Tokenizer.GroupsExtractor import GroupExtractor
from Tokenizer.Lexicon import Lexicon
from Tokenizer.MorphologicalAnalyzer import MorphologicalAnalyzer
from Tokenizer.Tokenizer import Tokenizer


class SyntaxicExtraction:
    def __init__(self, text):
        # Initialize the components of the NLP pipeline
        self.tokenizer = Tokenizer()
        self.lexicon = Lexicon()
        self.morph_analyzer = MorphologicalAnalyzer()
        self.disambiguator = Disambiguator()
        self.dependency_extractor = DependencyExtractor()
        self.group_extractor = GroupExtractor()
        
        # Process the text through the pipeline
        tokens = self.tokenizer.tokenize(text)
        tokens = self.lexicon.extract_lemmas(tokens)
        tokens = self.lexicon.extract_pos(tokens)
        tokens = self.morph_analyzer.analyze(tokens, self.lexicon)
        tokens = self.disambiguator.disambiguate(tokens, self.morph_analyzer, self.lexicon)
        tokens = self.dependency_extractor.extract_dependencies(tokens)
        tokens = self.group_extractor.extract_groups(tokens)
        
        # Store the processed tokens
        self.tokens = tokens
