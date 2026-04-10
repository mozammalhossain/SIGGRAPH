import os

import pandas as pd

class surveyDataPrepartion():
    
    def __init__(self,fileName:str):
        self.fileExtension = '.csv'
        self.fileTypes=['Values', 'Labels']
        self.fileStatuses = ['complete', 'incomplete']
        self.groups = [1,2]
        self.fileNameList = []
        self.survey_data = pd.DataFrame()
        self.fileReadFlag = True
        self.baseFileName = fileName #'Visual_FactSheet_Live_'


    def checkLocation(self, location: str):
        if not os.path.exists(location):
            os.makedirs(name=location, exist_ok=True)


    def processSurveyFile(self):

        for fileType in self.fileTypes:
            
            sourceFileLocationName = self.baseFileName + fileType + self.fileExtension
            
            fileLocation = fileType + '/'
            saveFileLocation =''
            
            if self.fileReadFlag:
                survey_data = pd.read_csv(sourceFileLocationName, skiprows=[1,2])
                survey_data = survey_data[(survey_data['DistributionChannel'] == 'anonymous') | (survey_data['DistributionChannel'] == 'qr')]
                
                self.fileReadFlag = False

            for fileStatus in self.fileStatuses:
                if fileStatus == 'complete':
                    competeSurvey = survey_data[survey_data['Progress'] == 100]
                    saveFileLocation = fileLocation + fileStatus + '/'
                    saveFileLocationName= saveFileLocation + fileStatus + '_survey_' + fileType + self.fileExtension
                    self.checkLocation(saveFileLocation)
                    competeSurvey.to_csv(saveFileLocationName, index=False)

                    for group in self.groups:
                        groupFileLocationName= saveFileLocation + fileStatus + '_group_' + str(group) + '_data_' + fileType + self.fileExtension
                        self.checkLocation(saveFileLocation)
                        self.fileNameList.append(groupFileLocationName)
                        group_data = competeSurvey[competeSurvey['Group'] == group]
                        group_data.to_csv(groupFileLocationName, index=False)
                
                else:
                    incompeteSurvey = survey_data[survey_data['Progress'] != 100]
                    saveFileLocation= fileLocation + fileStatus + '/'
                    saveFileLocationName= saveFileLocation + fileStatus + '_survey_' + fileType + self.fileExtension
                    self.checkLocation(saveFileLocation)
                    incompeteSurvey.to_csv(saveFileLocationName, index=False)

                    for group in self.groups:
                        groupFileLocationName= saveFileLocation + fileStatus + '_group_' + str(group) + '_data_' + fileType + self.fileExtension
                        self.checkLocation(saveFileLocation)
                        self.fileNameList.append(groupFileLocationName)
                        group_data = incompeteSurvey[incompeteSurvey['Group'] == group]
                        group_data.to_csv(groupFileLocationName, index=False)