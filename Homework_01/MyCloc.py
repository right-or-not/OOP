"""
MyCloc: Count the Lines of blank, comment, code in Files
- Avaliable File Format: Python, Java
- What you should do If you want to Add File Format: 
    1. Add your File Format Name in 'CodeCounter.stats'
    2. Add the Regular Expression in 'CodeCounter.patterns'
"""
# print("Hello world!\n") # Hello world


import os
import sys
import argparse
import re

class CodeCounter:
    def __init__(self):
        # Counter
        self.stats = {
            'Python': {'files': 0, 'blank': 0, 'comment': 0, 'code': 0},
            'Java': {'files': 0, 'blank': 0, 'comment': 0, 'code': 0},
            'Other': {'files': 0, 'blank': 0, 'comment': 0, 'code': 0}
        }
        
        # patterns of re
        self.patterns = {
            'python': {
                'filename': r'.*\.py|.*\.pyw',
                'blank': r'^\s*$',
                'single_comment': r'^\s*#',
                'multiline_comment': r'^\s*(""".*?""".*$)',
                'multiline_start_double': r'^\s*""".*$',
                'multiline_start_single': r"^\s*'''.*$",
                'multiline_end_double': r'.*"""\s*$',
                'multiline_end_single': r".*'''\s*$",
            },
            'java': {
                'filename': r'.*\.java|.*\.jav',
                'blank': r'^\s*$',
                'single_comment': r'^\s*//',
                'multiline_comment': r'^\s*/\*.*\*/\s*$',
                'multiline_start': r'^\s*/\*.*$',
                'multiline_end': r'.*\*/\s*$',
            },
            'other': {
                'blank': r'^\s*$',  # 空白行
            }
        }
    
    
    '''
    main function
    '''
    # Analyze the Path: File or Folder
    def process_path(self, path):
        # Path is a File
        if os.path.isfile(path):
            # Analyze the File
            result = self.analyze_file(path)
            if result:
                file_type = result['type']
                self.stats[file_type]['files'] += 1
                self.stats[file_type]['blank'] += result['blank']
                self.stats[file_type]['comment'] += result['comment']
                self.stats[file_type]['code'] += result['code']
                
                # Print the Answer
                self.print_single_file_result(result)
        # Path is a Folder
        elif os.path.isdir(path):
            # Traverse every File in the Path
            for root, dirs, files in os.walk(path):
                for file in files:
                    # Select the File
                    filepath = os.path.join(root, file)
                    # Analyze the File
                    result = self.analyze_file(filepath)
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
        if self.is_python_file(filename):
            return self.analyze_python_file(content, filepath)
        elif self.is_java_file(filename):
            return self.analyze_java_file(content, filepath)
        else:
            return self.analyze_other_file(content, filepath)
    
    
    '''
    Check & Analyze
    '''
    # check Python File 
    def is_python_file(self, filename):
        return re.match(self.patterns['python']['filename'], filename)
    
    # Test JAVA File   
    def is_java_file(self, filename):
        return re.match(self.patterns['java']['filename'], filename)
    
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
            if re.match(self.patterns['python']['blank'], line):
                blank_lines += 1
                continue
            
            # in multiline mode
            if in_multiline_comment:
                comment_lines += 1
                # check out multiline mode
                if (multiline_comment_char == '"""' and re.search(self.patterns['python']['multiline_end_double'], line)):
                    in_multiline_comment = False
                elif (multiline_comment_char == "'''" and re.search(self.patterns['python']['multiline_end_single'], line)):
                    in_multiline_comment = False
                continue
            
            # multiline comment
            if re.match(self.patterns['python']['multiline_comment'], line):
                comment_lines += 1
                continue
            
            # check in multiline mode
            # """
            if re.match(self.patterns['python']['multiline_start_double'], line):
                comment_lines += 1
                in_multiline_comment = True
                multiline_comment_char = '"""'
                continue
            # '''
            if re.match(self.patterns['python']['multiline_start_single'], line):
                comment_lines += 1
                in_multiline_comment = True
                multiline_comment_char = "'''"
                continue
            
            # single comment
            if re.match(self.patterns['python']['single_comment'], line):
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
            if re.match(self.patterns['java']['blank'], line):
                blank_lines += 1
                continue
            
            # in multiline mode
            if in_multiline_comment:
                comment_lines += 1
                # chech out multiline mode
                if re.search(self.patterns['java']['multiline_end'], line):
                    in_multiline_comment = False
                continue
            
            # multiline comment
            if re.match(self.patterns['java']['multiline_comment'], line):
                comment_lines += 1
                continue
            
            # check in multiline mode
            if re.match(self.patterns['java']['multiline_start'], line):
                comment_lines += 1
                if not re.search(self.patterns['java']['multiline_end'], line):
                    in_multiline_comment = True
                continue
            
            # single comment
            if re.match(self.patterns['java']['single_comment'], line):
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
            if re.match(self.patterns['other']['blank'], line):
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
    def print_single_file_result(self, result):
        """ Print 1 File """
        print()
        print(f"FilePath: {result['filepath']}")
        print(f"Language: {result['type']}")
        print(f"blank: {result['blank']}")
        print(f"comment: {result['comment']}")
        print(f"code: {result['code']}")
        print(f"sum: {result['blank'] + result['comment'] + result['code']}")
    
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
        print(f"{'SUM: ':<15} {total_files:>15} {total_blank:>15} {total_comment:>15} {total_code:>15} {total_all:>15}")
        print("-" * 95)


'''
main function - main()
'''
def main():
    # init a parser
    parser = argparse.ArgumentParser(description='Count the lines of the code file')
    # add an argument
    parser.add_argument('path', help='the Path to be analyzed')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"[ERROR]: Path '{args.path}' not exist! ! !")
        sys.exit(1)
    
    
    # init a CodeCounter Class
    counter = CodeCounter()
    
    print()
    print(f"Analyzing the Path: {args.path}")
    
    if counter.process_path(args.path):
        # multi files => show the summary information
        if os.path.isdir(args.path) or len(sys.argv) > 2:
            counter.print_summary()

if __name__ == "__main__":
    main()