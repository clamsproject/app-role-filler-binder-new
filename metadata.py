"""
The purpose of this file is to define the metadata of the app with minimal imports. 

DO NOT CHANGE the name of the file
"""

from mmif import DocumentTypes, AnnotationTypes

from clams.app import ClamsApp
from clams.appmetadata import AppMetadata
import re


# DO NOT CHANGE the function name 
def appmetadata() -> AppMetadata:
    """
    Function to set app-metadata values and return it as an ``AppMetadata`` obj.
    Read these documentations before changing the code below
    - https://sdk.clams.ai/appmetadata.html metadata specification. 
    - https://sdk.clams.ai/autodoc/clams.appmetadata.html python API
    
    :return: AppMetadata object holding all necessary information.
    """
    
    # first set up some basic information
    metadata = AppMetadata(
        name="Role Filler Binder",
        description="For identification and linking of named entities to their roles in OCR-based text.",
        app_license="Apache 2.0",
        identifier="role-filler-binder",
        url="https://github.com/clamsproject/app-role-filler-binder",
        analyzer_version=[l.strip().rsplit('==')[-1] for l in open('requirements.txt').readlines() if re.match(r'^transformers==', l)][0],
        analyzer_license="Apache 2.0",
    )
    # I/O specifications
    in_al = metadata.add_input(AnnotationTypes.Alignment)
    in_al.add_description('Alignment annotation between a TimePoint and a TextDocument.')
    in_td = metadata.add_input(DocumentTypes.TextDocument)
    in_td.add_description('Text document generated by an OCR tool.')
    in_tp = metadata.add_input(AnnotationTypes.TimePoint)
    in_tp.add_description("A labeled time point annotation generated by SWT or a similar app. "
                          "RFB will only process TimePoint annotations with currently supported labels: "
                          "{'I', 'N', 'Y', 'C', 'R'}")
    out_td = metadata.add_output(DocumentTypes.TextDocument, **{'@lang': 'en'})
    out_td.add_description('CSV-formatted text document.')
    out_al = metadata.add_output(AnnotationTypes.Alignment)
    out_al.add_description(
        'Alignment anchoring new RFB TextDocument to the original OCR TextDocument.'
    )

    return metadata


# DO NOT CHANGE the main block
if __name__ == '__main__':
    import sys
    metadata = appmetadata()
    for param in ClamsApp.universal_parameters:
        metadata.add_parameter(**param)
    sys.stdout.write(metadata.jsonify(pretty=True))
