
import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from scipy import stats

class processAndVisualizeSurveyData:

    def __init__(self,sourceFile:str, outputFilePath:str, diplayFlag:bool):
        self.file_save_location = outputFilePath
        self.source_file_location = sourceFile
        self.showFlag = diplayFlag

        self.checkLocation(self.file_save_location)

    
    def checkLocation(self, location: str):
            if not os.path.exists(location):
                os.makedirs(name=location, exist_ok=True)
    
    def createshowplot(self, grapdata,plottitle, savelocation,graphLebel,myLegend,myLegendTitle,myboxColor,mylegendColor,mylegendAnchor,myFigureSize):
        
        fig, ax = plt.subplots()
        bp = ax.boxplot(grapdata, patch_artist=True, tick_labels=graphLebel, showfliers=False)
        for patch, color in zip(bp['boxes'], myboxColor):
            patch.set_facecolor(color)

        for median in bp['medians']:
            median.set(color='orange', linewidth=2)

        plt.grid(True, axis='y', linestyle='-')

        legend_handles = [mpatches.Patch(color=colors_legend, label=label) for colors_legend, label in zip(mylegendColor, myLegend)]
        ax.legend(handles=legend_handles, loc='upper right', title=myLegendTitle, bbox_to_anchor=mylegendAnchor)

        fig.set_size_inches(myFigureSize)
        fig.savefig(fname=savelocation, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)
        
        if self.showFlag:
            plt.show()

    def processTLXQuestions(self):
        title = " Mental Demand Interpreting ToC"
        filename = 'TLX.pdf'

        question_list = ['Q10.4','Q20.4','Q10.5','Q20.5','Q10.6','Q20.6','Q10.7','Q20.7','Q10.8','Q20.8','Q10.9','Q20.9']
        my_tick_labels=['Text', 'Visual','Text', 'Visual','Text', 'Visual','Text', 'Visual','Text', 'Visual','Text', 'Visual']
        clr_legend = ['Question 1', 'Question 2', 'Question 3','Question 4', 'Question 5', 'Question 6']

        plotColors = ['olive', 'olive', 'forestgreen', 'forestgreen','cornflowerblue', 'cornflowerblue','mediumpurple', 'mediumpurple', 'lightseagreen','lightseagreen','darkgrey','darkgrey']
        plotColors_legend = ['olive', 'forestgreen', 'cornflowerblue', 'mediumpurple', 'lightseagreen','darkgrey']

        legendAnchor = (1.18, 1)
        figureSize = (10, 6)

        clr_legend_title='TLX Questions'
        savefile = self.file_save_location + filename

        df_subset = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=question_list)

        df_subset_list = df_subset.T.values.tolist()

        self.createshowplot(grapdata=df_subset_list,plottitle=title,
                    savelocation=savefile,graphLebel=my_tick_labels,
                    myLegend=clr_legend,myLegendTitle=clr_legend_title,
                    myboxColor=plotColors, mylegendColor=plotColors_legend,
                    mylegendAnchor=legendAnchor,myFigureSize=figureSize)
        
    def processDemographyGender(self):
        colA = 'Q4.2'
        filename = 'Gender.pdf'
        savefile = self.file_save_location + filename

        df_gender = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=[colA])

        subjects_map = {1: "Male", 2: "Female", 3: "Non-binary" }

        df_gender["education"] = df_gender["Q4.2"].map(subjects_map)

        df_grouped = df_gender.groupby('education').count()

        ax = df_grouped.plot(kind='bar', legend=False)
        ax.tick_params(axis='x', labelrotation=0)
        for container in ax.containers:
            ax.bar_label(container)
        plt.xlabel(None)
        plt.ylabel('Count')
        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)

        if self.showFlag:
            plt.show()

    def processDemographyAge(self):
        colA = 'Q4.3'

        filename = 'Age.pdf'
        savefile = self.file_save_location + filename

        df_age = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=[colA])

        bins = range(20, df_age[colA].max() + 11, 10)
        labels = [f'{i}-{i+9}' for i in bins[:-1]]
        df_age['age_group'] = pd.cut(df_age[colA], bins=bins, labels=labels, right=False)

        age_counts = df_age.groupby('age_group').size()

        ax = age_counts.plot(kind='bar', legend=False)
        ax.tick_params(axis='x', labelrotation=0)
        for container in ax.containers:
            ax.bar_label(container)
        plt.xlabel(None)
        plt.ylabel('Count')
        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)
        # plt.axvline(x=2.5, color='gray', linestyle='--', linewidth=1)
        if self.showFlag:
            plt.show()

    def processDemographyEduction(self):
        colA = 'Q4.4'
        filename = 'Eductaion.pdf'
        savefile = self.file_save_location + filename
        df_edu = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=[colA])

        subjects_map = {7: "Bachelor", 8: "Graduate", 6: "Some University" }

        df_edu["education"] = df_edu[colA].map(subjects_map)

        df_grouped = df_edu.groupby('education').count()

        ax = df_grouped.plot(kind='bar', legend=False)
        ax.tick_params(axis='x', labelrotation=0)
        for container in ax.containers:
            ax.bar_label(container)
        plt.xlabel(None)
        plt.ylabel('Count')
        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)
        
        if self.showFlag:
            plt.show()

    def processDemographyQuestion(self):
        question_list = ['Q4.6_1','Q4.6_2','Q4.6_3','Q4.6_4']

        filename = 'Demograpy_question.pdf'
        savefile = self.file_save_location + filename

        df_question = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=question_list)
        combined_df = pd.DataFrame()
        for item in question_list:
            count= df_question.groupby(item).size()

            temp = pd.DataFrame()
            temp = count.to_frame().T
            temp.reset_index(inplace=True)
            temp['index'] = item
            combined_df = pd.concat([combined_df, temp], ignore_index=True)

        combined_df = combined_df.fillna(0)
        combined_df = combined_df.convert_dtypes()
        combined_df = combined_df.rename(columns={"index": "Question", 1: "True", 2: "False", 3: "NotSure"})

        categories = ['Computer\nSmart Phone','Search\nEngine', 'Social\nMedia', 'AI\nAssistant']
        values = combined_df['True'].tolist()
        values1 = combined_df['False'].tolist()
        bar_width = 0.50
        x_positions = np.arange(len(categories))
        fig, ax = plt.subplots()
        a = ax.bar(categories, values,label='Yes',width=bar_width)
        b = ax.bar(categories, values1,label='No',width=bar_width)
        plt.legend()

        ax.bar_label(a, fmt='{:,.0f}')
        ax.bar_label(b, fmt='{:,.0f}')
        ax.locator_params(axis='y', integer=True) 

        ax.set_ylabel('Count')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(categories)
        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)
        
        if self.showFlag:
            plt.show

    def processToCTime(self):
        title = "Time Taken Reviewing ToC"
        filename = 'ToCReadingTime.pdf'
        savefile = self.file_save_location + filename

        click_list = ['Q7.4_First Click', 'Q7.4_Page Submit','Q17.4_First Click', 'Q17.4_Page Submit']

        df_time = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=click_list)
        df_time['text'] = df_time[click_list[1]]
        df_time['vfs'] = df_time[click_list[3]]

        plt.plot(df_time['text'].tolist(), c='blue', label='Text ToC', marker='o',linestyle='None')
        plt.plot(df_time['vfs'].tolist(), c='orange', label='Visual ToC', marker='s',linestyle='None')
        plt.legend()
        plt.ylabel("Time (Millisecond)")
        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)
        
        if self.showFlag:
            plt.show()

    def _processToCQuestionData(fileLocation, questionList) -> pd.DataFrame:
        df_question = pd.read_csv(filepath_or_buffer=fileLocation, usecols=questionList)
        combined_df = pd.DataFrame()
        for item in questionList:
            count= df_question.groupby(item).size()

            temp = pd.DataFrame()
            temp = count.to_frame().T
            temp.reset_index(inplace=True)
            temp['index'] = item
            combined_df = pd.concat([combined_df, temp], ignore_index=True)

        combined_df = combined_df.fillna(0)
        combined_df = combined_df.convert_dtypes()
        combined_df = combined_df.rename(columns={"index": "Question", 1: "True", 2: "False", 3: "NotSure"})

        return combined_df
    
    def processToCQuestion(self):
        question_list_T = ['Q9.2_1','Q9.2_2','Q9.2_3','Q9.2_4','Q9.2_5','Q9.2_6','Q9.2_7']
        question_list_V = ['Q19.2_1','Q19.2_2','Q19.2_3','Q19.2_4','Q19.2_5','Q19.2_6','Q19.2_7']

        filename = 'ToC_Test_Question.pdf'
        savefile = self.file_save_location + filename

        text_df = self._processToCQuestionData(fileLocation=self.source_file_location,questionList=question_list_T)
        visusl_df = self._processToCQuestionData(fileLocation=self.source_file_location,questionList=question_list_V)

        categories = ['Text  Visual\n\nQuestion 1','Text  Visual\n\nQuestion 2','Text  Visual\n\nQuestion 3','Text  Visual\n\nQuestion 4',
                    'Text  Visual\n\nQuestion 5','Text  Visual\n\nQuestion 6','Text  Visual\n\nQuestion 7']

        bar_width = 0.25
        fig, ax = plt.subplots(figsize=(10, 6))

        ax1 = text_df.plot(kind='bar', stacked=True, ax=ax, width=bar_width, position=1.1, legend=True)


        ax2 = visusl_df.plot(kind='bar', stacked=True, ax=ax, width=bar_width, position=-0.1, legend=True, color=['mediumpurple', 'sienna','orchid'])

        for container in ax.containers:
            ax.bar_label(container, label_type='center')
            
        ax.set_ylabel('Count')

        ax.set_xticklabels(categories)
        ax.tick_params(axis='x', labelrotation=0)
        ax.legend(loc='upper right',  bbox_to_anchor=(1.15, 1))
        ax.set_ylim(bottom=0, top=22)
        ax.set_xlim(-0.5, 6.5)
        ax.locator_params(axis='y', integer=True) 
        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)

        if self.showFlag:
            plt.show()
 
    def processDataConcern(self):
    
        title = " Concern"
        filename = 'Concern.pdf'
        savefile = self.file_save_location + filename

        colors_legend = ['mediumpurple', 'forestgreen', 'cornflowerblue', 'olive']

        question_list = ['Q23.2','Q23.3','Q23.4','Q23.5']
        

        df_subset = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=question_list)

        df_subset_list = df_subset.T.values.tolist()

        fig, ax = plt.subplots()
        bp = ax.boxplot(df_subset_list, patch_artist=True, showfliers=False,tick_labels=['Data Collection\nand Usage', 
                                                                                         'Personal Data\nProcessing', 
                                                                                         'Data Selling',
                                                                                         'ML Accuracy\nand Fairness'])

        for patch, color in zip(bp['boxes'], colors_legend):
            patch.set_facecolor(color)
            for median in bp['medians']:
                median.set(color='orange', linewidth=2)

            plt.grid(True, axis='y', linestyle='-')

            fig.set_size_inches(10, 6)

        plt.savefig(fname=savefile, format='pdf', dpi=300,bbox_inches='tight', pad_inches=0)

        if self.showFlag:
            plt.show

    def calculateTLXStatistics(self):
        question_list_T = ['Q10.4','Q10.5','Q10.6','Q10.7','Q10.8','Q10.9']
        question_list_V = ['Q20.4','Q20.5','Q20.6','Q20.7','Q20.8','Q20.9']

        df_subset_T = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=question_list_T)
        df_subset_V = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=question_list_V)

        df_subset_list_T = df_subset_T.values.tolist()
        df_subset_list_V = df_subset_V.values.tolist()

        t_statistic, p_value = stats.ttest_ind(df_subset_list_T, df_subset_list_V)

        if self.showFlag:

            resultFileName = self.savefile+ 'tTestResult.txt'

            with open(resultFileName, "w+") as file:

                file.write(f'T-statistic for TLX: {t_statistic}\n')
                file.write(f'P-value for TLX: {p_value}\n')
        else:
            print(f'T-statistic for TLX: {t_statistic}\n')
            print(f'P-value for TLX: {p_value}\n')

    def processTocUnderstandingRating(self):
        title = "Confidence Understanding ToC Agreement"
        filename = 'Understanding_RatingToC.pdf'

        question_list = ['Q8.8','Q18.8','Q23.7_1','Q23.7_2']
        my_tick_labels=['Text', 'Visual','Text', 'Visual']
        clr_legend = ['Understing', 'Rating']

        plotColors = ['olive', 'olive', 'forestgreen', 'forestgreen']
        plotColors_legend = ['olive', 'forestgreen']

        legendAnchor = (1.22, 1)
        figureSize = (8, 6)

        clr_legend_title=''

        savefile = self.file_save_location + filename

        df_subset = pd.read_csv(filepath_or_buffer=self.source_file_location, usecols=question_list)
        df_subset_list = df_subset.T.values.tolist()

        self.createshowplot(grapdata=df_subset_list,plottitle=title,
                    savelocation=savefile,graphLebel=my_tick_labels,
                    myLegend=clr_legend,myLegendTitle=clr_legend_title,
                    myboxColor=plotColors, mylegendColor=plotColors_legend,
                    mylegendAnchor=legendAnchor,myFigureSize=figureSize)