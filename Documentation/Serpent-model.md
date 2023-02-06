# Serpent 2 Model

This file describes the requirements and inputs for the Serpent 2 portion of **CONSTELATION**. The development, verification, and validation of the Serpent 2 model is up to the user. The [Serpent 2 wiki](https://serpent.vtt.fi/mediawiki/index.php/Main_Page) is a great resource. 


---
## Source Generation

Once the user has obtained a Serpent 2 input file for their needs, the input file must be run in source mode to generate the source files used in the transient simulation. After generating the source files, the input file must be modified to run in transient mode. The end of the *`Treat`* file included presents 'Source Inputs' and 'Transient Inputs'. The user can just comment out the inputs that are not being used. The excerpt below is set up to run in transient mode, with the source mode inputs commented out.
```
%**********************************************
%**** Source Inputs
%**********************************************
%set saverc "./Source" 0.09
%set cfe 10
set power 16000000000
set edepmode 2
%**********************************************
%**** Transient Inputs
%**********************************************
tme tsim 2 1000 0 5E-3
set nps 500000000 2500 tsim
set ccmaxiter 1
```
The time card in Serpent 2 should be set up to match the time steps at which the STAR model will output data.

---
## Detector Outputs

The detector defined below is used to provide STAR-CCM+ with the energy deposited in the helium-3 during the time step in Serpent 2. There should be a detector like this for every cartridge or experiment being coupled with STAR-CCM+. For HENRI in TREAT, there are two such detectors, since there are two STAR-CCM+ simulations being coupled with the Serpent 2 model. If the STAR-CC+ geometry uses a quarter slice, like HENRI, the detector volume should be determined by the quarter slice instead of the entire geometry modeled in Serpent 2. This will ensure the STAR-CCM+ simulations are receiving the correct energy deposition.
```
% Output Joules for that quarter slice (output Y slice to Pass to STAR)
%Top of Reactor
det Serpent2STop 
dr -4 void dm He3Top 
% Quarter Volume divded by number of detector slices
dv 0.1169
dx 20.405 21.35 1
dy  38.56  40.605  4
dz -60.48375 60.48375 500
```


---
## Interface Files

The interface files, with the extension *`.ifc`*, allow for information to be passed to the Serpent 2 model while it is running (between time steps). More information about the *`.ifc`* files and how to use them can be found at the Serpent 2 wiki: [Multi-physics Interface](https://serpent.vtt.fi/mediawiki/index.php/Multi-physics_interface). The form used for HENRI coupled in TREAT is seen below.
```
TYPE MAT OUT
MESHTYPE
[MESH DATA]
DENS1 T1
DENS2 T2
...
```
The header and first lines that **CONSTELATION** writes for the HENRI/TREAT model *`.ifc`* file is shown below. This uses a regular, cartesian based interface with no output file. The `[MESH DATA]` input defines the cartesian coordinates of interest.
```
2  He3Top 0
1
1 -100 100 1 0 100 500 -60.48375 60.48375
```

**CONSTELATION** will read the *`.csv`* output from STAR-CCM+ and convert it to the correct format for Serpent to read and then write the information to the *`.ifc`* file. The density and temperature data are appended into the file below the `[MESH DATA]` line.
