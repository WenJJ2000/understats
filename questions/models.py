from django.db import models

# Create your models here.
# class Question(models.Model):
#     answer = models.BooleanField()

class DecisionTreeNode(models.Model):
    yes_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="yes_nodes", null=True, blank=True)
    no_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="no_nodes", null=True, blank=True)
    question = models.TextField()

