# Simulation Status


## Cole's OG sim (500 psi initial pressure)

- getting `Done file not found, pausing ...` error, which comes from *`SerpentDone.txt`* file not being found by the STAR-CCM+ simulation (this error is occurring for both simulations). Possible causes:

    - done file is deleted before STAR-CCM+ simulations can read it
    - STAR-CCM+ simulations run much faster than Serpent and are waiting for the done file to be written

- after further investigation, one STAR-CCM+ simulation was able to read the done file once, but could not find it after the second 100 iterations. The other STAR-CCM+ simulation only completed 100 iterations before getting stuck on the done file.

    |    |  Bot  |  Top  |
    |:---: | :---: | :---: |
    |  Start  |   20:10:01    |  20:10:01   |
    |  Time Step |  200   | 100 |
    | Stop  | 23:58:47  | 21:12:37 |

    |   |  Time 1  |  Time 2  |
    | :---: | :---: | :---: |
    | Batch 1 | 20:04:34 Dec 29 | 1:29:29 run time |
    | Batch 500 | 0:02:33 run time | 1:30:13 run time |

- going to try using `select=1:ncpus=48:mpiprocs=48` for STAR-CCM+ job scripts, which is what Cole orginally used. I had mine at 3 nodes for speed on just cfd sims.

    |    |  Bot  |  Top  |
    |:---: | :---: | :---: |
    |  Start  |   22:19:58 Jan 02    |  22:19:25 Jan 02  |
    |  Time Step |  200   | 200 |
    | Stop  | 02:04:45 Jan 03  | 23:28:40 Jan 02 |

    |   |  Time 1  |  Time 2  |  Time 3  |
    | :---: | :---: | :---: | :---: |
    | Batch 1 | 22:15:16 Jan 02 | 0:08:14 run time | 1:27:07 run time |
    | Batch 500 | 0:02:36 run time | 0:09:06 run time | 1:27:56 run time |


- going to try replacing *bot* file with *top* because the *bot* file is taking so long to run
    - looks like the Serpent sim did not continue after the 6th time step from STAR. not sure why as the STAR done files are both present. the callback from the cli was at line 719 in CONSTELATION, which is waiting for the data from STAR. After checking where Serpent is looking, there are no new files. This must be due to replacing the STAR sim. I will need to edit the sims after I can use STAR licenses again.

    |    |  Bot  |  Top  |
    |:---: | :---: | :---: |
    |  Start  |   09:12:04 Jan 05    |  09:12:03 Jan 05  |
    |  Time Step |  600   | 600 |
    | Stop  | 10:46:58 Jan 05  | 10:46:40 Jan 05 |


    |  08:59:15 Jan 05    |  Batch 1  |  Batch 500  |
    |:---: | :---: | :---: |
    | Time 1 | 0:01:59 | 0:02:33 |
    | Time 2 | 0:16:51 | 0:17:40 |
    | Time 3 | 0:23:05 | 0:23:52 |
    | Time 4 | 0:28:49 | 0:29:36 |
    | Time 5 | 0:35:22 | 0:36:11 |
    | Time 6 | 0:41:55 | 0:42:44 |


- Tried to change the output of the new *bot* file but could not on pc, so I found and removed the saving of images every iteration from the original *bot* file.
    - this worked. will compare results to Cole's results to make sure it is working properly.


---
## 250 psi initial pressure

- Attempting to run 250 psi initial pressure coupled sim
    - had to reset directory for *bot* sim to save to. created a folder of the correct name in the sim directory and was able to change the location in STAR
    - everything else kept the same for the coupled sim, just changing the names of the STAR sim in the job scripts.
    - error in line 264 in CONSTELATION: `if int(line) != -1:` ValueError: invalid literal for int() with base 10: ''
    - *`com.in`* file had -1 and *`com.out`* file had 10
    - STAR-CCM+ sim made it to over 1ms, but Serpent 2 sim got to 4.24E-4 to 4.26E-4 time step

- Retrying with no change to see if results are repeated
    - same error in line 264
    - STAR-CCM+ sims ran to 0.0045 seconds, iteration 92000
    - Serpent on Time interval 921/2500 from 1.84E-03 to 1.842E-03 s
    - *`com.in`* file had -1 and *`com.out`* file had 10


    |       |  Time Step | Iteration | Calc Time | Reported Time |
    | :---: | :---:      |  :---:    |  :---:    |  :---:        |
    | Serpent| 2E-6      | 921       | 1.842E-3  | 1.842E-3      |
    | STAR-CCM+ | 5E-8   | 92000     | 4.6E-3    | 4.6E-3        |

- After talking with Cole:
    - STAR-CCM+ writes out every 40 iterations, but stops every 100
    - Every iteration, Serpent reads the files that are written by STAR at the appropiate 40 STAR iteration
    - The Serpent time step is determined by the simulation resolution, as the STAR time step is determined by its simulation. Then the STAR output frequency is determined by making the two match.

- Going to change *`load_dataBot.java`* and *`load_dataTop.java`* line 60 from 100 to 40

    ```java
    // Changes the number of time steps that one initalization of the STEP command performs
        simulation_0.getSimulationIterator().setNumberOfSteps(100);
    ```

    ```java
    // Changes the number of time steps that one initalization of the STEP command performs
        simulation_0.getSimulationIterator().setNumberOfSteps(40);
    ```

- Trying coupled sim with updated java files
    - ended with error on line 264 in CONSTELATION
    - Serpent got through time step 85 / 2500 1.68E-4 to 1.70E-4 seconds
    - STAR got to time step 8400, simulation time 0.00042 seconds

- creating new 250 psi sim files from 500psi files that worked
    - copied *`06.14.2021_STARTop.sim`* to *`06.14.2021_STARTop_250.sim`*
        - changed the field function to have 1.72E6 Pa as the initial driver pressure and re-initialized the solution
        - changed the monitors for Continuity, X-momentum, Y-momentum, Energy, TKE, and SDR to output every time step instead of every iteration
    - copied *`06.14.2021_STARBot3.sim`* to *`06.14.2021_STARBot3_250.sim`*
        - changed the field function to have 1.72E6 Pa as the initial driver pressure and re-initialized the solution
        - changed the monitors for Continuity, X-momentum, Y-momentum, Energy, TKE, and SDR to output every time step instead of every iteration
    - going to run both on their own to make sure they work
        - *`06.14.2021_STARBot3_250.sim`* failed due to license checkout failure. will try again soon
        - looks like the save file for *`06.14.2021_STARTop_250.sim`* got corrupted. it would not download from HPCondemand.

- while investigating the java files, I found another line (line 77) that has a time step call to be changed from 100 to 40:
```java
// While Loop dicating the refreshing of the Heating Table provided by the wrapping code
 double Current_Time;
 Current_Time = 0;
while (TotalTimeSteps > Current_Time)
{
    simulation_0.getSimulationIterator().step(100);
    sleep_time = 0;
```
```java
// While Loop dicating the refreshing of the Heating Table provided by the wrapping code
 double Current_Time;
 Current_Time = 0;
while (TotalTimeSteps > Current_Time)
{
    simulation_0.getSimulationIterator().step(40);
    sleep_time = 0;
```


---
## Prepping OSTR Serpent Model
- running *`TRIGA_05tube_D5_void`* on INL HPC 6 nodes, 48 cores each
    - $k_{eff}=1.02308$ with 

    | Rod | z-trans |
    | :---: | :---: |
    | tr  | 2.0955  |
    | sa  | 2.0955  |
    | sh  | -4.953  |
    | reg | 2.0974  |

- trying putting rods back to default values (fully inserted, I think)

    | Rod | z-trans |
    | :---: | :---: |
    | tr  | -19.05  |
    | sa  | -19.05  |
    | sh  | -19.05  |
    | reg | -18.5928|

    - $k_{eff}=0.97465$

- trying setting the rods just below the default positions defined in the input file (where the trans cards are 0)

    | Rod | z-trans |
    | :---: | :---: |
    | tr  | -2.0955 |
    | sa  | -2.0955 |
    | sh  | -4.953  |
    | reg | -2.0974 |

    - $k_{eff}=1.01252$

- lets try moving the rods further down

    | Rod | z-trans |
    | :---: | :---: |
    | tr  | -5 |
    | sa  | -5 |
    | sh  | -8  |
    | reg | -5 |

    - $k_{eff}=1.00218$

- lets try moving the rods down a little bit more

    | Rod | z-trans |
    | :---: | :---: |
    | tr  | -6 |
    | sa  | -6 |
    | sh  | -9  |
    | reg | -6 |