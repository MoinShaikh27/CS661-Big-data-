## Instructions

The code base consists of the following 2 folders:

1. ISOCONTOUR_Q1 : This corresponds to the first question
2. VOLUME_RENDERING : This corresponds to the second question

### ISOCONTOUR_Q1

The folder consists of the following files:

1. Assign1_Q1.py - The actual code
2. config.py - Configuration file which contains the data folder path and file name
3. Data - This folder contains the input for this question

### VOLUME_RENDERING

The folder consists of the following files:

1. Assign1_Q2.py - The actual code
2. config.py - Configuration file which contains the data folder path and file name
3. Data - This folder contains the input for this question

### Additional Files

1. requirements.txt - contains all the requirements to be installed to run the code base

## How To RUN

The following steps can be used to run the code

1. Open a terminal within the <Submission_Assignment1> folder
2. Install the modules required using requirements file

    > pip install -r ./requirements.txt

3. The user inputs are obtained from within the code and the expected user input is described in the input prompt. 
4. To run each of the questions:

#### ISOCONTOUR

1. The code can be run from either within the Assignment folder or from within the ISOCONTOUR_Q1 folder. The path has been handled within the config file.

    > python ./ISOCONTOUR_Q1/Assign1_Q1.py

2. The code would be running in an infinite loop and for each run the user would be asked to enter the iso value. Once the user enters, the file is generated and saved in the current folder itself along with the iso value.
3. In addition to this a render window is also opened which would contain the iso contour on top of the input data.
4. Once this render window is closed the loop would go onto the next iteration.
5. In order to end the loop we can just enter a character which would terminate the loop.


#### VOLUME RENDERING

1. The code can be run from either within the Assignment folder or from within the VOLUME_RENDERING folder. The path has been handled within the config file.

    > python ./VOLUME_RENDERING/Assign1-Q2.py

2. The code would ask for the user whether to enable Phong shading.
3. Once the user input is received, the corresponding output is created on the render window.


