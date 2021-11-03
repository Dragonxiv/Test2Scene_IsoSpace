from tkinter.constants import TRUE
import xml.etree.ElementTree as ET
import networkx as nx
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt

window = tk.Tk()
window.title('Tkinter Open File Dialog')
window.resizable(False, False)
window.geometry('1024x768')


def select_file():
    filetypes = (
        ('xml files', '*.xml'),
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filenamne = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    f = open(filenamne, encoding="utf8")

    textcontent = f.read()

    # print(textcontent)

    xmlData = ET.fromstring(textcontent)

    G = nx.Graph()

    listPlace = []
    listSpatialEntity = []
    listNonMotionEvent = []
    listPath = []
    listLocation = []
    listMetaLink = []

    listOlink = []
    listQSlink = []

    for child in xmlData[1]:
        if(child.tag == "PLACE"):
            listPlace.append(child)
        if(child.tag == "SPATIAL_ENTITY"):
            listSpatialEntity.append(child)
        if(child.tag == "NONMOTION_EVENT"):
            listNonMotionEvent.append(child)
        if(child.tag == "PATH"):
            listPath.append(child)
        if(child.tag == "LOCATION"):
            listLocation.append(child)
        if(child.tag == "METALINK"):
            listMetaLink.append(child)
        if(child.tag == "OLINK"):
            listOlink.append(child)
        if(child.tag == "QSLINK"):
            listQSlink.append(child)

    # remove nodes as referenced by METALINKs
    for link in listMetaLink:
        fromID = link.attrib["fromID"]
        toID = link.attrib["toID"]
        toIDFound = False
        for item in listPlace:
            id = item.attrib["id"]
            if(id == toID):
                toIDFound = True
                break
        if(not toIDFound):
            for item in listSpatialEntity:
                id = item.attrib["id"]
                if(id == toID):
                    toIDFound = True
                    break
        if(not toIDFound):
            for item in listNonMotionEvent:
                id = item.attrib["id"]
                if(id == toID):
                    toIDFound = True
                    break
        if(not toIDFound):
            for item in listPath:
                id = item.attrib["id"]
                if(id == toID):
                    toIDFound = True
                    break
        if(not toIDFound):
            for item in listLocation:
                id = item.attrib["id"]
                if(id == toID):
                    toIDFound = True
                    break

        if(toIDFound):
            for item in listPlace:
                id = item.attrib["id"]
                if(id == fromID):
                    listPlace.remove(item)
                    break
            for item in listSpatialEntity:
                id = item.attrib["id"]
                if(id == fromID):
                    listSpatialEntity.remove(item)
                    break
            for item in listNonMotionEvent:
                id = item.attrib["id"]
                if(id == fromID):
                    listNonMotionEvent.remove(item)
                    break
            for item in listPath:
                id = item.attrib["id"]
                if(id == fromID):
                    listPath.remove(item)
                    break
            for item in listLocation:
                id = item.attrib["id"]
                if(id == fromID):
                    listLocation.remove(item)
                    break
        if(not toIDFound):
            # print(link.attrib["id"])
            failsafe = 5
            while(not toIDFound and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == toID):
                        toID = link.attrib["toID"]
                        break

                for item in listPlace:
                    id = item.attrib["id"]
                    if(id == toID):
                        toIDFound = True
                        break
                if(not toIDFound):
                    for item in listSpatialEntity:
                        id = item.attrib["id"]
                        if(id == toID):
                            toIDFound = True
                            break
                if(not toIDFound):
                    for item in listNonMotionEvent:
                        id = item.attrib["id"]
                        if(id == toID):
                            toIDFound = True
                            break
                if(not toIDFound):
                    for item in listPath:
                        id = item.attrib["id"]
                        if(id == toID):
                            toIDFound = True
                            break
                if(not toIDFound):
                    for item in listLocation:
                        id = item.attrib["id"]
                        if(id == toID):
                            toIDFound = True
                            break

                if(toIDFound):
                    for item in listPlace:
                        id = item.attrib["id"]
                        if(id == fromID):
                            listPlace.remove(item)
                            break
                    for item in listSpatialEntity:
                        id = item.attrib["id"]
                        if(id == fromID):
                            listSpatialEntity.remove(item)
                            break
                    for item in listNonMotionEvent:
                        id = item.attrib["id"]
                        if(id == fromID):
                            listNonMotionEvent.remove(item)
                            break
                    for item in listPath:
                        id = item.attrib["id"]
                        if(id == fromID):
                            listPath.remove(item)
                            break
                    for item in listLocation:
                        id = item.attrib["id"]
                        if(id == fromID):
                            listLocation.remove(item)
                            break
            if(not toIDFound):
                print(link.attrib["id"])

    i = 0
    pos = {}
    labelList = {}
    nodeListred = []

    for item in listPlace:
        text = item.attrib["text"]
        G.add_node(i, id=item.attrib["id"])
        nodeListred.append(i)
        pos[i] = (0, len(nodeListred)*2)
        labelList[i] = text
        i += 1

    nodeListorrange = []

    for item in listSpatialEntity:
        text = item.attrib["text"]
        G.add_node(i, id=item.attrib["id"])
        nodeListorrange.append(i)
        pos[i] = (2, len(nodeListorrange)*2)
        labelList[i] = text
        i += 1

    nodeListblue = []

    for item in listNonMotionEvent:
        text = item.attrib["text"]
        G.add_node(i, id=item.attrib["id"])
        nodeListblue.append(i)
        pos[i] = (4, len(nodeListblue)*2)
        labelList[i] = text
        i += 1

    nodeListpurple = []

    for item in listPath:
        text = item.attrib["text"]
        G.add_node(i, id=item.attrib["id"])
        nodeListpurple.append(i)
        pos[i] = (6, len(nodeListpurple)*2)
        labelList[i] = text
        i += 1

    nodeListolive = []

    for item in listLocation:
        text = item.attrib["text"]
        G.add_node(i, id=item.attrib["id"])
        nodeListolive.append(i)
        pos[i] = (8, len(nodeListolive)*2)
        labelList[i] = text
        i += 1

    pos=nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodeListred, node_color="tab:red")
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodeListorrange, node_color="tab:orange")
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodeListblue, node_color="tab:blue")
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodeListpurple, node_color="tab:purple")
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodeListolive, node_color="tab:olive")
    nx.draw_networkx_labels(G, pos, labelList)

    edgeList = []
    edgeLabels = {}

    for item in listOlink:
        fromID = item.attrib["fromID"]
        toID = item.attrib["toID"]
        fromNode = None
        toNode = None
        for (node, nodedata) in G.nodes.items():
            if nodedata["id"] == fromID:
                fromNode = node
            if nodedata["id"] == toID:
                toNode = node
        if((fromNode is not None) and (toNode is not None)):
            edgeList.append((fromNode, toNode))
            edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
            G.add_edge(fromNode, toNode)
        elif (fromNode is None) and (toNode is not None):
            failsafe = 5
            while((fromNode is None)and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == fromID):
                        fromID = link.attrib["toID"]
                        break
                for (node, nodedata) in G.nodes.items():
                    if nodedata["id"] == fromID:
                        fromNode = node
            if((fromNode is not None) and (toNode is not None)):
                edgeList.append((fromNode, toNode))
                edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
                G.add_edge(fromNode, toNode)
            else:
                print(item.attrib["id"])
        elif (fromNode is not None) and (toNode is None):
            failsafe = 5
            while((toNode is None)and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == toID):
                        toID = link.attrib["toID"]
                        break
                for (node, nodedata) in G.nodes.items():
                    if nodedata["id"] == toID:
                        toNode = node
            if((fromNode is not None) and (toNode is not None)):
                edgeList.append((fromNode, toNode))
                edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
                G.add_edge(fromNode, toNode)
            else:
                print(item.attrib["id"])
        if((fromNode is None) or (toNode is None)):
            print(fromNode)
            print(toNode)

    nx.draw_networkx_edges(G, pos=pos, edgelist=edgeList, edge_color="tab:olive")

    edgeList = []

    for item in listQSlink:
        fromID = item.attrib["fromID"]
        toID = item.attrib["toID"]
        fromNode = None
        toNode = None
        for (node, nodedata) in G.nodes.items():
            if nodedata["id"] == fromID:
                fromNode = node
            if nodedata["id"] == toID:
                toNode = node
        if((fromNode is not None) and (toNode is not None)):
            edgeList.append((fromNode, toNode))
            edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
            G.add_edge(fromNode, toNode)
        elif (fromNode is None) and (toNode is not None):
            failsafe = 5
            while((fromNode is None)and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == fromID):
                        fromID = link.attrib["toID"]
                        break
                for (node, nodedata) in G.nodes.items():
                    if nodedata["id"] == fromID:
                        fromNode = node
            if((fromNode is not None) and (toNode is not None)):
                edgeList.append((fromNode, toNode))
                edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
                G.add_edge(fromNode, toNode)
            else:
                print("from")
                print(item.attrib["id"])
                print(item.attrib["fromID"])
        elif (fromNode is not None) and (toNode is None):
            failsafe = 5
            while((toNode is None)and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == toID):
                        toID = link.attrib["toID"]
                        break
                for (node, nodedata) in G.nodes.items():
                    if nodedata["id"] == toID:
                        toNode = node
            if((fromNode is not None) and (toNode is not None)):
                edgeList.append((fromNode, toNode))
                edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
                G.add_edge(fromNode, toNode)
            else:
                print("to")
                print(item.attrib["id"])
                print(item.attrib["toID"])
        if((fromNode is None) and (toNode is None)):
            failsafe = 5
            while((toNode is None)and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == toID):
                        toID = link.attrib["toID"]
                        break
                for (node, nodedata) in G.nodes.items():
                    if nodedata["id"] == toID:
                        toNode = node
            failsafe = 5
            while((fromNode is None)and failsafe > 0):
                failsafe -= 1
                for link in listMetaLink:
                    if(link.attrib["fromID"] == fromID):
                        fromID = link.attrib["toID"]
                        break
                for (node, nodedata) in G.nodes.items():
                    if nodedata["id"] == fromID:
                        fromNode = node
            if((fromNode is not None) and (toNode is not None)):
                edgeList.append((fromNode, toNode))
                edgeLabels[(fromNode, toNode)] = item.attrib["relType"]
                G.add_edge(fromNode, toNode)
            else:
                print("from to")
                print(item.attrib["id"])

    nx.draw_networkx_edges(G, pos=pos, edgelist=edgeList, edge_color="tab:blue")
    # ax = plt.gca()
    # for e in edgeLabels:
    #     ax.annotate(edgeLabels[(e[0], e[1])],
    #         xy=pos[e[0]], xycoords='data',
    #         xytext=pos[e[1]], textcoords="data",
    #         arrowprops=dict(arrowstyle="-", color="0.5",
    #             shrinkA=5, shrinkB=5,
    #             patchA=None, patchB=None,
    #             connectionstyle="arc3,rad=0.1",
    #             ),
    #         annotation_clip=False,

    #         )
    nx.draw_networkx_edge_labels(G, pos, edgeLabels, label_pos=0.5)

    print("Nodes of graph: ")
    print(G.nodes())
    print("Edges of graph: ")
    print(G.edges())
    # nx.draw_networkx(G)
    plt.show()


open_button = ttk.Button(
    window,
    text='Open a File',
    command=select_file
)
open_button.place(x=5, y=5, width=100, height=25)

window.mainloop()
