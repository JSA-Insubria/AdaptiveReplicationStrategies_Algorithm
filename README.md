# OptimalReplicationStrategies_Algorithm

***OptimalReplicationStrategies_Algorithm*** is a tool that allows optimizing the location of the replicas in a distributed management system.
In particular, this tool is adapted to work in a system based on a custom version of [Apache Hadoop](https://github.com/JSA-Insubria/hadoop.git) and [Apache Hive](https://github.com/JSA-Insubria/hive.git).

The tool is split into two different packages.
- ***solver*** - the optimization algorithm.
- ***benchmark*** - the benchmark tool.

### solver
The optimization algorithm takes as input some specific data retrieved from a Hadoop cluster.
This data includes the location of the replicas in the cluster, the characteristics of the cluster nodes, and the queries that have been run on the cluster. 
It is possible to find an example of the data in the data folder.
The tool retrieves a file called 'FilesLocation.txt' that contains the new optimized location for the replicas of the data, optimized by the solver based on the queries that have been executed.
We use two different solvers, *CPLEX* and *Gurobi*.

### benchmark
The benchmark tool takes input data from the execution of the queries, like the execution time, the cumulative CPU time, and the blocks that the queries have used.
The tool generates three different CSV files in the data folder that can be used for future plots. Files are:
- ***cpu_time.csv***, which contains the cumulative CPU time for each query.
- ***execution_time.csv***, which contains the execution time for each query.
- ***transfer_time.csv***, which contains, for each query, the cumulative time that the system uses to move blocks during queries execution.
It also contains the number of moved blocks and the cumulative size of these blocks.

## Setup
The tool requires Python3.
To install the tool is necessary to clone the repository manually.
```
git clone https://github.com/JSA-Insubria/OptimalReplicationStrategies_Algorithm.git
```
It requires libraries that can be installed using the requirements.txt file.
```
pip install -r requirements.txt
```
It is possible to change the data folder, changing the path in *solver/main.py* and *benchmark/main.py* files. 

## Data
The data folder contains a sample of the data the tool requires.
In particular, these data must be split into folders, where each folder represents a query.
Each query folder must have a name built in the following way: ***n*** is a number representing a specific query, and ***s*** is the repetition of the query.
```
Qn_s
```

Each folder contains two sub-folder, the *results*, and the *nodes_results*.
- The *results* folder contains data retrieved from the *Hadoop namenode*. In particular, it contains details regarding the query run in the cluster like its tables, execution time, and CPU time.
- The *nodes_results* folder contains folders with data retrieved from the *datanodes*. In particular, it contains information regards the blocks that are moved between datanodes during the query execution. 

The data folder also contains the system-info folder that contains two sub-folders.
- The *FilesInfo* folder containing information regarding all the files present in the cluster, their location, and their size.
- The *Clusterinfo* folder containing information regards the nodes that compose the cluster, like their capacity, their IP, etc.

This structure is automatically obtained using the following *Apache Hadoop* and *Apache Hive* custom versions.
```
Apache Hadoop: https://github.com/JSA-Insubria/hadoop.git
Apache Hive: https://github.com/JSA-Insubria/hive.git
```

## Run
### solver
The solver includes a *main.py* file that allows executing the tool.
```
python3 solver/main.py
```

Otherwise, it is possible to build its main.py. It is necessary to implement the following steps.
```python
import read_data
import matrix
import model
import model_gurobi
import plot
import os

# Setting the data path
path = '.' + os.sep + 'data' + os.sep + '5g-test1'

# retrieve data about nodes, files and queries
df_nodes = read_data.get_nodes_data(path)
df_files = read_data.get_files_data(path)
df_query = read_data.get_queries_data(path)

# build the co-occurrence matrix necessary to the model
history_matrix = matrix.get_history_matrix(df_files, df_query)
co_occurrence_matrix = matrix.get_co_occurrence_matrix(history_matrix)

# run CPLEX model
model.build_model(df_nodes, df_files, co_occurrence_matrix)

# run Gurobi model
model_gurobi.build_model(df_nodes, df_files, co_occurrence_matrix)
```

#### models
Is it possible to set the ***Time Limit*** for both the models.

For the ***CPLEX*** model is necessary to modify the following line in the *solver/model.py* file.
In the following we present different setting to limit the solver.
```python
# run until the model find the bst solution
solve = model.solve()
# run until the model 10 SolutionLimit 
solve = model.solve(SolutionLimit=10)
# run until the model reach 600 seconds
solve = model.solve(TimeLimit=600)
# run until the model find 1 solution or reach 600 seconds.
solve = model.solve(SolutionLimit=1, TimeLimit=600)
```

For the ***Gurobi*** model is necessary to modify the following line in the *model_gurobi.py* file.
In the following, we present different settings to limit the solver.
```python
# run until the model 10 SolutionLimit 
model.Params.SolutionLimit = 10
# run until the model reach 600 seconds
model.Params.TimeLimit = 600
# optimize
model.optimize()
```

### benchmark
The benchmark package includes a *main.py* file that allows executing the tool.
```
python3 solver/main.py
```

Otherwise, it is possible to build its main.py. It is necessary to implement the following steps.
```python
import os
import solver.read_data as rd
import transfer_time
import execution_time
import cpu_time

# Setting the data path
path = '..' + os.sep + 'data' + os.sep + '5g-test1'
os.mkdir(path + os.sep + 'benchmark')

# retrieve data about nodes and files
df_nodes = rd.get_nodes_data(path)
df_files = rd.get_files_data(path)

# compute the metrics from the data
df_transfer_time = transfer_time.get_transfer_time(path, df_nodes, df_files)
df_execution_time = execution_time.get_execution_time(path)
df_cpu_time = cpu_time.get_cpu_time(path)
```
