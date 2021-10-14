import tkinter as tk
from dataclasses import dataclass
from abc import ABC, abstractmethod
from functools import reduce #magical function that makes recusive object/property calling happen

class basePrintSettings():
	def __init__(self):
		self.tabNameDictionary = {"demographic_Info":self.printDemographicInfo,
								  "daily_Updates":self.printDailyUpdates,
								  "plan":self.printPlan}

	def printDemographicInfo(self,patient):
		name = patient.demographic_Info.name.get()
		age = patient.demographic_Info.age.get()
		gender = patient.demographic_Info.gender.get()
		pastHistory = patient.demographic_Info.past_History.get('1.0',tk.END)
		hisotryOfPresentIllness = patient.demographic_Info.hisotry_Of_Present_Illness.get('1.0',tk.END)
		useName = 1 if patient.demographic_Info.name.isRelevant.get() == 1 else 0
		useAge = 1 if patient.demographic_Info.age.isRelevant.get() == 1 else 0
		useGender = 1 if patient.demographic_Info.gender.isRelevant.get() == 1 else 0
		usePastHistory = 1 if patient.demographic_Info.past_History.isRelevant.get() == 1 else 0
		usePresentHistory = 1 if patient.demographic_Info.hisotry_Of_Present_Illness.isRelevant.get() == 1 else 0

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
		labNames = patient.daily_Updates.labs.names
		dailyUpdateString = ''
		if patient.daily_Updates.tabIsRelevant.get():

			for lab in labNames:
				
				if getattr(patient.daily_Updates,lab).isRelevant.get():
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
		output = '\nCBC lab results:' + output
	return output


cbcLab = lab(entries = ['rbc','wbc','hemoglobin','hematocrit','platelet'],
			structure= {'multifield':['cbc','lab',
							  {'entry':['RBC','0','trillion cells/L']},
							  {'entry':['WBC','0','billion cells/L']},
							  {'entry':['Hemoglobin','0','g/dL']},
							  {'entry':['Hematocrit','0','%']},
							  {'entry':['Platelet','0','billion/L']}
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
		output = '\nCMP lab results:' + output
	return output

cmpLab = lab(entries = ['albumin','alkaline','ala','ast','bun',\
						'calcuium','chloride','co2','creatine',	'glucose',\
						'potassium','sodium','total_Billirubin','total_Protein'],
			structure= {'multifield':['cmp','lab',
							{'entry':['Albumin','0','']},
							{'entry':['Alkaline','0','']},
							{'entry':['ALA','0','']},
							{'entry':['AST','0','']},
							{'entry':['BUN','0','']},
							{'entry':['Calcuium','0','']},
							{'entry':['Chloride','0','']},
							{'entry':['CO2','0','']},
							{'entry':['Creatine','0','']},
							{'entry':['Glucose','0','']},
							{'entry':['Potassium','0','']},
							{'entry':['Sodium','0','']},
							{'entry':['Total Billirubin','0','']},
							{'entry':['Total Protein','0','']},
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
							  {'entry':['Stuff1','0','']},
							  {'entry':['Stuff2','0','']}
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
		values.append(getattr(patient.daily_Updates,entry + f"_{labNumber}").get())
		relevantFlags.append(reduce(getattr,['daily_Updates',entry + f"_{labNumber}",'isRelevant'],patient).get())
		
	##implement calling the right print statement
	return _labDict[labName].printer(values,relevantFlags,_labDict[labName])
	

def addLab(patient,labName):			
	

	patient.daily_Updates.labs.number = patient.daily_Updates.labs.number + 1
	#Check if any of the existing labs share a name with this one
	sameLabs = [oldLabName for oldLabName in patient.daily_Updates.labs.names if labName in oldLabName]
	#if they do, update the number of the current lab
	labNum =1
	if sameLabs:
		for oldLab in sameLabs:
			oldNum = int(oldLab.split('_')[1])
			if oldNum >= labNum:
				labNum = oldNum + 1
	addedField = patient.daily_Updates.addField(_labDict[labName].structure, "_" + str(labNum))
	patient.daily_Updates.labs.names.append(labName + '_' + str(labNum))
	patient.daily_Updates.fields.append(addedField)

def addImaging(patient):
	pass

def addProblem(patient):
	pass


class patientPrinter(basePrintSettings):
	def __init__(self):
		super(patientPrinter, self).__init__()	

