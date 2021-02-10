import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="The parent directory containing the nmap xml file want to combine.", type=str,
                    default='.')
parser.add_argument("-x", "--xmldocument", help="The name of the xml document that will be finally converted to xml.",
                    type=str, default='combined.xml')
parser.add_argument("-f", "--htmldocument", help="The name of the html document that will be the final report.",
                    type=str, default='combined.html')
parser.add_argument("-b", "--browser", help="The browser that you might want to open your final html doc",
                    type=str, default='firefox')
args = parser.parse_args()


def combine(directory='.', finaldoc='combined.xml', htmldoc='combined.html', browser='firefox'):
    dirlist = os.listdir(directory)
    filecount = 0
    
    if finaldoc in dirlist:
        print("A combined document already exist")
        exit(1)
    
    for x in dirlist:
        if x == 'xmlReportGenerator.py':
            continue
        elif '.xml' in x[-4:]:
            filecount += 1
            print(f'Adding {directory}/{x}')
            f = open(f'{directory}/{x}', 'r')
            lines = f.readlines()
            doc = open(f'{directory}/{finaldoc}', 'a')
            for line in lines:
                if (filecount != 1) and (line in lines[:5]):
                    continue
                elif line != lines[-1]:
                    doc.write(line)
            doc.close()
            f.close()
        else:
            print(f'Skipping {directory}/{x}')

    if finaldoc in os.listdir(directory):
        doc = open(finaldoc, 'a')
        doc.write("</nmaprun>")
        doc.close()
        print(f"Generating {directory}/{htmldoc}")
        os.system(f"xsltproc {directory}/{finaldoc} -o {directory}/{htmldoc}")
        answer = input(f'Do you want to view in {browser}? (yes/no) ')
        if answer.lower() == 'yes':
            os.system(f'{browser} {directory}/{htmldoc}')
    else:
        print('No files combined. Exiting...')
        exit(1)


combine(args.directory, args.xmldocument, args.htmldocument, args.browser)
