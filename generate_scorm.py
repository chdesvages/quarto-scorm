# Example usage: run this in the root directory for your course if your HTML site
# is in the _site/ subfolder:
#
# python generate_scorm.py _site my_course
#
# This will build a SCORM manifest and zip the contents of the _site/ folder
# into a file called SCORM_my_course.zip
# Note that your site needs to be generated/rendered first.

import sys, os, random, string, shutil

# Default arguments
if len(sys.argv) > 1:
    ROOT_DIR = sys.argv[1]
    OUTPUT_FILENAME = sys.argv[2]
else:
    ROOT_DIR = '.'
    OUTPUT_FILENAME = 'main'

# Default random unique identifier; replace this with an ID of your choice if you prefer
SCORM_ID = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=40))

TEMPLATE_LINE = "            <file href=\"FILE_PATH\"/>"
with open('scorm_manifest_template.xml', 'r') as template_file:
    HEADER = template_file.read()

ALL_LINES = HEADER.replace('REPLACE_SCORM_ID', SCORM_ID)

# Loop over the output of find, which lists all the files in root directory and subdirectories
for filename in os.walk(ROOT_DIR):
    for file in filename[-1]:
        FILENAME = os.path.join(filename[0].replace(ROOT_DIR, ''), file).lstrip('/')
        XML_LINE = TEMPLATE_LINE.replace('FILE_PATH', FILENAME)
        ALL_LINES += XML_LINE + '\n'

# Close the last XML tags
ALL_LINES += '        </resource>'
ALL_LINES += '\n' + '    </resources>'
ALL_LINES += '\n' + '</manifest>'

# Display the output to the console
print(ALL_LINES)

# Write to manifest file
MANIFEST_FILENAME="${ROOT_DIR}/imsmanifest.xml"
with open(ROOT_DIR + '/imsmanifest.xml', 'w') as file:
    file.write(ALL_LINES)

# Zip the SCORM
shutil.make_archive('SCORM_' + OUTPUT_FILENAME, 'zip', root_dir=ROOT_DIR)
