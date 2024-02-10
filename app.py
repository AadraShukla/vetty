from flask import Flask, render_template, request
import os
import sys
import codecs

app = Flask(__name__)

#Example url: http://127.0.0.1:5000/file4.txt?start_line=2&end_line=24

@app.route('/')
def display_default_file():
    return display_file('file1.txt')

@app.route('/<filename>')
def display_file(filename='file1.txt'):
    try:
        start_line = int(request.args.get('start_line',   1))
        end_line = int(request.args.get('end_line', sys.maxsize))

        # Try to open the file with UTF-8 encoding, if it fails, use the system's default encoding
        try:
            with codecs.open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            with open(filename, 'r', encoding='utf-16') as file:
                lines = file.readlines()

        if end_line > len(lines):
            end_line = len(lines)

        content = ''.join(lines[start_line-1:end_line])
        
        return render_template('file_content.html', content=content)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
