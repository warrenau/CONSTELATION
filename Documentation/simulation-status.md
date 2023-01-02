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

- going to try using *`select=1:ncpus=48:mpiprocs=48`* for STAR-CCM+ job scripts, which is what Cole orginally used. I had mine at 3 nodes for speed on just cfd sims.