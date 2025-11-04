import os
import sys
import argparse
from MyCodeCounter import MyCodeCounter

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
    counter = MyCodeCounter()
    
    print()
    print(f"Analyzing the Path: {args.path}")
    
    if counter.process_path(args.path):
        # multi files => show the summary information
        if os.path.isdir(args.path) or len(sys.argv) > 2:
            counter.print_summary()
        else:
            counter.print_single_file_result()

if __name__ == "__main__":
    main()