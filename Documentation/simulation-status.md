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