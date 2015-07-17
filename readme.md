# Overlap Calculations
## some files that were used for overlap calculations of various sorts
Skeletal overlap is a measure of how "close" two skeletons are from each other. This is a very controversial measure that can take very many meanings and values can differ greatly from one measure to the next.

- One method of calculating overlap is called cylindrical overlap and takes into consideration edges distance and angle from edges on the other cells dendrite/axon. This measure is implemented in the [catmaid module](https://github.com/htem/catmaid_utils/blob/master/catmaid/algorithms/population/synapses.py) for 
neuron overlap calculations. This method can be modified by re-sampling the skeleton. Some code for this can be found in the [Module branch of Lathomas42's catmaid_utils](https://github.com/Lathomas42/catmaid_utils/tree/develop/catmaid/algorithms/population) This code when combined with plot_overlaps_works in this directory
can be used to calculate overlaps on re-sampled edges of a neuron.

- Another metric for overlap could be just euclidean distance (this is a somewhat unsophisticated metric) where each node on neuron A's axon is compared to each node on neuron B's dendrite and vice versa. Code for this can be found in [CatmaidNeuronTools](https://github.com/Lathomas42/CatmaidNeuronTools). This is probably not the best
metric however modifications could be considered starting with this metric

- Another metric between two skeletons could be the [Hausdorff Distance](https://en.wikipedia.org/wiki/Hausdorff_distance) which is easily described as "the largest smallest distance" between two sets. Basically this amounts to doing the same measurements
as were done for the euclidean metric although instead of summing over all the distances, for each axonal node find its smallest distance to the dendrite of the other neuron, then, once this has been done for all axons, the maximum of all of these smallest 
distances is the Hausdorff distance. Code for this can be found in the [catmaid module](https://github.com/htem/catmaid_utils/blob/496740e04e56ca6addd12a1e48ffda69086130ba/catmaid/algorithms/population/distance.py)

I believe the best metric will be something similar to the cylindrical overlap method with the re-sampling optimized. The goal is to sample large enough to dampen human error but get cylinders that follow the axon/dendrite well.