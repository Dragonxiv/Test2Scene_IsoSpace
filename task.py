import spacy
import tkinter as tk
from tkinter.constants import DISABLED
from tkinter.font import NORMAL
from tkinter import ttk
from tkinter import filedialog as fd
import xml.etree.ElementTree as ET
import matplotlib, numpy
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# create the root window
window = tk.Tk()
window.title('Tkinter Open File Dialog')
window.resizable(False, False)
window.geometry('1024x768')

nlp = spacy.load("en_core_web_trf")

labelList = []

def resetGUI():
    for label in labelList:
        label.destroy()
    
    labelList.clear()
    textText.config(state=NORMAL)
    textText.delete(1.0, tk.END)
    textText.config(state=DISABLED)
    textText2.config(state=NORMAL)
    textText2.delete(1.0, tk.END)
    textText2.config(state=DISABLED)

def select_file():
    filetypes = (
        ('xml files', '*.xml'),
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filenames = fd.askopenfilenames(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if (len(filenames) > 0):
        resetGUI()
    
    counterPOS = {}
    sentLengths = {}

    counter = {}
    counterQS = {}
    counterQSTrig = {}
    counterOLTrig = {}
    counterMotion = {}

    for filename in filenames:
        f = open(filename, encoding="utf8")
        textcontent = f.read()

        xmlData = ET.fromstring(textcontent)
        doc = nlp(xmlData[0].text)

        sentLength = 0
        for token in doc:
            if(token.is_sent_start):
                if(sentLength > 0):
                    if(sentLengths.get(sentLength) is None):
                        sentLengths[sentLength] = 0
                    sentLengths[sentLength] = sentLengths[sentLength] + 1
                sentLength = 1
            else:
                sentLength += 1
            if(counterPOS.get(token.pos_) is None):
                counterPOS[token.pos_] = 0
            counterPOS[token.pos_] = counterPOS[token.pos_] + 1

        for child2 in xmlData[1]:
            if(counter.get(child2.tag) is None):
                counter[child2.tag] = 0
            counter[child2.tag] = counter[child2.tag] + 1
            if(child2.tag == "MOTION"):
                if(counterMotion.get(child2.attrib["text"]) is None):
                    counterMotion[child2.attrib["text"]] = 0
                counterMotion[child2.attrib["text"]] = counterMotion[child2.attrib["text"]] + 1
            if(child2.tag == "QSLINK"):  
                if(counterQS.get(child2.attrib["relType"]) is None):
                    counterQS[child2.attrib["relType"]] = 0
                counterQS[child2.attrib["relType"]] = counterQS[child2.attrib["relType"]] + 1
                trig = child2.attrib["trigger"]
                if(trig != ""):
                    for tag in xmlData[1]:
                        if(tag.tag == "SPATIAL_SIGNAL"):
                            if(tag.attrib["id"] == trig):
                                if(counterQSTrig.get(tag.attrib["text"]) is None):
                                    counterQSTrig[tag.attrib["text"]] = 0
                                counterQSTrig[tag.attrib["text"]] = counterQSTrig[tag.attrib["text"]] + 1
            if(child2.tag == "OLINK"):
                trig = child2.attrib["trigger"]
                if(trig != ""):
                    for tag in xmlData[1]:
                        if(tag.tag == "SPATIAL_SIGNAL"):
                            if(tag.attrib["id"] == trig):
                                if(counterOLTrig.get(tag.attrib["text"]) is None):
                                    counterOLTrig[tag.attrib["text"]] = 0
                                counterOLTrig[tag.attrib["text"]] = counterOLTrig[tag.attrib["text"]] + 1

    print(counterQS)
    print(len(counterQSTrig.keys()))
    plotX = []
    plotY = []
    for key in sentLengths.keys():
        plotX.append(key)
        plotY.append(sentLengths[key])

    x = numpy.array(plotX)
    y = numpy.array(plotY)

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    rects1 = ax.bar(x, y, .5)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().place(x=600, y=30, width=400)

    i = 1
    for key in counterPOS.keys():
        tmp = ttk.Label(window, text=key + ": " + str(counterPOS[key]))
        tmp.place(x=160, y=30+i*20, height=25)
        labelList.append(tmp)
        i += 1

    counterMaxMotion = {}
    for i in range(5):
        maxMotion = max(counterMotion, key=counterMotion.get)
        counterMaxMotion[maxMotion] = counterMotion[maxMotion]
        counterMotion.pop(maxMotion)
    
    i = 1
    for key in counterMaxMotion.keys():
        tmp = ttk.Label(window, text=key + ": " + str(counterMaxMotion[key]))
        tmp.place(x=300, y=30+i*20, height=25)
        labelList.append(tmp)
        i += 1

    i = 1
    for key in counterQSTrig.keys():
        textText.config(state=NORMAL)
        textText.insert(tk.END, key + ": " + str(counterQSTrig[key]) + "\n")
        textText.config(state=DISABLED)
        # tmp = ttk.Label(window, text=key + ": " + str(counterQSTrig[key]))
        # tmp.place(x=400, y=30+i*20, height=25)
        # labelList.append(tmp)
        # i += 1

    i = 1
    for key in counterOLTrig.keys():
        textText2.config(state=NORMAL)
        textText2.insert(tk.END, key + ": " + str(counterOLTrig[key]) + "\n")
        textText2.config(state=DISABLED)
        # tmp = ttk.Label(window, text=key + ": " + str(counterOLTrig[key]))
        # tmp.place(x=500, y=170+i*20, height=25)
        # labelList.append(tmp)
        # i += 1

    i = 1
    for key in counter.keys():
        tmp = ttk.Label(window, text=key + ": " + str(counter[key]))
        tmp.place(x=5, y=30+i*20, height=25)
        labelList.append(tmp)
        i += 1
        
    i = 1
    for key in counterQS.keys():
        tmp = ttk.Label(window, text=key + ": " + str(counterQS[key]))
        tmp.place(x=300, y=170+i*20, height=25)
        labelList.append(tmp)
        i += 1

open_button = ttk.Button(
    window,
    text='Open a File',
    command=select_file
)
open_button.place(x=5, y=5, width=100, height=25)

tagLabel = ttk.Label(window, text="TAGS")
tagLabel.place(x=5, y=30, height=25)

posLabel = ttk.Label(window, text="PoS-Tags")
posLabel.place(x=160, y=30, height=25)

qsLabel = ttk.Label(window, text="QsLink Typen")
qsLabel.place(x=300, y=170, height=25)

scrollbar = tk.Scrollbar(window)
scrollbar.place(x=585, y=55, width=15, height=250)

textText = tk.Text(window, state=DISABLED, yscrollcommand=scrollbar.set)
textText.place(x=400, y=55, width=185, height=250)

scrollbar.config(command=textText.yview)

qstLabel = ttk.Label(window, text="QsLink Trigger")
qstLabel.place(x=400, y=30, height=25)

otLabel = ttk.Label(window, text="OLink Trigger")
otLabel.place(x=400, y=305, height=25)

scrollbar2 = tk.Scrollbar(window)
scrollbar2.place(x=585, y=330, width=15, height=250)

textText2 = tk.Text(window, state=DISABLED, yscrollcommand=scrollbar2.set)
textText2.place(x=400, y=330, width=185, height=250)

scrollbar2.config(command=textText2.yview)

moLabel = ttk.Label(window, text="Motion Top5")
moLabel.place(x=300, y=30, height=25)

window.mainloop()
