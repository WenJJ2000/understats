from django.db import models

# Create your models here.
# class Question(models.Model):
#     answer = models.BooleanField()

class DecisionTreeNode(models.Model):
    yes_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="yes_nodes", null=True, blank=True)
    no_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="no_nodes", null=True, blank=True)
    one_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="one_nodes", null=True, blank=True, default=None)
    two_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="two_nodes", null=True, blank=True, default=None)
    moreThanTwo_node = models.ForeignKey("self", on_delete=models.CASCADE, related_name="moreThanTwo_nodes", null=True, blank=True, default=None)
    question = models.TextField()

