import tkinter as tk

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
		
		
		return ''
	def printPlan(self,patient):
		return ''

class patientPrinter(basePrintSettings):
	def __init__(self):
		super(patientPrinter, self).__init__()	



def addLab(patient,labName):
	_cbc = {'multifield':['cbc','lab',
							  {'entry':['RBC','','']},
							  {'entry':['WBC','','']},
							  {'entry':['Hemoglobin','','']},
							  {'entry':['Hematocrit','','']},
							  {'entry':['Platelet','','']}
							  ]}
	_cmp = {'multifield':['cmp','lab',
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
							]}
	_bmp = {'multifield':['bmp','lab',
							  {'entry':['Stuff','','']},
							  {'entry':['Stuff','','']}
							  ]}			
	_labDict = {'cbc':_cbc,
				'cmp':_cmp,
				'bmp':_bmp}

	patient.dailyUpdates.labs.number = patient.dailyUpdates.labs.number + 1
	addedField = patient.dailyUpdates.addField(_labDict[labName], "_" + str(patient.dailyUpdates.labs.number))
	patient.dailyUpdates.labs.names.append(addedField)
	patient.dailyUpdates.fields.append(addedField)

def addImaging(patient):
	pass

def addProblem(patient):
	pass
