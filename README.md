# GemStone-ApplyPower

This project allows empirical power models (e.g. those build from [Powmon](http://powmon.ecs.soton.ac.uk)) 
to be applied to either data collected from an Arm hardware platfrom 
(e.g. using [GemStone-Profiler-Automate](https://github.com/mattw200/gemstone-profiler-automate)) or 
 [gem5](http://gem5.org) simulation. 
 
It also outputs equations that can be inserted directly into [gem5](http://gem5.org) for "online"
 power readings in the simulation. 
 
Furthermore, it allows the performance, power and energy scaling to be evaluted and 
plotted with [GemStone](http://gemstone.ecs.soton.ac.uk). 

## Usage

Tutorials for using this project are available at [GemStone](http://gemstone.ecs.soton.ac.uk). 

## Provided models, sample data, etc.

### MODELS

All models characterised on a Hardkernel ODROID-XU3 board with an Exynos-5422
SoC (quad-core Arm Cortex-A7 and Arm Cortex-A15 CPU)

|Name			        | paper	 | from	| power model description
|-----------------------|--------|------|-------------------------------------
|asrtpm-A15.params	    | [2]	 | [1]	| Cortex-A15
|asrtpm-A7.params	    | [2]	 | [1]	| Cortex-A7
|thermal-A15.params     | [3]    | [1] 	| Cortex-A15 with thermal compensation
|thermal-A7.params      | [3]    | [1] 	| Cortex-A7 with thermal compensation
|gs-A15-asrtpm-e.params | [4]    |      | Cortex-A15, gs, with asrtpm events
|gs-A15.params		    | [4]    | 	    | Cortex-A15 (optimised for gem5)
|gs-A7.params		    | [4]    |      | Cortex-A7 (optimised for gem5)
|gs-A7-4-pmcs.params    | [4]    |    	| Cortex-A7 (optimised for gem5)*

\*using only four PMC events (instead of five)

### SAMPLE DATA

There are several different sample data inputs. Some are measured from 
 a hardware platform (ODROID-XU3) and some from gem5. The data from [2]
 was collected using Powmon [1] - workloads are repeated for 30 seconds.
 The hardware data from [4] was collected using GemStone-Profile and has a 
 different format and workloads were exeucted once. The gem5 data was 
 collected from gem5 experiments and converted using GemStone, see [4]. 

|Name				               | paper	| from  | data collected with
|----------------------------------|--------|-------|----------------------
|asrtpm-A15-powmon-data.csv        | [2]	| [1]	| Powmon
|asrtpm-A7-powmon-data.csv         | [2]	| [1]	| Powmon
|gs-profiler-gem5-0-A15-data.csv   | [4]    | 	    | GemStone-Profiler + gem5 (0)
|gs-profiler-gem5-0-A7-data.csv    | [4]    | 	    | GemStone-Profiler + gem5 (0)
|gs-profiler-gem5-1-A15-data.csv   | [4]    | 	    | GemStone-Profiler + gem5 (1)
|gs-profiler-gem5-1-A7-data.csv    | [4]    | 	    | GemStone-Profiler + gem5 (1)

\*gem5 model ((0):before,(1):after)) branch predictor fix was made, see [4]

The `GemStone-Profiler` and gem5 data are combined in the same file. 


### MAP FILES

|Name			      | Description
|---------------------|--------------------------------------------------------
|powmon-A15.map		  | For use with data from Powmon (A15)
|gs-profiler-A7.map   | For use with data from GemStone-Profiler (A7)
|gs-profiler-A15.map  | For use with data from GemStone-Profiler (A15)
|gem5-A7.map		  | For use with gem5 data processed by GemStone (A7)
|gem5-A15.map		  | For use with gem5 data processed by GemStone (A15)


### REFERENCES

1. http://www.powmon.ecs.soton.ac.uk/powermodeling/
2. M. J. Walker; S. Diestelhorst; A. Hansson; A. K. Das; S. Yang; B. M. Al-Hashimi; G. V. Merrett, "Accurate and Stable Run-Time Power Modeling for Mobile and Embedded CPUs," in IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems , vol.PP, no.99, pp.1-1, doi: 10.1109/TCAD.2016.2562920
3. Walker, Matthew J. , Diestelhorst, Stephan, Hansson, Andreas , Balsamo, Domenico, Merrett, Geoff V. and Al-Hashimi, Bashir M., "Thermally-aware composite run-time CPU power models," In, International Workshop on Power And Timing Modeling, Optimization and Simulation (PATMOS 2016), Bremen, DE, 21 - 23 Sep 2016
4. M. J. Walker, S. Bischoff, S. Diestelhorst, G V. Merrett, and B M. Al-Hashimi, "Hardware-Validated CPU Performance and Energy Modelling", in IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), Belfast, Northern Ireland, UK, April, 2018 [Accepted]

## Authors

[Matthew J. Walker](mailto:mw9g09@ecs.soton.ac.uk) - [University of Southampton](https://www.southampton.ac.uk)

This project supports the paper:
>M. J. Walker, S. Bischoff, S. Diestelhorst, G V. Merrett, and B M. Al-Hashimi,
>["Hardware-Validated CPU Performance and Energy Modelling"](http://www.ispass.org/ispass2018/),
>in IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS), 
> Belfast, Northern Ireland, UK, April, 2018 [Accepted]

This work is supported by [Arm Research](https://developer.arm.com/research), 
[EPSRC](https://www.epsrc.ac.uk), and the [PRiME Project](http://www.prime-project.org).


## License

This project is licensed under the 3-clause BSD license. See LICENSE.md for details.


