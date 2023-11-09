from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from questions.scripts import choose_method
from .forms import DatafileForm
from .models import DecisionTreeNode
from questions import const
import pandas as pd
from decouple import config


def decision_tree_view(request):
    # Fetch the root node of the decision tree
    root_node = get_object_or_404(DecisionTreeNode, pk=const.ROOT_NODE)
    # print(root_node)
    all_nodes = DecisionTreeNode.objects.all()
    # Create a list to store the nodes in the decision tree
    nodes = []

    # If the form was submitted, determine the next node to display
    if request.method == "POST":
        # Get the primary key of the current node from the form data
        node_pk = request.POST["node_id"]
        current_node = get_object_or_404(DecisionTreeNode, pk=node_pk)

        # Determine the next node based on the user's answer
        if request.POST["answer"] == "Yes":
            next_node = current_node.yes_node
        elif request.POST["answer"] == "No":
            next_node = current_node.no_node
        elif request.POST["answer"] == "1":
            next_node = current_node.one_node
        elif request.POST["answer"] == "2":
            next_node = current_node.two_node
        elif request.POST["answer"] == "More than 2":
            next_node = current_node.moreThanTwo_node
        else:
            next_node = None
        nodes.append(current_node)
        nodes.append(next_node)
        # print(current_node)
        if next_node.yes_node == None and next_node.one_node == None:
            base = reverse("upload")
            q_string = urlencode({"test": next_node.description})
            url = "{}?{}".format(base, q_string)
            return redirect(url)

        # Retrieve the previous nodes and add it to the front of nodes.
        # After the full recursion, the list "nodes" will have the entire
        # pathway of nodes to the current node
        def retrieve_previous_nodes(node):
            for x in all_nodes:
                if x.yes_node_id == node.id:
                    nodes.insert(0, x)
                    retrieve_previous_nodes(x)
                if x.no_node_id == node.id:
                    nodes.insert(0, x)
                    retrieve_previous_nodes(x)
                if x.one_node_id == node.id:
                    nodes.insert(0, x)
                    retrieve_previous_nodes(x)
                if x.two_node_id == node.id:
                    nodes.insert(0, x)
                    retrieve_previous_nodes(x)
                if x.moreThanTwo_node_id == node.id:
                    nodes.insert(0, x)
                    retrieve_previous_nodes(x)

        retrieve_previous_nodes(current_node)

    # If the form was not submitted
    else:
        nodes = [root_node]

    # reach root node
    # Render the form template with the list of nodes and the current node
    return render(request, "questions/form.html", {"nodes": nodes})


def index_page(request):
    return render(request, "questions/index.html")


def upload_file(request):
    if request.method == "POST":
        test = request.GET.get("test")
        form = DatafileForm(request.POST, request.FILES)
        # print(request.FILES["document"])
        if form.is_valid():
            confidence = request.POST.get("confidence_level")
            choose_method(request.FILES["document"], test, float(confidence))
            return redirect("/questions/Result")
    else:
        form = DatafileForm()
        test = request.GET.get("test")
        # print(request, request.POST, test)

        context = {"form": form, "uploaded_file_url": config("BASE_URL")}
    return render(request, "questions/input.html", context)


def show_result(request):
    data = pd.read_json("output.json", typ="series")
    output = ""
    for k, v in data.items():
        output += f"{k} : {v}, "
    context = {"data": output}
    return render(request, "questions/output.html", context)


# def index(request):
#     latest_question_list = questions.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)
