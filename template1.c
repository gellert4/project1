/*
Degree: Artificial Intelligence
Subject: Fundamentals of Programming 2
Practical project: 1

Simulator - main program
*/

#include <stdio.h>
#include <stdlib.h>

#include "project1.h" // header with all data structures

//----------------------------------------------------------General
// WARNING: do not change this function
enum EventType GenerateEventType()
{
	return rand()%3;
}

void CheckArguments (int argc, char ** argv)
{
	// check the input introduced by the user
}

//----------------------------------------------------------RobotPackages -> Sorted list
// WARNING: do not change this function
struct RobotPackage * GenerateRobotPackage()
{
	// reserve memory for a RobotPackage
	struct RobotPackage * RobotPackage=malloc(sizeof(struct RobotPackage));
	int RobotPackageNum=rand()%8;
	// initialize the RobotPackage's fields
	strcpy (RobotPackage->supplier, suppliers[RobotPackageNum]);
	strcpy (RobotPackage->id, ids[RobotPackageNum]);
	int year=rand()%40+1980;
	RobotPackage->year=year;
	return RobotPackage;
}

// function to print a list of RobotPackages
void PrintRobotPackages()
{
	
}

// function to search for a RobotPackage
struct RobotPackage * SearchRobotPackage(/*...*/)
{

}

// function to simulate an insertion of RobotPackages in a ordered way (sorted by supplier)
void SimulateManagingRobotPackages(struct RobotPackage * RobotPackage)
{

}

// function to remove all the RobotPackages from the list at the end of the program
void RemoveAllRobotPackages()
{

}

//----------------------------------------------------------Packages -> different Stacks
// WARNING: do not change this function
struct Package * GeneratePackage()
{
	// reserve memory for a Package
	struct Package * Package=malloc(sizeof(struct Package));
	// initialize the Package's fields
	enum PackageType type=rand()%3;
	enum Colors color=rand()%4;
	Package->type = type;
	Package->color = color;
	return Package;
}

// function to initialize all stacks of Packages 
void InitStacks()
{

}

// function to print all stacks with all Packages
void PrintPackages()
{

}

// function to remove all packages from a given stack when its MAX_CAPACITY is reached
void RemoveStack(/*...*/)
{

}

// function to simulate putting a generated Package to a corresponding stack depending on the type (size)
void SimulateClassifyPackage(struct Package * Package)
{

}

// function to clean all stacks before the end of the program
void CleanPackageStacks()
{

}

//----------------------------------------------------------Shopping -> Queue
// WARNING: do not change this function
struct Shopping * GenerateShopping()
{
	// reserve memory for a Shopping
	struct Shopping * shopping=malloc(sizeof(struct Shopping));
	// initialize the shopping's fields
	int n=rand()%5+1;
	shopping->numberThingsToBuy = n;
	nextRobotID++;
	shopping->robot_id=nextRobotID;
	return shopping;
}

// function to print a list of robots in a shopping queue
void PrintShopping()
{

}

// function to add a robot to a shopping queue
void AddToQueue(struct Shopping * shopping)
{

}

// function to remove a robot from the queue and serve it
// it may return the number of things to buy to simulate the time
int Dequeue ()
{

}

// function to simulate the time the robot is in the queue
void UpdateShoppingQueue (/*...*/)
{

}

// function to simulate a robot going for shopping - add to the queue
void SimulateGoForShopping(struct Shopping * shopping)
{

}

// function to clean shopping queue before the end of the program
void CleanShoppingQueue(/*...*/)
{

}

//----------------------------------------------------------main
// This is the main loop of the program. 
// It generates and consumes events.
void SimulationLoop(int EventNumbers)
{
	// declare and initialize necessary variables

	InitStacks();
	
	for (int i=0; i<EventNumbers; i++)    
	{
		// generate event type
		// depending on the generated event type:
		// event type 0: 
			// generate RobotPackage 
			// Simulate managing RobotPackages (sorting)
		// event type 1:
			// generate Package
			// Simulate classifying Packages (putting to a corresponding stack)
		// event type 2:
			// generate shopping
			// Simulate go for shopping 
		// UpdateShopping
	}
	// CLEANING THE SIMULATION
}

int main (int argc, char ** argv)
{
	int EventNumbers;
	printf ("Starting... \n");
	CheckArguments(argc, argv);
	
	// initialize EventNumbers 

	SimulationLoop(EventNumbers);
	return 0;
}
