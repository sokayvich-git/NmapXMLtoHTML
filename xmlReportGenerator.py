import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="The parent directory containing the nmap xml file want to combine.", type=str,
                    default='./')
parser.add_argument("-x", "--xmldocument", help="The name of the xml document that will be finally converted to xml.",
                    type=str, default='combined.xml')
parser.add_argument("-f", "--htmldocument", help="The name of the html document that will be the final report.",
                    type=str, default='combined.html')
parser.add_argument("-b", "--browser", help="The browser that you might want to open your final html doc",
                    type=str, default='firefox')
args = parser.parse_args()


def combine(directory, finaldoc, htmldoc, browser):
    # ensures uniformity in the file path structure
    if directory[-1] != '/':
        directory += '/'

    # Collect the file names in the directory
    dirlist = os.listdir(directory)
    filecount = 0

    # Checks to see if there is a possibility of of this being ran before and to make sure to make xml frank. monter
    if finaldoc in dirlist:
        print("A combined document already exist.")
        exit(1)

    # Begin the process of checking the file names for the xml files
    for x in dirlist:
        # Bit redundent but thought it would be nice to not think that the file will read itself
        if x == 'xmlReportGenerator.py':
            continue
        # Begin process of adding xmls to a combined document
        elif '.xml' in x[-4:]:
            # This var will keep track of docs to make sure it stripts the proper markups
            filecount += 1
            print(f'Adding {directory}{x}')
            # Opens xml file for copying
            f = open(f'{directory}{x}', 'r')
            lines = f.readlines()
            # Opens/Creates combined document to append the info
            doc = open(f'{directory}{finaldoc}', 'a')
            for line in lines:
                # Skip the first 5 lines of any document that isn't the first one
                if (filecount != 1) and (line in lines[:5]):
                    continue
                # Remove the last line of every xml document to not close the document early
                elif line != lines[-1]:
                    doc.write(line)
            # Close the combined xml for memory upkeep
            doc.close()
            # Close the single xml document
            f.close()
        # Skips all files that don't end in '.xml'
        else:
            print(f'Skipping {directory}{x}')

    # Checks if a combined xml document exist to prevent the creation of an empty 'combine' xml
    if finaldoc in os.listdir(directory):
        # Opens up the combined xml document to add the last markup to the end
        doc = open(f'{directory}{finaldoc}', 'a')
        doc.write("</nmaprun>")
        # Closes the combined xml document
        doc.close()
        print(f"Generating {directory}{htmldoc}")
        # Using the xsltproc program to convert the xml document to an html report
        os.system(f"xsltproc {directory}{finaldoc} -o {directory}{htmldoc}")
        # Ask if the user wants to use a browser to verify the output
        answer = input(f'Do you want to view in {browser}? (yes/no) ')
        if answer.lower() == 'yes':
            os.system(f'{browser} {directory}{htmldoc}')
    else:
        print('No files combined. Exiting...')
        exit(1)


combine(args.directory, args.xmldocument, args.htmldocument, args.browser)
