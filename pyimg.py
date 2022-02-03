import os
import tempfile
from pdf2image import convert_from_path

filename = '1.pdf'

with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path(filename, dpi=300,output_folder=path, last_page=1, first_page=0)

base_filename = os.path.splitext(os.path.basename(filename))[0] + '.jpg'

save_dir = '.'

for page in images_from_path:
    page.save(os.path.join(save_dir, base_filename), 'JPEG')