from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil

class ImageProcessor:
    @staticmethod
    def remove_metadata(image_path):
        temp_path = os.path.splitext(image_path)[0] + '_temp' + os.path.splitext(image_path)[1]
        shutil.copy(image_path, temp_path)
        image = Image.open(temp_path)
        data = list(image.getdata())
        image_without_metadata = Image.new(image.mode, image.size)
        image_without_metadata.putdata(data)
        try:
            image_without_metadata.save(temp_path, format=image.format, quality=95)  # Save without metadata, preserving quality
        except Exception as e:
            raise e
        return temp_path

    @staticmethod
    def save_image(temp_path, original_path):
        directory = os.path.dirname(original_path)
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)
        save_path = os.path.join(directory, f"{name}_NOMETADATA{ext}")
        shutil.move(temp_path, save_path)

    @staticmethod
    def display_metadata(image_path):
        image = Image.open(image_path)
        metadata = image.info
        exif_data = None
        
        try:
            exif_data = image._getexif()  
        except Exception as e:
            raise e

        if exif_data:
            exif_metadata = {TAGS.get(tag, tag): value for tag, value in exif_data.items() if TAGS.get(tag, tag)}
            metadata.update(exif_metadata)
        
        metadata_text = "\n".join([f"{key}: {value}" for key, value in sorted(metadata.items())])
        return metadata_text if metadata_text else "No metadata found."

    @staticmethod
    def has_metadata(image_path):
        image = Image.open(image_path)
        metadata_present = False
        
        # Check EXIF data
        try:
            exif_data = image._getexif()
            if exif_data:
                metadata_present = True
        except Exception:
            pass
        
        # Check other metadata based on image format
        if image.format == 'PNG':
            if image.info:
                metadata_present = True
        elif image.format in ['GIF', 'BMP']:
            if image.info:
                metadata_present = True
        elif image.format in ['WEBP', 'HEIC']:
            if image.info:
                metadata_present = True
        
        # Additional check for any metadata in image.info
        if image.info:
            metadata_present = True
        
        return metadata_present