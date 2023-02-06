// Simcenter STAR-CCM+ macro: load_data.java
// Written by Simcenter STAR-CCM+ 15.04.010
package macro;

import java.io.File;
import java.util.*;
import star.common.*;
import star.base.neo.*;
import star.meshing.*;
import star.energy.*;
import java.io.IOException;  
import java.io.FileWriter;

public class load_dataBot extends StarMacro {

  public void execute() {
// Starts the STAR-CCM+ simulation
    execute0();
  }

  private void execute0() {
// Remeshes problem to ensure start from scratch
    Simulation simulation_0 = 
      getActiveSimulation();

    MeshPipelineController meshPipelineController_0 = 
      simulation_0.get(MeshPipelineController.class);

    meshPipelineController_0.clearGeneratedMeshes();

    meshPipelineController_0.generateVolumeMesh();

    Solution solution_0 = 
      simulation_0.getSolution();
      
// Creates Table from provided .csv from the wrapping code 
    FileTable fileTable_2 = 
      (FileTable) simulation_0.getTableManager().createFromFile(resolvePath("STAR_HeatBot.csv"));

// Set Volumetric Heating input to use the table created from wrapping code
    Region region_0 = 
      simulation_0.getRegionManager().getRegion("3.29.2019_Benchmark_1in");

    VolumetricHeatSourceProfile volumetricHeatSourceProfile_0 = 
      region_0.getValues().get(VolumetricHeatSourceProfile.class);

    volumetricHeatSourceProfile_0.setMethod(XyzTabularScalarProfileMethod.class);

    volumetricHeatSourceProfile_0.getMethod(XyzTabularScalarProfileMethod.class).setTable(fileTable_2);
 
 // Initializes the simulation   
    solution_0.initializeSolution();
// Grabs the user-set max stopping time 
  PhysicalTimeStoppingCriterion physicalTimeStoppingCriterion_0 = 
      ((PhysicalTimeStoppingCriterion) simulation_0.getSolverStoppingCriterionManager().getSolverStoppingCriterion("Maximum Physical Time"));
// Grabs the current simulation time (should be 0.0 sec) 
double startTimelevel = simulation_0.getSimulationIterator().getCurrentTimeLevel();

// Changes the number of time steps that one initalization of the STEP command performs
    simulation_0.getSimulationIterator().setNumberOfSteps(40);
// Sets the Max Stopping time to a number so it can be compared to current sim time
double maxstoppingtime = physicalTimeStoppingCriterion_0.getMaximumTime().getValue();
double TotalTimeSteps;
TotalTimeSteps = 100000000;
File f;
int sleep_time;
int wait_time;
int break_again;
wait_time = 100000000;
sleep_time = 0;
break_again = 0;
// While Loop dicating the refreshing of the Heating Table provided by the wrapping code
 double Current_Time;
 Current_Time = 0;
while (TotalTimeSteps > Current_Time)
{
    simulation_0.getSimulationIterator().step(40);
    sleep_time = 0;
//Create file says STAR-CCM+ is done simulating
   try {
       FileWriter writer = new FileWriter("STARBotDone.txt", true);
       writer.write("Hello World");
       writer.write("\r\n");   // write new line
       writer.write("Good Bye!");
       writer.close();
   } catch (IOException e) {
           e.printStackTrace();
   }
 
    // Check to see if wrapping code says SERPENT 2 is done executing this step
    f = new File("SerpentDone.txt");
    boolean exist = f.exists();
// If it doesnt exist (pause execution for a second and check again
    while (!f.exists())
    {
     simulation_0.println("Could not find done file pausing...");
       try {
       Thread.sleep(1000);
       }
       catch(InterruptedException ex)
       {
        Thread.currentThread().interrupt();
       }
       sleep_time = sleep_time + 1;
// If file isn't created in specified wait time, break out of loops
        if (sleep_time > wait_time)
        {
           simulation_0.println("Breaking out of Running Loop");
	   break_again = break_again+1;
            break;
        }
    }
// If it does exist then just reload and continue simulation
    if (f.exists())
    {
    fileTable_2.extract();
    }
// Breaks out of execution loop
    if (break_again > 0)
    {
    break;
    }
    Current_Time = simulation_0.getSimulationIterator().getCurrentTimeLevel();
    simulation_0.println("Current Time Step is :" + Current_Time);
  }
 }
}
