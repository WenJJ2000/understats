from django.db.models import DecimalField, FileField
from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from questions.models import Datafile
from django.test import override_settings
import shutil
from questions.const import TEST_DIR


@override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
class Datafile_Test(TestCase):
    def setUp(cls):
        file = SimpleUploadedFile("input.csv", b"1,2,3,4,5,6,7")
        Datafile.objects.create(confidence_level=0.95, document=file)
        pass

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    def test_confidence_level_is_float(self):
        data = Datafile.objects.get(id=1)
        field = data._meta.get_field("confidence_level")
        print("Method: test_confidence_level_is_float.")
        self.assertEqual(type(field), DecimalField)

    # @override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
    def test_document_is_valid(self):
        data = Datafile.objects.get(id=1)
        doc = data._meta.get_field("document")
        print("Method: test_document_is_valid.")
        self.assertEqual(type(doc), FileField)

    def tearDown(self):
        print("\nDeleting temporary files...\n")
        shutil.rmtree(TEST_DIR, ignore_errors=True)
