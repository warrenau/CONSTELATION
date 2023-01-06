# Simulation Status


## Cole's OG sim

- getting *`Done file not found, pausing ...`* error, which comes from `SerpentDone.txt` file not being found by the STAR-CCM+ simulation (this error is occurring for both simulations). Possible causes:

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

- going to try using *`select=1:ncpus=48:mpiprocs=48`* for STAR-CCM+ job scripts, which is what Cole orginally used. I had mine at 3 nodes for speed on just cfd sims.

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