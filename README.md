# [On Running Buffer Minimization for Tabletop Rearrangement](https://arxiv.org/pdf/2105.06357.pdf)

## Kai Gao   &middot;   Si Wei Feng   &middot;    Jingjin Yu  [[arxiv preprint, to appear in R:SS 2021](https://arxiv.org/pdf/2105.06357.pdf)]


This repository will host the source code implementing efficient algorithms for computing rearrangement plans that minimize running buffers, to be published prior to the start of R:SS 2021. 

## Setup Instruction

1. It is recommended to use a virtual environment with Python 3 for this project, e.g., `conda create -n pagerank python=3`.
2. Make sure you are in your virtual environment. 
3. Run `pip install -e .` to install the pagerank package and dependencies. 

## Run
1. Labeled Instance: `python3 ./Labeled_case/Labeled_Experiment.py`
2. Unlabeled Instance: `python3 ./Unlabeled_case/Unlabeled_Experiment.py`
