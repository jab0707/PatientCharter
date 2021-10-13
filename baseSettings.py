import tkinter as tk
from dataclasses import dataclass
from abc import ABC, abstractmethod
from functools import reduce #magical function that makes recusive object/property calling happen

class basePrintSettings():
	def __init__(self):
		self.tabNameDictionary = {"demographicInfo":self.printDemographicInfo,
								  "dailyUpdates":self.printDailyUpdates,
								  "plan":self.printPlan}

	def printDemographicInfo(self,patient):
		name = patient.demographicInfo.name.get()
		age = patient.demographicInfo.age.get()
		gender = patient.demographicInfo.gender.get()
		pastHistory = patient.demographicInfo.pastHistory.get('1.0',tk.END)
		hisotryOfPresentIllness = patient.demographicInfo.hisotryOfPresentIllness.get('1.0',tk.END)
		useName = 1 if patient.demographicInfo.name.isRelevant.get() == 1 else 0
		useAge = 1 if patient.demographicInfo.age.isRelevant.get() == 1 else 0
		useGender = 1 if patient.demographicInfo.gender.isRelevant.get() == 1 else 0
		usePastHistory = 1 if patient.demographicInfo.pastHistory.isRelevant.get() == 1 else 0
		usePresentHistory = 1 if patient.demographicInfo.hisotryOfPresentIllness.isRelevant.get() == 1 else 0

		demographicInfoString = ''

		if useName == 0:
			name = 'Patient'
		if useGender == 1 or useAge == 1:
			demographicInfoString = demographicInfoString + f"{name} is a "
		else:
			demographicInfoString = demographicInfoString + f"{name} "


		if useAge == 1:
			demographicInfoString = demographicInfoString + f"{age} year old "
		if useGender ==1:
			demographicInfoString = demographicInfoString + f"{gender} "
		if usePastHistory == 1:
			if useAge == 1 or useGender == 1:
				demographicInfoString = demographicInfoString + f"with a past medical history of {pastHistory}\n"
			else:
				demographicInfoString = demographicInfoString + f"has a past medical history of {pastHistory}\n"
		if usePresentHistory == 1:
			demographicInfoString = demographicInfoString + f"{name} presented with {hisotryOfPresentIllness}\n"
		demographicInfoString = demographicInfoString + "\n"
		return demographicInfoString

	def printDailyUpdates(self,patient):
		labNames = patient.dailyUpdates.labs.names
		dailyUpdateString = ''
		if patient.dailyUpdates.tabIsRelevant.get():

			for lab in labNames:
				
				if getattr(patient.dailyUpdates,lab).isRelevant.get():
					dailyUpdateString = dailyUpdateString + getLab(patient,lab)
				pass
		
		return dailyUpdateString
	def printPlan(self,patient):
		return ''

def checkValueAgainstStandard(value,defaultValues):
	if float(value)<defaultValues[0]:
		return '. This value is low.'
	elif float(value)>defaultValues[1]:
		return '. This value is high.'
	else:
		return ''
def pullUnitsFromStructure(structure):
	unitList = []
	for subfield in structure['multifield']:
		if type(subfield) is dict:
			unitList.append(subfield['entry'][2])
	return unitList
def pullLabVals(labVals,labUnits,index):
	if labUnits[index] == '':
		return labVals[index]
	else:
		return f"{labVals[index]} {labUnits[index]}"

@dataclass
class lab():
	entries:list[list]
	structure:dict
	defaultRanges:list[list]
	printer:str

def printCBC(labVals,relevantFlags,labStruct):
	
	defaultValues = labStruct.defaultRanges
	labUnits = pullUnitsFromStructure(labStruct.structure)
	output = ''
	valueIndex = 0
	if relevantFlags[valueIndex] ==1:
		output += f'\n RBC of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n WBC of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Hemoglobin level of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Hematocrit of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Platelet count of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	if output != '':
		output = 'CBC lab results:\n' + output
	return output


cbcLab = lab(entries = ['rbc','wbc','hemoglobin','hematocrit','platelet'],
			structure= {'multifield':['cbc','lab',
							  {'entry':['RBC','','trillion cells/L']},
							  {'entry':['WBC','','billion cells/L']},
							  {'entry':['Hemoglobin','','g/dL']},
							  {'entry':['Hematocrit','','%']},
							  {'entry':['Platelet','','billion/L']}
							  ]},
			defaultRanges=[[0,1],[0,1],[0,1],[0,1],[0,1]],
			printer=printCBC)
def printCMP(labVals,relevantFlags,labStruct):
	defaultValues = labStruct.defaultRanges
	labUnits = pullUnitsFromStructure(labStruct.structure)
	output = ''
	valueIndex = 0
	if relevantFlags[valueIndex] ==1:
		output += f'\n Albumin of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Alkaline of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n ALA level of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n AST of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n BUN of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Calcium of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Chloride of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n CO2 of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Creatine of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Glucose of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Potassium of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Sodium of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Total billirubin of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	valueIndex += 1
	if relevantFlags[valueIndex] ==1:
		output += f'\n Total protein of {pullLabVals(labVals,labUnits,valueIndex)}'
		output += checkValueAgainstStandard(labVals[valueIndex],defaultValues[valueIndex])
	if output != '':
		output = 'CMP lab results:\n' + output
	return output

cmpLab = lab(entries = ['albumin','alkaline','ala','ast','bun',\
						'calcuium','chloride','co2','creatine',	'glucose',\
						'potassium','sodium','totalBillirubin','totalProtein'],
			structure= {'multifield':['cmp','lab',
							{'entry':['Albumin','','']},
							{'entry':['Alkaline','','']},
							{'entry':['ALA','','']},
							{'entry':['AST','','']},
							{'entry':['BUN','','']},
							{'entry':['Calcuium','','']},
							{'entry':['Chloride','','']},
							{'entry':['CO2','','']},
							{'entry':['Creatine','','']},
							{'entry':['Glucose','','']},
							{'entry':['Potassium','','']},
							{'entry':['Sodium','','']},
							{'entry':['Total Billirubin','','']},
							{'entry':['Total Protein','','']},
							]},
			defaultRanges=[[0,1],[0,1],[0,1],[0,1],
							[0,1],[0,1],[0,1],[0,1],
							[0,1],[0,1],[0,1],[0,1],
							[0,1],[0,1]],
							printer=printCMP)

def printBMP(bmpValues,defaultValues,relevantFlags):
	return ''
bmpLab = lab(entries = ['stuff1','stuff2'],
			structure= {'multifield':['bmp','lab',
							  {'entry':['Stuff1','','']},
							  {'entry':['Stuff2','','']}
							  ]},
			defaultRanges=[[0,1],[0,1]],
			printer=printBMP)



_labDict = {'cbc':cbcLab,
				'cmp':cmpLab,
				'bmp':bmpLab}

def getLab(patient,labFullName):
	values = []
	relevantFlags = []
	labName,labNumber = labFullName.split('_')
	for entry in _labDict[labName].entries:
		values.append(getattr(patient.dailyUpdates,entry + f"_{labNumber}").get())
		relevantFlags.append(reduce(getattr,['dailyUpdates',entry + f"_{labNumber}",'isRelevant'],patient).get())
		
	##implement calling the right print statement
	return _labDict[labName].printer(values,relevantFlags,_labDict[labName])
	

def addLab(patient,labName):			
	

	patient.dailyUpdates.labs.number = patient.dailyUpdates.labs.number + 1
	#Check if any of the existing labs share a name with this one
	sameLabs = [oldLabName for oldLabName in patient.dailyUpdates.labs.names if labName in oldLabName]
	#if they do, update the number of the current lab
	labNum =1
	if sameLabs:
		for oldLab in sameLabs:
			oldNum = int(oldLab.split('_')[1])
			if oldNum >= labNum:
				labNum = oldNum + 1
	addedField = patient.dailyUpdates.addField(_labDict[labName].structure, "_" + str(labNum))
	patient.dailyUpdates.labs.names.append(labName + '_' + str(labNum))
	patient.dailyUpdates.fields.append(addedField)

def addImaging(patient):
	pass

def addProblem(patient):
	pass


class patientPrinter(basePrintSettings):
	def __init__(self):
		super(patientPrinter, self).__init__()	

