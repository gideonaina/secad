import pypandoc
import os

from dotenv import load_dotenv
load_dotenv()

temp_file = os.getenv('TEMP_FILE')
export_file = os.getenv('EXPORT_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')

def convert_markdown(markdown_string, doc_type='docx'):
    if not markdown_string:
        return None
    
    # Save the text to a temporary Markdown file
    # markdown_file = "/tmp/c.md"
    # with open(markdown_file, "w") as f:
    #     f.write(markdown_string)

    outputfile=f"{export_file}.{doc_type}"
    detail_file=f"{detail_output_file}.{doc_type}"

    print(f"coverting to .{doc_type}")
    pypandoc.convert_file(temp_file, doc_type, outputfile=outputfile)
    pypandoc.convert_file(detail_output_file, doc_type, outputfile=detail_file)
    print(f"output path {outputfile}")
    return outputfile