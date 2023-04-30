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

- new 250psi star files ran for 1 week without issue.
- I turned off the residual printing to the terminal to reduce the cluster output file
- when I attempted to start the coupled sim, the virtual desktop had a maximum of 168 hour requested time. I have asked HPC support if there is a way around that.
    - HPC support fixed the issue
- started a new coupled run on HPC
    - sim failed bc star couldn't find licenses. retrying.
- Failed again
    - line 264 CONSTELATION error again, not sure why
    - in STAR top output: `corrections limited on 1 cells in 3.29.2019_Benchmark_1in` and `minimum absolute pressure limited to 1 on 1 cells in 3.29.2019_Benchmark_1in`
    - server time out on STAR sim: `Could not find done file pausing...`
    - from troubleshooting: determined that the *`com.out`* file was empty for some reason while **CONSTELATION** was trying to read it. one fix from Cole is to add more wait time before looking for the file. a better fix might be to add a check to make sure there is something in the file before it is read by **CONSTELATION**.
    - going to add check and maybe more wait time.
- added check for integer in *`com.out`* file. will retry simulation with fix.
    - still failed, but it failed in the check. It is passing the check for digits, but failing when trying to convert to int
    Error message:
    ```
    Traceback (most recent call last):
      File "CONSTELATION.py", line 268, in <module>
        line_int = int(line)
    ValueError: invalid literal for int() with base 10: ''
    ```
    - Lines 265-268 of *`CONSTELATION.py`*:
    ```python
    f_digit = line.strip('-\n\r').isdigit
    if f_digit:
        # create variable that is the integer of the read in string
        line_int = int(line)
    ```
    - forgot parentheses on end of `isdigit`? yes, and it makes a difference. fixed in code. trying again.
    - sim got to 2.18200E-03 s (Bot) and 43640 iterations (Top) / time interval 1092/2500 from 2.182000E-03 to 2.184000E-03 s batch 500/500 (Serpent)
- Fixed typo. retrying.
    - STAR sims could not get licenses to run
- Retrying with fresh virtual desktop
    - it worked!!!!
    - ran for 1 week, then died at 4.6ms
    - realized looking at the results that the input is in guage pressure, so the absolute pressure starts at 264.7 psi in the driver tanks

- Changed intial pressure in driver tanks in both CFD simulations to be 1622053.706 Pa, which is 235.259 psig. Running again.
    - got to 3.22E-4 s then was stopped? the Serpent sim is queued, but it looks like the STAR sims timed out? not sure what happened, maybe a server issue. trying again, I guess
    - it tried to run and could not get enough STAR-CCM+ licenses. will try again sometime, but I am focusing on the STAR-CCM+ sims for the OSTR experiment for right now.

- Starting new sim using the changes made to **CONSTELATION** and the *`.java`* files in the OSTR-CONSTELATION development. This uses *`CONSTELATION_3.py`*, *`functions.py`*, *`load_dataBot.java`*, and *`load_dataTop.java`*. I cleared the ExtractedData folders, but did not wipe the other folders in the directory (ie Archive, LineProbe, etc).
- The simulation failed because one of the STAR sims could not get the correct number of licenses. Trying again.
- sim failed bc STAR_bot couldnt get enough licenses. will try again.
- got error about detector file on line 256 in *`CONSTELTATION_3.py`*:

```
ValueError: coupledTreat_det1.m has not been created or could not be read
```

- however, both of the star simulations started and the simulation got the signal to go to the next step before failing. will investigate.
- only one step of serpent simulation was completed. it should have continued to the next step after the star simulations both got through their first step.
- changed density conversion function to do nothing because Cole's STAR simulations convert the density already
- Got the same error again as above. Will investigate.
    - I have concluded that the error is caused by the *`com.in`* file not having the correct signal. It still read -1 when the simulation failed, but it should have read 12 to signal the Serpent simulation to continue. I tried to use the code to write the signal in a separate python script and it did not work, which could be due to some memory problem or a coincidence that Serpent was trying to read at the same time. I changed the code as described below and the signal was written properly. When I tried the original code again, it also worked. I am making the change though to see if the syntax will help avoid the error. If not, I may have to add an arbitrary wait time.
    - ```python
      file_out = open('com.in','w')
      file_out.write(str(signal.SIGUSR2.value))
      file_out.close()
      ```
    - ```python
      with open('com.in','w') as file_out:
          file_out.write(str(signal.SIGUSR2.value))
      ```

- Not enough STAR-CCM+ licenses on INL HPC, trying again.
    - error on Line 291 in *`CONSTELATION_3.py`*:
    ```
     ValueError: ./STARTopDone.txt has not been created or cannot be read
    ```
    - This is because the STAR simulations started about an hour and a half after the Serpent 2 simulation and the default wait time is 1 hour, so the *`STARTopDone.txt`* file had not been created when the wait time ran out.

    |    |  Start time   |  End Time  |
    | ---|  --- |    ---          |
    | Serpent | 21:03:45  | 21:06:02  |
    | STAR Top | 22:25:13  | 23:26:54 |
    | STAR Bot | 22:25:12  | 23:26:54 |


 April 21, 2023:
 - I changed the requested time to 48 hours in hope it will get through the queue before the cluster goes down.

 April 26, 2023:
 - Started sim with 168 hours requested on all jobs and 336 hours on virtual desktop
- same problem with waiting for *`coupledTREAT_det1.m`* file.
    - Dr. Howard proposed to move the write command for *`com.out`* to only happen if the contents are 12. such that **CONSTELATION** does not overwrite the file unless we are moving to the next step.

April 29, 2023:
- same problem with waiting for *`coupledTREAT_det1.m`* file.
    - after some investigation, I found that you cannot write to or copy over the *`com.in`* file before Serpent 2 has output the signal to move on to the next time step (at least for `SIGUSR2` signal). I did not try other signals, but they do not matter since **CONSTELATION** does not have to two codes interact between time steps.
    - I am going to make the following change to not let the script move on until the signal says to go to the next time step.
    - ```python
      # Check signal
        if line_int == -1:
            pass
        elif line_int == signal.SIGUSR1.value:
            # Got the signal to resume
            print(signal.SIGUSR1.value)
            print("Resume Current Iteration")
            sleeping = 0
        elif line_int == sig_notdigit:
            # Could not turn the contents of com.out into an integer. Continue and try again.
            print(sig_notdigit)
            print("Resume Current Iteration")
            sleeping = 0
        elif line_int == signal.SIGUSR2.value:
            # Got the signal to move to next time point
            print(signal.SIGUSR2.value)
            print('Move to Next Time Step')
            iterating = 0
            sleeping = 0
      ```
    - ```python
        # Check signal
        if line_int == -1:
            pass
        elif line_int == signal.SIGUSR1.value:
            # Got the signal to resume
            print(signal.SIGUSR1.value)
            print("Resume Current Iteration")
        elif line_int == sig_notdigit:
            # Could not turn the contents of com.out into an integer. Continue and try again.
            print(sig_notdigit)
            print("Resume Current Iteration")
        elif line_int == signal.SIGUSR2.value:
            # Got the signal to move to next time point
            print(signal.SIGUSR2.value)
            print('Move to Next Time Step')
            sleeping = 0
      ```

      - this change did not work. the simulation got stuck on printing `Resume Current Iteration`. I found another example script from Serpent for coupled transient sims that includes an additional while loop using `iterating` to control the time steps. It looks like I will need to add another loop to the script and tell Serpent to continue with a signal written to *`com.in`*. The simulation did move to the next step when I manually changed the signal.
      - I ran into a storage issue, which may have been bc of the huge amounts of terminal output caused by the simulation getting stuck in that loop.
