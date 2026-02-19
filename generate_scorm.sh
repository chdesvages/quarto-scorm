#!/usr/bin/env bash
#
# Example usage: run this in the root directory for your course if your HTML site
# is in the _site/ subfolder:
#
# bash generate_scorm.sh _site my_course
#
# This will build a SCORM manifest and zip the contents of the _site/ folder
# into a file called SCORM_my_course.zip
# Note that your site needs to be generated/rendered first.

# Default root directory is ./
ROOT_DIR=${1:-"."}

# Default output filename will be SCORM_main.zip
OUTPUT_FILENAME=${2:-"main"}

# Default random unique identifier; replace this with an ID of your choice if you prefer
SCORM_ID=$(shuf -er -n40  {A..Z} {a..z} {0..9} | tr -d '\n')

TEMPLATE_LINE="                <file href=\"FILE_PATH\"/>"
HEADER=$(cat scorm_manifest_template.xml)
ALL_LINES="${HEADER/REPLACE_SCORM_ID/$SCORM_ID}"

# Loop over the output of find, which lists all the files in root directory and subdirectories
while IFS= read -r filename; do
    # Build the corresponding line to include each file
    FILENAME_NO_ROOT=${filename#"$ROOT_DIR/"}
    XML_LINE="${TEMPLATE_LINE/FILE_PATH/$FILENAME_NO_ROOT}"
    ALL_LINES+=$'\n'"$XML_LINE"
done < <(find "$ROOT_DIR" -type f)

# Close the last XML tags
ALL_LINES+=$'\n'"        </resource>"
ALL_LINES+=$'\n'"    </resources>"
ALL_LINES+=$'\n'"</manifest>"

# Display the output to the console
printf $ALL_LINES

# Write to manifest file
MANIFEST_FILENAME="${ROOT_DIR}/imsmanifest.xml"
echo "$ALL_LINES" > "$MANIFEST_FILENAME"
# cat $MANIFEST_FILENAME

# Zip the SCORM
zip -r SCORM_"${OUTPUT_FILENAME}".zip "$ROOT_DIR"
