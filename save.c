// Author: Kiyoshi Yamamoto
// Class: CS370
// Date: April-29-2020
// email: kyamamo@rams.colostate.edu

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int main(int argc, char* argv[]) {

	const char* systemFilePath = "/home/pi/Documents/CS370/node_files/views/System_data.txt";
	const char* GPSFilePath = "/home/pi/Documents/CS370/node_files/views/GPS_data.txt";
	char GPSsave[82];
	char systemSave[85];
	time_t clock;
	struct tm *currTime;

	time(&clock);
	currTime = localtime(&clock);
	strftime(GPSsave, 82, "/home/pi/Documents/CS370/node_files/views/savedData/%H-%M-%S_%m-%d-%y_GPS_data.txt", currTime);
	strftime(systemSave, 85, "/home/pi/Documents/CS370/node_files/views/savedData/%H-%M-%S_%m-%d-%y_system_data.txt", currTime);

	FILE* gpsFile = fopen(GPSFilePath,"r");
	FILE* systemFile = fopen(systemFilePath,"r");
	FILE* saveGPS = fopen(GPSsave,"w");
	FILE* saveSystem = fopen(systemSave, "w");

	char ch = fgetc(gpsFile);
	while(!feof(gpsFile)) {
		fputc(ch, saveGPS);
		ch = fgetc(gpsFile);
	}
	ch = fgetc(systemFile);
	while(!feof(systemFile)) {
		fputc(ch, saveSystem);
		ch = fgetc(systemFile);
	}

	fclose(gpsFile);
	fclose(systemFile);
	fclose(saveGPS);
	fclose(saveSystem);

	return 0;
}
