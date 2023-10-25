from django.db import models

# Create your models here.
# class Question(models.Model):
#     answer = models.BooleanField()


class CONST:
    ROOT_NODE = 17
    DEBUG = True


class DecisionTreeNode(models.Model):
    yes_node = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="yes_nodes",
        null=True,
        blank=True,
    )
    no_node = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="no_nodes", null=True, blank=True
    )
    one_node = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="one_nodes",
        null=True,
        blank=True,
        default=None,
    )
    two_node = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="two_nodes",
        null=True,
        blank=True,
        default=None,
    )
    moreThanTwo_node = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="moreThanTwo_nodes",
        null=True,
        blank=True,
        default=None,
    )
    description = models.TextField(null=True, default=None)
    question = models.TextField()

    def __str__(self):
        if CONST.DEBUG == True:
            return self.question + " " + str(self.pk)
        else:
            return self.pk


class Datafile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
