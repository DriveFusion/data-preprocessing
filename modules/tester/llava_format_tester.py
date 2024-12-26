
from modules.tester.format_tester import FormatTester


class LlavaFormatTester:
    
    
    @staticmethod
    def compare_questions(json_path, questions_list, tokens, is_eval):
        FormatTester.compare_questions(json_path, questions_list, tokens, is_eval, False)
    
    
    @staticmethod
    def compare_answers(json_path, answers_list, is_eval):
        FormatTester.compare_answers(json_path, answers_list, is_eval, False)
    
    
    @staticmethod
    def compare_videos(json_path, videos_list, to_remove, is_eval):
        FormatTester.compare_videos(json_path, videos_list, to_remove, is_eval, False)