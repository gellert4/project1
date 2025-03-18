/*
Degree: Artificial Intelligence
Subject: Fundamentals of Programming 2
Practical project: 1

project1.h
Header of all necessary data structures required by the project 1.
It also contains enumeration types and additional variables, 
arrays for managing data structures and their initial values
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum EventType { robotPackage=0, package=1, shopping=2 };

//-----------------------------------------------------------------------Sorting packages: RobotPackages struct
// predefined suppliers of RobotPackages; there are 8 RobotPackages
char suppliers[8][20]={{"Philips"}, {"CISCO"}, {"DELL"}, {"SONY"},
{"IBM"}, {"Intel"}, {"Samsung"}, {"Lenovo"}
};

// predefined ids of RobotPackages; there are 8 RobotPackages
char ids[8][20]={{"PHI-TS-BLU-SM"}, {"CIS-X1-GRE-ME"}, {"DEL-DX-PLA-LAR"}, {"SON-XR-BRO-SM"},
{"IBM-OX-PLA-LA"}, {"INT-EX-ORA-ME"}, {"SAM-VK-DBL-LA"}, {"LEN-IN-SIL-LA"}
};

// a pointer to the head of the RobotPackage list
struct RobotPackage * RobotPackagesHead=NULL;

struct RobotPackage
{
	char supplier[20];
	char id[20];
	int year;
   struct RobotPackage *next;
};

//---------------------------------------------------------------------Classifying packages: Packages struct

#define NUMBER_OF_STACK 3
#define MAX_CAPACITY 3

enum PackageType { small=0, medium=1, large=2 };
enum Colors { white=0, green=1, yellow=2, beige=3 };

// There are 3 different stacks, each one for each type of Package
// Here we create a static array to have 3 pointers to a top element of each stack
struct Package * Top_ofPackageStacks[NUMBER_OF_STACK];

// Each stack has a current number of Packages
// At the beginning each stack has 0 Packages
// Here we create a static array where we will store a number of Packages that are in each stack
// We assume here that the capacity of each stack is MAX_CAPACITY (which is 3)
int CurrentState[NUMBER_OF_STACK];

struct Package
{
   enum PackageType type;
   enum Colors color;
   struct Package *next;
};

//---------------------------------------------------------------------Going for shopping: Shopping struct

// a pointer to the first element of the shopping list
struct Shopping * queueFirst=NULL;
// a pointer to the last element of the shopping list
struct Shopping * queueLast=NULL;

// global variable that is used for assigning a next identifier 
// when a next robot is generated
int nextRobotID=-1;

struct Shopping
{
   int numberThingsToBuy; 
   int robot_id;
   struct Shopping *next;
};

