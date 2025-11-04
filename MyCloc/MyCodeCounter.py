import os
import re

class MyCodeCounter():
    """
    self.data
    """
    def __init__(self):
        # languages
        self.languages = []
        # counter
        self.stats = {}
        # patterns of re
        self.patterns = {}
        
        # init counter and patterns
        self._init_default_languages()
        
    
    # init default languages:
    def _init_default_languages(self):
        default_languages = {
            'Python': {
                'filename': r'.*\.py|.*\.pyw',
                'blank': r'^\s*$',
                'single_comment': r'^\s*#',
                'multiline_comment': r'^\s*(""".*?""".*$)',
                'multiline_start_double': r'^\s*""".*$',
                'multiline_start_single': r"^\s*'''.*$",
                'multiline_end_double': r'.*"""\s*$',
                'multiline_end_single': r".*'''\s*$",
                "analyze_file": self.analyze_python_file
            },
            'Java': {
                'filename': r'.*\.java|.*\.jav',
                'blank': r'^\s*$',
                'single_comment': r'^\s*//',
                'multiline_comment': r'^\s*/\*.*\*/\s*$',
                'multiline_start': r'^\s*/\*.*$',
                'multiline_end': r'.*\*/\s*$',
                "analyze_file": self.analyze_java_file,
            },
            'Other': {
                'blank': r'^\s*$',
            }
        }
        
        for language_name, patterns in default_languages.items():
            if language_name != 'Other':
                self.languages.append(language_name)
            self.stats[language_name] = {'files': 0, 'blank': 0, 'comment': 0, 'code': 0}
            self.patterns[language_name] = patterns
            
    """
    main functions
    """
    # Analyze the Path: 
    def process_path(self, path):
        # File
        if os.path.isfile(path):
            # get the analyse result
            result = self.analyze_file(path)
            # update self.stats
            if result:
                file_type = result['type']
                self.stats[file_type]['files'] += 1
                self.stats[file_type]['blank'] += result['blank']
                self.stats[file_type]['comment'] += result['comment']
                self.stats[file_type]['code'] += result['code']
                
        # Folder
        elif os.path.isdir(path):
            # Traverse every files in Folder
            for root, dirs, files in os.walk(path):
                for file in files:
                    # select the filepath
                    filepath = os.path.join(root, file)
                    # get the analyse result
                    result = self.analyze_file(filepath)
                    # update self.stats
                    if result:
                        file_type = result['type']
                        self.stats[file_type]['files'] += 1
                        self.stats[file_type]['blank'] += result['blank']
                        self.stats[file_type]['comment'] += result['comment']
                        self.stats[file_type]['code'] += result['code']
        
        # ERROR Path
        else:
            print(f"[ERROR]: Path '{path}' not exist! ! !")
            return False
        return True
    
    # Analyze 1 File: Python or JAVA or Other
    def analyze_file(self, filepath):
        # Read all contents of the file
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.readlines()
            
        # Cannot Read the File
        # Encoding ERROR
        except(UnicodeDecodeError) as e:
            print(f"[ERROR][Encoding] File '{filepath}': Not a valid UTF-8 Encoding! ! !")
            print(f"[ERROR][Detials]: {e}")
            return None
        
        except(IOError) as e:
            error_type = "Not Exist! ! !"
            if "Permission denied" in str(e):
                error_type = "No Read Permission! ! !"
                
            print(f"[ERROR][IOError] File {filepath}: {error_type}")
            print(f"[ERROR][Detials]: {e}")
            return None
        
        except Exception as e:
            print(f"[ERROR][Unknow] File {filepath}: {type(e).__name__}")
            print(f"[ERROR][Detials]: {e}")
            return None
        
        # select filename and analyze
        filename = os.path.basename(filepath)
        for language in self.languages:
            if re.match(self.patterns[language]['filename'], filename):
                return self.patterns[language]['analyze_file'](content, filepath)
        return self.analyze_other_file(content, filepath)
    
    
    '''
    Analyze Methods
    '''
    # Analyze Python File
    def analyze_python_file(self, lines, filepath):
        # init param
        blank_lines = 0
        comment_lines = 0
        code_lines = 0
        in_multiline_comment = False
        multiline_comment_char = None
        
        # traverse every line
        for line in lines:
            # blank
            if re.match(self.patterns['Python']['blank'], line):
                blank_lines += 1
                continue
            
            # in multiline mode
            if in_multiline_comment:
                comment_lines += 1
                # check out multiline mode
                if (multiline_comment_char == '"""' and re.search(self.patterns['Python']['multiline_end_double'], line)):
                    in_multiline_comment = False
                elif (multiline_comment_char == "'''" and re.search(self.patterns['Python']['multiline_end_single'], line)):
                    in_multiline_comment = False
                continue
            
            # multiline comment
            if re.match(self.patterns['Python']['multiline_comment'], line):
                comment_lines += 1
                continue
            
            # check in multiline mode
            # """
            if re.match(self.patterns['Python']['multiline_start_double'], line):
                comment_lines += 1
                in_multiline_comment = True
                multiline_comment_char = '"""'
                continue
            # '''
            if re.match(self.patterns['Python']['multiline_start_single'], line):
                comment_lines += 1
                in_multiline_comment = True
                multiline_comment_char = "'''"
                continue
            
            # single comment
            if re.match(self.patterns['Python']['single_comment'], line):
                comment_lines += 1
                continue
            
            # code
            code_lines += 1
        
        return {
            'type': 'Python',
            'blank': blank_lines,
            'comment': comment_lines,
            'code': code_lines,
            'filepath': filepath
        }
    
    # Analyze JAVA File
    def analyze_java_file(self, lines, filepath):
        # init param
        blank_lines = 0
        comment_lines = 0
        code_lines = 0
        in_multiline_comment = False
        
        # traverse every line
        for line in lines:
            # blank
            if re.match(self.patterns['Java']['blank'], line):
                blank_lines += 1
                continue
            
            # in multiline mode
            if in_multiline_comment:
                comment_lines += 1
                # chech out multiline mode
                if re.search(self.patterns['Java']['multiline_end'], line):
                    in_multiline_comment = False
                continue
            
            # multiline comment
            if re.match(self.patterns['Java']['multiline_comment'], line):
                comment_lines += 1
                continue
            
            # check in multiline mode
            if re.match(self.patterns['Java']['multiline_start'], line):
                comment_lines += 1
                if not re.search(self.patterns['Java']['multiline_end'], line):
                    in_multiline_comment = True
                continue
            
            # single comment
            if re.match(self.patterns['Java']['single_comment'], line):
                comment_lines += 1
                continue
            
            # code
            code_lines += 1
        
        return {
            'type': 'Java',
            'blank': blank_lines,
            'comment': comment_lines,
            'code': code_lines,
            'filepath': filepath
        }
    
    # Analyze Other File
    def analyze_other_file(self, lines, filepath):
        # init param
        blank_lines = 0
        comment_lines = 0
        code_lines = 0
        
        # traverse every line
        for line in lines:
            # blank
            if re.match(self.patterns['Other']['blank'], line):
                blank_lines += 1
            # code
            else:
                code_lines += 1
        
        return {
            'type': 'Other',
            'blank': blank_lines,
            'comment': comment_lines,
            'code': code_lines,
            'filepath': filepath
        }
        
    
    
    '''
    OUTPUT: Print the Answer
    '''
    def print_single_file_result(self):
        """ Print one File """        
        print()
        print("-" * 95)
        
        # Head
        headers = ["Language", "files", "blank", "comment", "code", "sum"]
        print(f"{headers[0]:<15} {headers[1]:>15} {headers[2]:>15} {headers[3]:>15} {headers[4]:>15} {headers[5]:>15}")
        print("-" * 95)
        
        # print number of result
        result = {}
        for language, counter in self.stats.items():
            if counter['files']:
                result = counter
                result['type'] = language
        print(f"{result['type']:<15} {1:>15} {result['blank']:>15} {result['comment']:>15} {result['code']:>15} {result['blank'] + result['comment'] + result['code']:>15}")
        print("-" * 95)
    
    def print_summary(self):
        """ Print multi Files """
        print()
        print("-" * 95)
        
        # Head
        headers = ["Language", "files", "blank", "comment", "code", "sum"]
        print(f"{headers[0]:<15} {headers[1]:>15} {headers[2]:>15} {headers[3]:>15} {headers[4]:>15} {headers[5]:>15}")
        print("-" * 95)
        
        # print number of different lang
        for lang, data in self.stats.items():
            total_lines = data['blank'] + data['comment'] + data['code']
            if data['files'] > 0:
                print(f"{lang:<15} {data['files']:>15} {data['blank']:>15} {data['comment']:>15} {data['code']:>15} {total_lines:>15}")
        
        # compute total number
        total_files = sum(data['files'] for data in self.stats.values())
        total_blank = sum(data['blank'] for data in self.stats.values())
        total_comment = sum(data['comment'] for data in self.stats.values())
        total_code = sum(data['code'] for data in self.stats.values())
        total_all = total_blank + total_comment + total_code
        # print number of sum
        print("-" * 95)
        print(f"{'SUM':<15} {total_files:>15} {total_blank:>15} {total_comment:>15} {total_code:>15} {total_all:>15}")
        print("-" * 95)    
    
        
    


            
'''
Debug
'''   
def main():
    counter = MyCodeCounter()
    
    print(">>> Print counter.languages: ")
    print(f"> {counter.languages}")
    
    print()
    print(">>> Print counter.stats: ")
    for language, numbers in counter.stats.items():
        print(f"> '{language}': {numbers}")
    
    print()
    print(">>> Print counter.patterns: ")
    for language, patterns in counter.patterns.items():
        print(f"> '{language}': {patterns} ")
        
if __name__ == "__main__":
    main()
    