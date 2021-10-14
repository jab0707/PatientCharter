# Set-ExecutionPolicy Unrestricted -Scope Process
#python_dev/Scripts/activate
import tkinter as tk
import json as js
from tkinter import filedialog, Text, ttk, messagebox
from functools import reduce #magical function that makes recusive object/property calling happen
import os
import importlib.util
import baseSettings as charterSettings
import re
'''
Generic
-hotkeys for adding labvs and navigating
-print to google docs
-make a launcher
-make an installer

Give patients tabs:
	history/demographic
		-make past history modular/add more with rlevant checkbox
	day to day updates
		buttons for add lab, speech to say if labs were taken or not
		buttons for specific common labs and an "other" button
			speech generated all lab values within normal limits excepts
		same for imagine
			imaging modlaity
			radiology comments/read
			personal read
	plan
	-default plans

	print button
		with relevant checkbox
		new patient ..
		day to day updates ..
		into a text box on last part of patient panel

	make history of present illness scrollable and bigger
'''

#functions and classes
defaultPatient = """[
		{"Tab":["Demographic Info",
			{"Entry":["Name","","",""]},
			{"Entry":["Age","","years",""]},
			{"Entry":["Gender","","",""]},
			{"Text":["Past History","",""]},
			{"Text":["Hisotry of Present Illness","",""]}
		]},
		{"Tab":["Daily Updates",
			{"Variable": ["labs",0,[],""]},
			{"Variable": ["imaging",0,[],""]}
		]}
	]"""
def importSettings(file):
	spec = importlib.util.spec_from_file_location("*", file)
	lib = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(lib)
	return lib


def formatAttributeName(attributeStr):
	nameList = re.split(' |_',attributeStr)
	formattedName = ''
	for strIx in range(len(nameList)):
		if strIx > 0:
			formattedName = formattedName+'_'+nameList[strIx].capitalize()
		else:
			formattedName = formattedName+nameList[strIx].lower()
	return formattedName

class Patient_Variable():
	def __init__(self,number = 0,names = []):
		self.number = number
		self.names = names



class Patient_Tab():

	def __init__(self,parent,label,fields):
		self.frame = tk.Frame(parent)
		self.canvas = tk.Canvas(self.frame,highlightthickness = 0, bd = 0)
		
		scrollBar = ttk.Scrollbar(self.frame, command = self.canvas.yview, orient="vertical")
		
		self.canvas.configure(yscrollcommand=scrollBar.set)
		#self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
		
		self.tab = tk.Frame(self.canvas)
		
		self.parent = parent
		self.label = label
		self.fields = [];
		self.attributesList = []
		self.tabIsRelevant = tk.IntVar()
		self.tabIsRelevant.trace('w',self.toggleRelevant)
		self.tabIsRelevantButton = tk.Checkbutton(self.tab, variable = self.tabIsRelevant, onvalue = 1, offvalue = 0, text='Tab Is Relevant')
		self.tabIsRelevantButton.select()
		self.tabIsRelevantButton.grid(row = 0,columnspan = 3)
		self.rows = 1
		for field in fields:
			field = {k.lower():val for k, val in field.items()}
			addedField = self.addField(field)
			self.fields.append(addedField)
		self.canvasFrame = self.canvas.create_window((0,0), window = self.tab)
		self.canvas.pack(fill = 'both', expand = True,side = 'left')
		scrollBar.pack(fill = 'both', expand = True,side = 'right')
		self.frame.pack(fill = 'both', expand = True)
		#self.tab.grid(row = 0,columnspan =2)
		self.canvas.bind('<Configure>', self.fixScroll)

	def fixScroll(self, event):
		canvas_width = event.width
		
		#print(canvas_width)
		#canvas_width = self.frame.width
		self.canvas.configure(scrollregion = self.canvas.bbox('all'))
		#self.canvas.itemconfig(self.canvasFrame, width = canvas_width)
	def toggleRelevant(self,*args,**kwargs):
		for attr in self.attributesList:
			if self.tabIsRelevant.get() == 1:
				getattr(self, attr).relevantButton.select()
			else:
				getattr(self, attr).relevantButton.deselect()
	def toggleMultifieldRelevant(self,*args):
		multifieldName = args[0]
		relevantVal = mainApp.getvar(multifieldName)
		for subFieldName in reduce(getattr,[multifieldName,'subfieldNames'],self):
			subType = reduce(getattr,[subFieldName,'type'],self)
			if subType == 'entry' or subType == 'text':
				if relevantVal == 1:
					getattr(self, subFieldName).relevantButton.select()
				else:
					getattr(self, subFieldName).relevantButton.deselect()
		pass
	def addField(self,field, fieldId= ''):
		baseName = formatAttributeName(list(field.values())[0][0])
		attrName = baseName+fieldId
		if [*field][0].lower() == 'entry':
			#attrName = formatAttributeName(field['entry'][0])
			self.attributesList.append(attrName)
			addedField = self.addEntry(field,attrName)
		elif [*field][0].lower() == 'text':
			#attrName = formatAttributeName(field['text'][0])
			self.attributesList.append(attrName)
			addedField = self.addText(field,attrName)
		elif [*field][0].lower() == 'multifield':
			multiField = field['multifield']
			#multifieldName = formatAttributeName(multiField[0])
			addedField = self.addMultiField(multiField,attrName,fieldId)
			
		elif [*field][0].lower() == 'variable':
			#attrName = formatAttributeName(field['variable'][0])
			addedField = self.addVariable(field,attrName)
		self.rows = self.rows+1
		return addedField
		
			
	def addVariable(self,field,attrName):
		setattr(self,attrName,Patient_Variable(number = field['variable'][1],names = field['variable'][2]))
		setattr(getattr(self,attrName),'type','variable')
		return {'variable':attrName}

	def addEntry(self,field,attrName):
		
		tk.Label(self.tab, text=list(field.values())[0][0]).grid(row = self.rows, column = 0)

		setattr(self, attrName, tk.Entry(self.tab))
		setattr(getattr(self,attrName),'type','entry')
		getattr(self, attrName).grid(row=self.rows,column=1)
		units = field['entry'][2]
		setattr(getattr(self,attrName),'units',units)
		if units =='':
			finalCol =2
		else:
			finalCol = 3
			tk.Label(self.tab,text=units).grid(row= self.rows, column = 2)

		setattr(getattr(self,attrName),'isRelevant',tk.IntVar())
		setattr(getattr(self,attrName),'relevantButton', tk.Checkbutton(self.tab, variable = reduce(getattr, [attrName, 'isRelevant'], self),
																		onvalue = 1, offvalue=0, text = 'relevant'))
		reduce(getattr,[attrName,'relevantButton'],self).grid(row=self.rows,column=finalCol,sticky='w')
		reduce(getattr,[attrName,'relevantButton'],self).select()
		getattr(self,attrName).delete(0,tk.END)
		getattr(self,attrName).insert(0,field['entry'][1])

		return {'entry':attrName}

	def addText(self,field,attrName):
		tk.Label(self.tab, text=list(field.values())[0][0]).grid(row = self.rows, column = 0)
		setattr(self,attrName, tk.Text(self.tab, width = 30, height =5))
		setattr(getattr(self,attrName),'type','text')
		getattr(self,attrName).grid(row=self.rows,column=1)
		scrollBar = ttk.Scrollbar(self.tab, command = reduce(getattr,[attrName, "yview"],self))
		scrollBar.grid(row = self.rows, column = 2, sticky="nsew")
		getattr(self,attrName)['yscrollcommand'] = scrollBar.set
		setattr(getattr(self,attrName),'isRelevant',tk.IntVar())
		setattr(getattr(self,attrName),'relevantButton', tk.Checkbutton(self.tab, variable = reduce(getattr, [attrName, 'isRelevant'], self),
																		onvalue = 1, offvalue=0, text = 'relevant'))
		reduce(getattr,[attrName,'relevantButton'],self).grid(row=self.rows,column=3)
		reduce(getattr,[attrName,'relevantButton'],self).select()
		#getattr(self,attrName).delete(0,tk.END)
		getattr(self,attrName).insert(tk.END,field['text'][1])
		return {'text':attrName}

	def addMultiField(self,multiField,multifieldName,fieldId):
		setattr(self,multifieldName,tk.Label(self.tab, text = multiField[0]))
		setattr(getattr(self,multifieldName),'tag',multiField[1])
		setattr(getattr(self,multifieldName),'isRelevant',tk.IntVar(name =multifieldName))
		reduce(getattr,[multifieldName,'isRelevant'],self).trace('w',self.toggleMultifieldRelevant)
		setattr(getattr(self,multifieldName),'relevantButton', tk.Checkbutton(self.tab, variable = reduce(getattr, [multifieldName, 'isRelevant'], self),
																		onvalue = 1, offvalue=0, text = 'group is relevant'))

		reduce(getattr,[multifieldName,'relevantButton'],self).grid(row=self.rows,column=2)
		
		setattr(getattr(self,multifieldName),'subfieldNames',[])
		reduce(getattr,[multifieldName,'relevantButton'],self).select()
		getattr(self,multifieldName).grid(row=self.rows,column=1)
		self.rows = self.rows + 1
		subFields = [multifieldName,multiField[1] ]
		subFieldNames = []
		for subFieldIx in  range(len(multiField)-2):
			subField = multiField[subFieldIx+2]
			subField = {k.lower():val for k, val in subField.items()}
			addedField = self.addField(subField,fieldId)
			subFields.append(addedField)
			subFieldNames.append(list(addedField.values())[0])
		setattr(getattr(self,multifieldName),'subfieldNames',subFieldNames)
		return {"multifield":subFields}
class Patient_Presentation():


	def __init__(self,parent,text ="new patient",patientDataFile='',patientSettingsFile = '[]'):
		self.tab = tk.Frame(parent)
		self.tab.pack(fill = 'both', expand = True)
		self.text = text
		self.subTabs =[]
		self.parent = parent
		self.patientSettingsFile = patientSettingsFile
		self.generateBody(patientDataFile)
		for tabName in self.subTabs:
			if hasattr(getattr(self,tabName),"name"):
				if (name := reduce(getattr,[tabName,'name'],self).get()) != "":
					self.text = name

		#.grid(row = 0, column = 0, sticky = 'nsew')

	def generateBody(self,patientDataFile):
		if patientDataFile == '':
			data = js.loads(defaultPatient)
		else:
			f = open(patientDataFile)
			data = js.load(f)


		self.individualTabController = ttk.Notebook(self.tab)
		fieldsWithoutTabs = []
		for field in data:
			field = {k.lower():val for k, val in field.items()}
			if [*field][0].lower() == 'tab':
				tabData = field['tab']
				tabName = formatAttributeName(tabData[0])
				setattr(self,tabName,Patient_Tab(self.individualTabController,tabName,tabData[1:]))
				self.subTabs.append(tabName)
			else:
				fieldsWithoutTabs.append(field)
		if len(fieldsWithoutTabs) > 0:
				tabName = 'misc_Patient_Info'
				setattr(self,tabName,Patient_Tab(self.individualTabController,tabName,fieldsWithoutTabs))
				self.subTabs.append(tabName)
		
		for tab in self.subTabs:
			self.individualTabController.add(reduce(getattr, [tab,'frame'], self),text = reduce(getattr, [tab,'label'], self))
		
		#add the output window
		self.EvaluationStatementWindow = tk.Frame(self.individualTabController)
		self.EvaluationStatement = tk.Text(self.EvaluationStatementWindow, width = 60, height =20)
		self.EvaluationStatement.grid(row=0, column = 0, sticky="nsew", padx=2, pady=2)
		self.EvaluationStatementScroll = ttk.Scrollbar(self.EvaluationStatementWindow, command = self.EvaluationStatement.yview)
		self.EvaluationStatementScroll.grid(row = 0, column = 1, sticky="nsew")
		self.EvaluationStatement['yscrollcommand'] = self.EvaluationStatementScroll.set
		self.individualTabController.add(self.EvaluationStatementWindow, text = 'Evaluation Statement')

		self.individualTabController.pack(fill='both',expand=True)
		self.saveButton = ttk.Button(self.tab, text = 'Save Patient', command = self.savePatient).pack(side = 'left',expand = True)#.grid(row = 1, column = 0)
		self.loadSettingsButton = ttk.Button(self.tab, text = 'Load Print Settings', command = self.loadPrintSettings).pack(side = 'left',expand = True)#.grid(row = 1, column = 1)
		self.printButton = ttk.Button(self.tab, text = 'Refresh Evaluation', command = self.printEvaluation).pack(side = 'left',expand = True)#.grid(row = 1, column = 2)
		

	def getField(self,tabName,field):
		fieldType = [*field][0]
		if fieldType == 'entry':
			return {'entry':[field['entry'],reduce(getattr,[tabName, field['entry']], self).get(),reduce(getattr,[tabName,field['entry'],'units'],self)]}
		elif fieldType == 'text':
			return {'text':[field['text'],reduce(getattr,[tabName, field['text']], self).get('1.0',tk.END)]}
		elif fieldType == 'variable':
			number = reduce(getattr,[tabName,field['variable'],'number'],self)
			names = reduce(getattr,[tabName,field['variable'],'names'],self)
			
			return {'variable':[field['variable'],number,names]}
		elif fieldType == 'multifield':
			subfields = field['multifield']
			multifieldValues = [subfields[0],subfields[1]]
			
			for subIx in range(len(subfields)-2):
				multifieldValues.append(self.getField(tabName,subfields[subIx+2]))
			return {'multifield':multifieldValues}

	def savePatient(self):
		outData = []
		
		for tabName in self.subTabs:
			fieldsInTab = [tabName]
			for field in reduce(getattr,[tabName, "fields"], self):
				fieldsInTab.append(self.getField(tabName,field))
			print(fieldsInTab)
			outData.append({"tab":fieldsInTab})
			
		global baseDir
		fileName = filedialog.asksaveasfilename(initialdir=baseDir, title = 'Save Patient',
								  filetypes =(('json','*.json'),('all files', '*.*')),defaultextension="*.json")
		
		baseDir = os.path.split(fileName)[0]
		with open(fileName, 'w') as f:
			js.dump(outData, f)
	def loadPrintSettings(self):
		global baseDir
		fileName = tk.filedialog.askopenfilename(initialdir=baseDir, title = 'Select Patient Print Settings',
								  filetypes =(('json','*.json'),('all files', '*.*')))
		baseDir = os.path.split(fileName)[0]
		self.patientSettingsFile = fileName

	def printEvaluation(self):
		self.EvaluationStatement.delete('1.0',tk.END)
		if self.patientSettingsFile == '[]':
			#messagebox.showwarning('Warning', 'No patient print settings loaded\nEvaluation may not be printer correctly')
			self.printSettings = importSettings('baseSettings.py')
		else:
			self.printSettings = importSettings(self.patientSettingsFile)
		self.printer = self.printSettings.patientPrinter()
		for tabName in self.subTabs:
			if reduce(getattr, [tabName,'tabIsRelevant'],self).get() == 1:
				self.printTab(tabName)
			'''fieldsForThisTab = []
			for field in reduce(getattr [tabName, "attributesList"], self):
				if reduce(getattr [tabName, "field", "isRelevant"], self).get() == 1:
					fieldsForThisTab.append([field])
			relevantFields{tabName} = fieldsForThisTab'''

	def printTab(self, tabName):
		printout = self.printer.tabNameDictionary[tabName](self)
		self.EvaluationStatement.insert(tk.END, printout)


	def deletePatient(self):
		pass
	def exportPatient(self):
		pass

def main(runApp=True):
	

	if runApp:
		mainApp.mainloop()
	else:
		NewPatient()
	
def NewPatient():
	patient = Patient_Presentation(patientTabController, f'New Patient {len(patientList)}')
	patientList.append(patient)
	patientTabController.add(patient.tab,text = patient.text)

def LoadPatient():
	global baseDir
	
	fileName = tk.filedialog.askopenfilename(initialdir=baseDir, title = 'Select Patient',
								  filetypes =(('json','*.json'),('all files', '*.*')))
	baseDir = os.path.split(fileName)[0]
	patient = Patient_Presentation(patientTabController, patientDataFile =fileName)
	patientList.append(patient)
	patientTabController.add(patient.tab,text = patient.text)

def AddLab(labName):
	currentPatientTab = patientTabController.index(patientTabController.select())
	currentPatient = patientList[currentPatientTab]
	currentPatient.daily_Updates.fixScroll
	charterSettings.addLab(currentPatient,labName)
def AddImaging():
	currentPatientTab = patientTabController.index(patientTabController.select())
	currentPatient = patientList[currentPatientTab]
	charterSettings.addImaging(currentPatient)
print('Patient Charter, Version alpha. Author: Jake Bergquist')

#Some startup global variables
global baseDir, patientList, patientTabController
patientList = []
baseDir = '/'

mainApp = tk.Tk()
mainApp.geometry('1100x800')
mainApp.title('Patient Presentation Manager')

#menu bar setup
main_menu_bar = tk.Menu(mainApp)
mainApp.config(menu=main_menu_bar)

file_menu_bar = tk.Menu(main_menu_bar)
main_menu_bar.add_cascade(label="File",menu=file_menu_bar)
file_menu_bar.add_command(label = 'New Patient...', command = NewPatient)
file_menu_bar.add_command(label = 'Load Patient...', command = LoadPatient)
file_menu_bar.add_command(label = 'Exit', command = mainApp.quit)

daily_update_bar  = tk.Menu(main_menu_bar)
main_menu_bar.add_cascade(label = "Daily Update", menu = daily_update_bar)
labs_bar = tk.Menu(daily_update_bar)
daily_update_bar.add_cascade(label = 'Add Lab ...', menu = labs_bar)


labs_bar.add_command(label = 'BMP', command = lambda :AddLab('bmp'))
labs_bar.add_command(label = 'CBC', command = lambda :AddLab('cbc'))
labs_bar.add_command(label = 'CMP', command = lambda :AddLab('cmp'))
#daily_update_bar.add_command(label = 'Add Imaging ...', command = AddImaging)

#patient tab setup
patientTabController = ttk.Notebook(mainApp)
#tk.Grid.rowconfigure(mainApp, 0, weight=1)
#tk.Grid.columnconfigure(mainApp, 0, weight=1)
patientTabController.pack(fill='both',expand = True)#grid(row = 0,column = 0, sticky = 'nsew')


if __name__ == '__main__':
	main()

