from django.shortcuts import render, get_object_or_404, redirect

from .models import DecisionTreeNode

# from .forms import QuestionForm

# class TreeNode:
#     def __init__(self,value,left=None, right=None):
#         self.value = value
#         self.left = left
#         self.right = right
    
# def my_view(request):
#     root = TreeNode

# def question_view(request):
#     form = QuestionForm(request.POST or None)
#     # if form.is_valid():
#         # form.save()
#     context = {
#         "form": form
#     }
#     return render(request,"questions/form.html", context)

# def decision_tree_view(request):
#     root_node = DecisionTreeNode.objects.get(pk=2)  # assume this is the root node of the decision tree
#     context = {"root_node": root_node}
#     return render(request, "questions/form.html", context)

def decision_tree_view(request, id):
    node = get_object_or_404(DecisionTreeNode, pk=id)

    if request.method == 'POST':
        # Process the user's answer and redirect to the next node
        if request.POST.get('answer') == 'Yes':
            next_node_id = node.yes_node_id
        elif request.POST.get('answer') == 'No':
            next_node_id = node.no_node_id
        elif request.POST.get('answer') == '1':
            next_node_id = node.one_node_id
        elif request.POST.get('answer') == '2':
            next_node_id = node.two_node_id
        elif request.POST.get('answer') == 'More than 2':
            next_node_id = node.moreThanTwo_node_id

        return redirect('questions:decision_tree', id=next_node_id)

    return render(request, 'questions/form.html', {'node': node})

# Create your views here.
# def decision_tree_view(request):
#     current_node = DecisionTreeNode.objects.get(id=1)  # get the root node

#     if request.method == 'POST':
#         answer = request.POST.get('answer')
#         if answer == 'yes':
#             current_node = current_node.yes_node_id
#         else:
#             current_node = current_node.no_node_id

#     return render(request, 'questions/form.html', {'current_node': current_node})
