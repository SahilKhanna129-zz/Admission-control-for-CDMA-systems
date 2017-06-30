This simulation is implemented by using three python scripts

Main.py: It consists of main code for the simulation and uses two modules LossFunction.py and 
         SupportingMethod.py. In order to run the simulation please append the path of the files
	to the sys path.

LossCalucation.py: It consists of loss calculations methods which supports the simulation.

SupportingMethods.py: It consists of many methods which supports the simulation. Please appends
		      the files directory path to the sys path because it uses some of the methods
		      from the LossCalculation module.

 
1. Please add the path to the files to the sys path at each script to run the simulation
3. Only Numpy and matplotlib.pyplot modules are used in the scripts. Please download the supporting modules
4. Uncomment the display function  call in Main.py in order to see the simulation but it will slow the execution
   because of the pause statement for the figures.
