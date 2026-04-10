import configparser

import Survey_Data_Prepartion as SDP
import Survey_Data_Visualization as SDV


def main_menu(sourceFile:str, processedFile:str, outputFileLocation:str):
    while True:
        print("\n--- PROGRAM MENU ---")
        print("1. Process Survey File")
        print("2. Process Demography Data")
        print("3. Process ToC Reading Time Data")
        print("4. Process ToC Question Data")
        print("5. Process TLX Data")
        print("6. Process User Concern Data")
        print("7. Process ToC Understaing and Rating Data")
        print("0. Exit")
        
        
        choice = input("Enter your choice: ")

        match choice:
            case '0':
                break
            case '1':
                dataPreparation = SDP.surveyDataPrepartion(fileName=sourceFile)
                dataPreparation.processSurveyFile()
                print("Data Processing Complete")
            case '2':
                print("1. Process Educataion Data")
                print("2. Process Gender Data")
                print("3. Process Age Data")
                print("4. Process Question Data")
                print("5. Return to Previous Menu")
                
                dmChoice = input("Enter your choice: ")

                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=True)

                match dmChoice:
                    case '1':
                        dataVisualization.processDemographyEduction()
                    case '2':
                        dataVisualization.processDemographyGender()
                    case '3':
                        dataVisualization.processDemographyAge()
                    case '4': 
                        dataVisualization.processDemographyQuestion()
                    case '5':
                        print("Returning to previous ment")
                    case _:
                        print("Invalid choice. Please try again.")
            case '3':
                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=True)
                dataVisualization.processToCTime()
            case '4':
                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=True)
                dataVisualization.processToCQuestion()
            case '5':
                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=True)
                dataVisualization.processTLXQuestions()
            case '6':
                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=True)
                dataVisualization.processDataConcern()
            case '7':
                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=True)
                dataVisualization.processTocUnderstandingRating()
            case '8':
                dataVisualization = SDV.processAndVisualizeSurveyData(sourceFile=processedFile, outputFilePath=outputFileLocation,diplayFlag=False)
                dataVisualization.processDemographyEduction()
                dataVisualization.processDemographyGender()
                dataVisualization.processDemographyAge()
                dataVisualization.processDemographyQuestion()
                dataVisualization.processToCTime()
                dataVisualization.processToCQuestion()
                dataVisualization.processTLXQuestions()
                dataVisualization.processDataConcern()
                dataVisualization.processTocUnderstandingRating()
            case _:
                print("Invalid choice. Please try again.")
    
    print("END")

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')

    sLocation = config['sourcefile']['sourceFileLocation']
    sName = config['sourcefile']['sourceFileName']
    pLocationName = config['sourcefile']['processedFileLocation']

    sourceFileLocationName = sLocation + sName

    oLocation = config['outputfile']['outputFileLocation']

    print(sourceFileLocationName)
    print(oLocation)

    main_menu(sourceFile=sourceFileLocationName, processedFile=pLocationName, outputFileLocation=oLocation)
