Repository for the 4th Assignment of Big Data Lab - 8th semester (Jan-May 24). Assignment on working with DVC

## Instructions on how to run
The repository consists of a source folder and a params folder. The dependencies are all stored in requirements.txt. <br />
Use conda create --name my_env --file requirements.txt to create an environment with required libraries. 
### DVC commands
dvc exp show -A to show list of experiments. <br />
dvc exp show --num 4 to show list of experiments for all 4 commits. <br />
dvc exp run -n <expname> to run a new experiment. <br />
can also be done using dvc repro <br /> <br />
Initial experiments had some errors. Hence dvc exp show -A presents some unrequired columns. <br />
Moreover, the experiments of interest (names given) are present in the commit named a9e406f which is 4 commits before latest commit <br /> <br />
dvc dag to visualize the dag <br />
dvc params diff <exp1> <exp2> to view parameter differences between different experiments <br />
### DVC files
dvc.yaml contains the stage details (dependencies, params,outputs and commands for each stage in the pipeline) <br />
dvc.lock contains experiment information <br />
.dvc folder and .dvcignore also present in the repo <br />
The dependencies, outputs and params of each stage is automatically tracked by dvc <br />
## DVC pipeline and experiments
![3](https://github.com/dhan-02/BDL-Assignment4/assets/74642765/38a11c1d-1378-4337-a7cc-6b242dd360ae)
![4](https://github.com/dhan-02/BDL-Assignment4/assets/74642765/a5de0f68-1ce0-4517-bcc8-40a3ef939af0)
![5](https://github.com/dhan-02/BDL-Assignment4/assets/74642765/5d698814-b7fe-4421-b8df-46b32c28dd89)
## Problem Statement
1. Install Git for source control and DVC for source control and pipeline management.
2. Create a blank project in GitHub and check out to a folder. This folder will have the params, source,
data and other outputs. You are expected to checkin all the relevant files to source control.
3. Initiate DVC also from the same folder. Now DVC and Git are linked.
4. Setup the pipeline using “dvc stage add --run -v -f” command to add a stage to the pipeline. Every
time you add a stage, “dvc.yaml” is created/updated in your folder. Also, another file named “dvc.lock”
is also created/updated, which should be tracked in git.
5. Once all the stages are added, use “dvc dag” to visualize the DAG of the pipeline.
6. Run the pipeline using “dvc repro” command. Everytime, you change the parameters, the
pipeline will be run again. You may change the ‘n_locs’, while keeping the ‘year’ constant during
multiple runs. Alternately, you may introduce a dummy variable, say ‘seed: ####’ to the params file
and keep changing only the seed to run multiple rounds. Remember, when the dependencies are
unaltered, the pipeline would skip running. 
7. Use “dvc exp show” to list the runs. 
8. Use “dvc params diff” to compare experiments.
9. Ensure that all the versions of your experiments are correctly checked into DVC and Github.
## Script structure and content
download.py is responsible for downloading valid files (which have suitable fields) <br />
prepare.py extracts the monthly data directly into a csv and also creates a text file with the required daily names <br />
process.py computes the monthly average from the daily data into a csv <br />
evaluate.py computes the r2 values for each field and each location (and gives a csv as the final result) <br /> <br />
The following fields have been used for daily and monthly respectively: 

DailyAverageSeaLevelPressure <br />
DailyAverageStationPressure <br />
DailyMaximumDryBulbTemperature <br />
DailyAverageDryBulbTemperature <br />
DailyMinimumDryBulbTemperature <br /> <br />
MonthlySeaLevelPressure <br />
MonthlyStationPressure	<br />
MonthlyMaximumTemperature <br />
MonthlyMeanTemperature	<br />
MonthlyMinimumTemperature	<br />

## Files of interest
We have 4 script files which are download.py, prepare.py, process.py and evaluate.py  <br />
Two folders which are data and outputs are created while running dvc repro / dvc exp run <br />
data contains n_locs number of csv files and 1 data_store.html file <br />
outputs contains 4 files which are prepare_output.csv, process_output.csv, evaluate_output.csv and daily_fields_list.txt <br />






