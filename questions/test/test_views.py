import shutil
from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.test import Client
from django.urls import reverse
from questions.models import DecisionTreeNode, Datafile
from decouple import config
from django.core.files.uploadedfile import SimpleUploadedFile
from questions.scripts import choose_method
from questions.const import TEST_DIR, ROOT_NODE
from django.test import override_settings


# Create your tests here.
@override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
class PagesTest(SimpleTestCase):
    databases = "__all__"

    def setUp(self):
        self.client = Client()
        file = SimpleUploadedFile(
            "input.csv",
            b"1,2,3,4,5,6",
        )
        Datafile.objects.create(confidence_level=0.95, document=file)
        pass

    def test_index_page(self):
        url = reverse("index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "questions/index.html")
        print("Index_Page Check")

    def test_upload_page(self):
        url = reverse("upload")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "questions/input.html")
        print("Upload Check")

    def test_result_page(self):
        url = reverse("questions:ShowResults")
        context = {"data": [1, 2, 3]}
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "questions/output.html")
        res = self.client.post(url, context)
        self.assertEqual(res.status_code, 200)
        print("Result Check")

    def tearDown(self):
        print("\nDeleting temporary files...\n")
        shutil.rmtree(TEST_DIR, ignore_errors=True)

    # def test_choose_ztest(self):
    #     # c = Client()
    #     res = choose_method()
    #     self.assertFieldOutput({})


@override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
class QuestionsPageTest(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        DecisionTreeNode.objects.create(
            description="test", question="testing", id=ROOT_NODE
        )

    def test_question_page(self):
        url = reverse("questions:Decisions")
        # print(url)
        res = self.client.get(url)
        # request = res.wsgi_request
        # print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "questions/form.html")
        print("questions Check")

    def tearDown(self):
        print("\nDeleting temporary files...\n")
        shutil.rmtree(TEST_DIR, ignore_errors=True)
