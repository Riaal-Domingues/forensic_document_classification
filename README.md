Exploring Information Retrieval by Applying Topic Analysis to Email Forensics
==============================

The project is the code that is referenced by the mini-dissertation with the same title. The mini-dissertation is currently submitted for examination for MIT 807, at the University of Pretoria.  

The mini-dissertation abstract is repeated here for convenience:

__Abstract__
Digital forensic investigators are faced with an increasing number of emails that needs to be processed to find evidence. Examples of such cases are Enron, and more recently, the Gupta leaked emails.

Topic modelling has been proposed in the past as an aid to investigators in finding evidence. Past proposals focussed on displaying word clouds, or topic words in the flow of email between parties. However, past proposals do not deal with the factors that affect the optimality of the performance of topic modelling in the context of emails. Past proposals also do not deal with the detail of making the topic modelling useful to the digital forensic investigators to extract specific emails of interest. This leads to the main research question in this mini-dissertation: Which factors need to be considered to optimise natural language processing of email bodies for digital forensic investigations?

This mini-dissertation proposes combining topic modelling, specifically the Latent Dirichlet Allocation algorithm, with information retrieval. An investigator uses an email, or typed piece of text as a query to the information retrieval system. Specific emails that are a topical match to the query are extracted from the dataset of emails, ranked and then presented in the ranked order to the investigator for consideration.

The feasibility of implementing such a solution is investigated on the Enron dataset through four experiments. Experiment 1 investigates the pre-processing required that are unique to emails for topic modelling. Experiment 2 investigates whether there is a strong relation between topic coherence scores, and precision and recall metric performance of the proposed solution. It was  found that topic coherence scores are not optimal in selecting the number of topics for the proposed solution. Experiment 3 investigates the precision and recall metric performance of the proposed solution by training and scoring emails on paragraph level instead of email level. It was found that a combination of training the topic modelling algorithm on email level, while scoring on paragraph level for retrieval, is more optimal. Finally, experiment 4 investigates the possibility of training the topic modelling algorithm on a small number of emails of interest. It was found that this approach performs poorly under precision and recall metrics.
The experiments show that it is feasible to implement an information retrieval system for email forensics. This approach enables the forensic investigator to search for specific emails of interest, based on reference emails of interest instead of a keyword only search approach. The proposal improves on previous attempts which only indicated to the investigator which topics are contained in the emails, but did not directly retrieve relevant emails.

# Getting started
## Getting this repository
The easiest way to get the code, is to clone this repository to your own computer. The entire structure, including this document, will be accessible locally.

## Software environment
This code was written in Python and, like all Python code, is heavily dependant on third party libraries. Most of the third party libraries can be installed using pip. The requirements.txt file contains a list of all the libraries that were used. One can use the command below to automatically install all the Python libraries.

`python -m pip install -r requirements.txt`


The code was written in Python version 3.9.6. It is advisable to use the same version of Python if you want to run this code in the notebooks. A convenient way to have multiple versions of Python available is through pyenv. The reader unfamiliar with pyenv is encouraged to search for it on the Internet.

It may be a bit tricky to get the code to run, even after installing the required libraries. The libraries depend on some data being loaded manually, e.g. the Encore_web data. This is usually resolved by considering the error and searching on the Internet for a solution. To fully document all required steps to get the code running is beyond scope for now, but is on a list of to-do's if there is enough interest in this work.

## Obtaining the dataset
The well known Enron email dataset was used in this project. It is the version used with all the emails in a folder structure. This should be downloaded and unzipped into the folder _data/raw_ so that the _maildir_ folder is in _data/raw_. The preprocess notebook will create all relevant folders as required. The _Multex_files.txt_ which is located in this folder, must also be copied to _data/raw_. This file points to specific _multex.com_ emails which are used by the preprocess notebook to construct a subset of query emails.

## Exploring the notebooks
The notebooks can be found in the _notebooks/Experiments_ and _notebooks/Preprocess_ folders. The _Preprocess_ notebook is the first notebook that should be explored. It prepares the data for all the experiments from the Enron dataset.

The _Experiments_ folder contains four notebooks, one for each experiment performed for the mini-dissertation. The notebooks are not documented to be explored alone. The notebooks are written as a companion to the mini-dissertation. All interpretations can be found in the mini-dissertation.

The experiments must be run in the order they are named. Experiment 1 is fully self contained. Experiment 2 generates a model which is saved and reused in experiment 3, therefore experiment 3 cannot be run before experiment 2 was finalised, or at least to the point of saving the model. Experiment 4 can be run on its own without running previous experiments, but the results of experiment 4 in the mini-disseration rely on comparison to experiment 2.

It is not necessary to run experiments. The last code executed, was saved, with its output, in the notebooks. The notebooks can therefore be used purely for reference and insight into the code.

## Exploring the source code
Much of the source code is available in the notebooks. The notebooks do rely on a class efpl.py, which was written specifically for this work. The class can be found in the _src/modules_ folder.



Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment.
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── modules        <- Modules written specifically for this project.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
