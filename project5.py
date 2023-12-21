import os
import tarfile
import subprocess
import re

def create_summary_file(assignment_path, assignment_number):
    summary_filename = f'summary_a{assignment_number}.html'
    with open(summary_filename, 'w') as summary_file:
        # Write HTML header
        summary_file.write('<html><head><title>Assignment Summary</title></head><body>\n')
        summary_file.write(f'<h1>Assignment {assignment_number} Summary</h1>\n')

        for root, dirs, files in os.walk(assignment_path):
            for file in files:
                file_path = os.path.join(root, file)
                if (file_path.endswith('.c') or file_path.endswith('.clj') or file_path.endswith('.lp') or file_path.endswith('.ml') or file_path.endswith('.py')): 
                    # Write file name and line count
                    summary_file.write(f'<p><a href="./a{assignment_number}/{file}">{file}</a> - Lines: {count_lines(file_path)}</p>\n')
                    # Write identifiers
                    identifiers = extract_identifiers(file_path)
                    summary_file.write('<ul>')
                    for identifier in sorted(identifiers):
                        summary_file.write(f'<li>{identifier}</li>')
                    summary_file.write('</ul>\n')

        # Write HTML footer
        summary_file.write('</body></html>\n')

    return summary_filename

def count_lines(file_path):
    with open(file_path, 'r') as file:
        line_count = 0
        for line in file:
            line_count += 1
        return line_count

def remove_comments(code):
    # Remove text between double and single quotation
    code = re.sub(r'".*?"', '', code, flags=re.DOTALL)
    code = re.sub(r'\'.*?\'', '', code, flags=re.DOTALL)
    # Remove C comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//[^\n]*', '', code)
    # Remove Clojure comments
    code = re.sub(r';;[^\n]*', '', code)
    # Remove OCaml comments
    code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)
    # Remove Python comments
    code = re.sub(r'#.*', '', code)
    # Remove Clingo comments
    code = re.sub(r'%[^\n]*', '', code)
    return code

def extract_identifiers(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
        code = remove_comments(code)
        words = re.split(r'[ \t\n\(\)\{\}\:\;\.,|$]', code)
        words = [word for word in words if word.replace('-','').isidentifier()]
        words = set(words)
    return words

def create_index_html(summary_files):
    with open('index.html', 'w') as index_file:
        index_file.write('<html><head><title>Assignment Index</title></head><body>\n')
        index_file.write('<h1>Assignment Index</h1>\n')
        index_file.write('<ul>\n')
        for summary_file in summary_files:
            index_file.write(f'<li><a href="{summary_file}">{summary_file}</a></li>\n')
        index_file.write('</ul>\n')
        index_file.write('</body></html>\n')

def create_tar_archive(assignment_path, summary_files):
    with tarfile.open('assignments.tar.gz', 'w:gz') as archive:
        for root, dirs, files in os.walk(assignment_path):
            for file in files:
                file_path = os.path.join(root, file)
                if (file_path.endswith('.c') or file_path.endswith('.clj') or file_path.endswith('.lp') or file_path.endswith('.ml') or file_path.endswith('.py')): 
                    archive.add(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), assignment_path))
        for summary_file in summary_files:
            archive.add(summary_file)
        archive.add('index.html')

def send_email():
    email_address = input("Enter the email address: ").strip()
    subprocess.run(["mutt", "-s", "Assignment 5", "-a", "assignments.tar.gz", "--", email_address], input=open("body.txt").read(), text=True)

if __name__ == "__main__":
    assignment_path = '/csc344'
    summary_files = []

    for assignment_number in range(1, 6):
        assignment_folder = os.path.join(assignment_path, f'a{assignment_number}')
        summary_file = create_summary_file(assignment_folder, assignment_number)
        summary_files.append(summary_file)

    create_index_html(summary_files)
    create_tar_archive(assignment_path, summary_files)


    # Send email
    send_email()

    print('Email sent successfully!')

