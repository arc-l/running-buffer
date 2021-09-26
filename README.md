# [On Running Buffer Minimization for Tabletop Rearrangement](https://arxiv.org/pdf/2105.06357.pdf)

## Kai Gao   &middot;   Si Wei Feng   &middot;    Jingjin Yu  [[arxiv preprint, to appear in R:SS 2021](https://arxiv.org/pdf/2105.06357.pdf)]


This repository will host the source code implementing efficient algorithms for computing rearrangement plans that minimize running buffers, to be published prior to the start of R:SS 2021. 

## Setup Instruction

1. It is recommended to use a virtual environment with Python 3 for this project, e.g., `conda create -n RunningBuffer python=3`.
2. Make sure you are in your virtual environment. 
3. Run `pip install -e .` to install the pagerank package and dependencies. 

## Run
1. Labeled Instance: `python3 ./Labeled_Case/Labeled_Experiment.py`
2. Unlabeled Instance: `python3 ./Unlabeled_Case/Unlabeled_Experiment.py`

## On Minimizing the Number of Running Buffers for Tabletop Rearrangement

In nearly all aspects of our everyday lives, be it work related, at home, or for 
play, objects are to be grasped and rearranged, e.g., tidying up a messy desk, 
cleaning the table after dinner, or solving a jigsaw puzzle. Similarly, many
industrial and logistics applications require repetitive rearrangements of many 
objects, e.g., the sorting and packaging of products on conveyors with robots, 
and doing so efficiently is of critical importance to boost the competitiveness 
of the stakeholders. However, even without the challenge of grasping, **deciding 
the sequence of objects for optimally solving a pick-n-place based rearrangement 
task** is non-trivial. 

For the example below, perhaps we want to arrange the sodas from the configuraiton 
on the left to the neater configuration on the right (the order between coke and 
pepsi does not necessarily reflect my personal preference :D). Let us assume the 
robot will use overhand grasps: it will pick up an object, lift it above all 
other objects, move it around, and drop it off at a place on the table that is 
collision-free. A natural question to ask here is, **how many** such pick-n-place 
operations are needed to solve a given problem? 

![setup](https://user-images.githubusercontent.com/35314983/124187803-59b14b00-da8c-11eb-8160-7b3af0f1c4a2.png)

In solving the problem, we first make the following observation: the coke occupies 
the pepsi's goal and vice versa, which means that one of them must be moved to 
a temporary location before the problem can be solved. This creates a **two-way** 
constraint. The coke also occupies the goal of the fanta, but this constraint is a 
**one-way** constraint. From the observation, we may fully capture the constraints 
in a tabletop pick-n-place rearrangement problem using **dependency graphs**, as 
shown on the right side of the figure below. Dependency graphs can be computed 
easily by extracting the the pairwise object constraints. 

![labeled](https://user-images.githubusercontent.com/35314983/124187832-633ab300-da8c-11eb-9a6f-1cd623ac30b1.png)

The above dependency graph structure is induced by labeled (distinguishable) objects. 
When the objects are unlabeled, dependency graphs can also be defined. In this case, 
the dependency graphs are undirected and bipartite. 

![unlabeled](https://user-images.githubusercontent.com/35314983/124187844-6766d080-da8c-11eb-9178-2313de59bda7.png)

As it turns out, minimizing the **total number** of objects to place at temporary 
locations, or **buffers**, is a difficult problem to solve at scale, because it is 
essentially the same as the *feedback vertex set* problem on the corresponding 
dependency graph, which is one of the 
[first batch of problems proven to be NP-hard](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems).
This aspect of the tabletop rearrangement problem is studied by 
[Han et al.](https://journals.sagepub.com/doi/pdf/10.1177/0278364918780999)
a few years back. 

Here, we are interested in a related optimization objective. Instead of the 
**total number** of buffers, what about the **minimum number of buffers that are 
currently being used**? That is, how many **running buffers** are needed to solve 
a given tabletop rearrangement problem? This is an important question to ask, 
because the number of running buffers is more relevant than the number of 
total buffers in deciding the feasibility of solving a given problem. That is, 
even if the total number of buffers may be very large, it is likely that at any 
moment, only a few objects needs to be displaced to solve the problem. 

In a recent work, 

```
On Minimizing the Number of Running Buffers for Tabletop Rearrangement
Kai Gao, Siwei Feng, Jingjin Yu. R:SS 2021. 
```

we made a first systmatic study of the problem of minimizing the number of running 
buffers in solving pick-n-place based tabletop rearrangement (**TORO**) problem. As 
a summary of the results, we begin by showing that computing an **MRB** (minimum 
running buffer) solution on arbitrary dependency graphs is NP-hard. Then, we establish 
that for an $n$-object **TORO** instance, **MRB** can be lower bounded by $\Omega(\sqrt{n})$ 
for uniform cylinders, even when all objects are *unlabeled*. This implies that the 
same is true for the *labeled* setting. We also provide a matching algorithmic upper
bound $O(\sqrt{n})$ for the unlabeled setting. In terms of practical methods, we 
have developed multiple highly effective and optimal algorithms for computing 
**MRB** rearrangement plans. In particular, we present a *depth-first-search dynamic 
programming* routine that readily scales to instances with over a hundred objects for 
the labeled setting, and a priority queue-based modification of a dynamic programming 
algorithm for the unlabeled setting. This allows us to quickly compute high-quality 
plans for solving highly constrained rearrangement problems like the follwoing, where
only two external buffers are needed. 

<video width="100%" src="https://user-images.githubusercontent.com/35314983/124187934-89f8e980-da8c-11eb-8e48-930681b38f0b.mp4" data-canonical-src="https://user-images.githubusercontent.com/35314983/124187934-89f8e980-da8c-11eb-8e48-930681b38f0b.mp4" controls="controls" muted="muted" class="d-block rounded-bottom-2 width-fit" style="max-height:640px;">
</video>

For more information, check out the [presentation](https://youtu.be/hbD-cumF_H4) and the [paper](http://www.roboticsproceedings.org/rss17/p033.pdf). 
