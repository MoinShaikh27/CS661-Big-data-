# CS738_Big_Data_Project_IITK

The repo consists of the Code base for the 2019 Indian Election Visual Analysis Dashboard we have created as part of Course CS738. The repo has been structure in the following manner.

1. The dashboard can be started via either the notebook "Solution_Notebook_Sabari.ipynb" or via the python script "script.py"
2. The requirements for running the dashboard has been noted in the requirements.txt file along with the versions of the modules.
3. The dataset was taken from Kaggle and was processed over to create the final dataset. Parts of the processing done was done via code while some part was done manually. The EDA and processing which was done on the original data is available with the EDA folder.
4. The final processed dataset which is being used is the "modified_dataset.csv" file.
5. All the utilities for the various plots is available within the Utils folder which has been named based on the members who helped to implement these components. The components and their associated code can be available as follows:

   > Moin - Contains the mapping for the State to the Zone which is being used in the Zone based plots

   > Hemang - Contains the code for Parallel Coordinates Plot

   > Shubham - Contains the code for the Choropleth plots as well as the plot which shows the number of constituencies won by party
   
   > Sabari - Contains the code for the party based analysis plots based on Gender, Category, Age and Education.

6. Other than these, the dash dashboard structure along with the callbacks and the code for other components is available within the notebook/script itself.
7. The script is a python script and can be executed via "python ./script.py" after creating a venv with the requirements provided.
