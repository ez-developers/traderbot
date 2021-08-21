from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomFileSystemStorage(FileSystemStorage):

    def get_valid_name(self, name):
        return name