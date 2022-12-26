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

def decision_tree_view(request):
    # Fetch the root node of the decision tree
    root_node = get_object_or_404(DecisionTreeNode, pk=1)
    all_nodes = DecisionTreeNode.objects.all()
    # Create a list to store the nodes in the decision tree
    nodes = []

    # If the form was submitted, determine the next node to display
    if request.method == 'POST':
        # Get the primary key of the current node from the form data
        node_pk = request.POST['node_id']
        current_node = get_object_or_404(DecisionTreeNode, pk=node_pk)

        # Determine the next node based on the user's answer
        if request.POST['answer'] == 'Yes':
            next_node = current_node.yes_node
        elif request.POST['answer'] == 'No':
            next_node = current_node.no_node
        elif request.POST['answer'] == '1':
            next_node = current_node.one_node
        elif request.POST['answer'] == '2':
            next_node = current_node.two_node
        elif request.POST['answer'] == 'More than 2':
            next_node = current_node.moreThanTwo_node
        else:
            next_node = None
        nodes.append(current_node)
        nodes.append(next_node)
        
        # Retrieve the previous nodes and add it to the front of nodes. After the full recursion, nodes will have the entire pathway of nodes to the current node
        def retrieve_previous_nodes(node):
            for x in all_nodes:
                if x.yes_node_id == node.id:
                    nodes.insert(0,x)
                    retrieve_previous_nodes(x)
                if x.no_node_id == node.id:
                    nodes.insert(0,x)
                    retrieve_previous_nodes(x)            
                if x.one_node_id == node.id:
                    nodes.insert(0,x)
                    retrieve_previous_nodes(x)            
                if x.two_node_id == node.id:
                    nodes.insert(0,x)
                    retrieve_previous_nodes(x)            
                if x.moreThanTwo_node_id == node.id:
                    nodes.insert(0,x)
                    retrieve_previous_nodes(x)            
        retrieve_previous_nodes(current_node)

    # If the form was not submitted
    else:
        nodes = [root_node]

    # Render the form template with the list of nodes and the current node
    return render(request, 'questions/form.html', {'nodes': nodes})

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
