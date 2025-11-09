from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine             import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based import Semantic_Text__Engine__Hash_Based


class Semantic_Text__Service(Type_Safe):
    semantic_text__engine: Semantic_Text__Engine = None

    def setup(self):
        #self.semantic_text__engine = Semantic_Text__Engine__Random()        # todo: figure out how to assign this (specially when we wire in the multiple LLMs engines)
        self.semantic_text__engine = Semantic_Text__Engine__Hash_Based()    # Using hash-based engine for deterministic, reproducible classifications   (pseudo random mappings based on the hash value)
        return self

    def classify_text(self, text):
        return self.semantic_text__engine.classify_text(text)