
from modules.tester.format_tester import FormatTester


class LlamaFormatTester:
    
    
    @staticmethod
    def compare_questions(json_path, questions_list, tokens, is_eval):
        FormatTester.compare_questions(json_path, questions_list, tokens, is_eval, True)
    
    
    @staticmethod
    def compare_answers(json_path, answers_list, is_eval):
        FormatTester.compare_answers(json_path, answers_list, is_eval, True)
    
    
    @staticmethod
    def compare_videos(json_path, videos_list, to_remove, is_eval):
        FormatTester.compare_videos(json_path, videos_list, to_remove, is_eval, True)