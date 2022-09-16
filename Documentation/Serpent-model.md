# Serpent 2 Model

This file describes the requirements and inputs for the Serpent 2 portion of **CONSTELATION**. The development, verification, and validation of the Serpent 2 model is up to the user. The [Serpent 2 wiki](https://serpent.vtt.fi/mediawiki/index.php/Main_Page) is a great resource. Once the user has obtained a Serpent 2 input file for their needs, the input file must be run in source mode to generate the source files used in the transient simulation. After generating the source files, the input file must be modified to run in transient mode. The end of the *Treat* file included presents 'Source Inputs' and 'Transient Inputs'. The user can just comment out the inputs that are not being used. The excerpt below is set up to run in transient mode, with the source mode inputs commented out.
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