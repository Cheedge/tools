#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#define BUFFERSIZE 500
#define N 900
int main(int argc, char* argv[])
{
	FILE* fp_in;
	FILE* fp_out;
	double sq3=sqrt(3);
	double x[N];
	double y[N];
	double z[N];
	double Nex[N];
	int i;
	char buffer[BUFFERSIZE];
	for(i=0;i<argc;i++)
	{
		if(argc<1){
			printf("error argc=%d\n is wrong", argv[0]);
		}
		printf("argc is %d, argv[%d]=%s\n", argc, i, argv[i]);
	}
	double b = atof(argv[1]);
	int Num = atoi(argv[2]);
	printf("b=%s is reciprocal lattice longth, N=%s is the lines in the input file correspond to the num of x, y, z and Nex array.", argv[1], argv[2]);
	printf("input=%s is the old point data file, output=%s is the new point data file\n", argv[3], argv[4]); 
	if((fp_in=fopen(argv[3], "r"))==NULL || (fp_out=fopen(argv[4], "w"))==NULL)
	{
		printf("ERROR OPEN input FILE\n");
		return 1;
	}
	int j=0;
	while(fgets(buffer, BUFFERSIZE-1, fp_in) != NULL){
		sscanf(buffer, "%lf %lf %lf %lf", &x[j], &y[j], &z[j], &Nex[j]);
		//sscanf(buffer, "%lf %lf %lf %lf", x, y, z, Nex);
		j++;
	};
	for(i=0; i<N; i++)
	{
	//	printf("%lf	%lf	%lf\n", x[i], y[i], Nex[i]);
		if(abs(y[i])<=sq3)
		{
			if(x[i]>=0)
			{
				if(sq3*(x[i]-b)+y[i]>0 || sq3*(x[i]-b)-y[i]>0)
				{
					Nex[i]=0.0;
				}
			}
			else
			{
				if(sq3*(x[i]+b)-y[i]<0 || sq3*(x[i]+b)+y[i]<0)
				{
					Nex[i]=0.0;
				}
			}
		}
		else
		{
			Nex[i]=0.0;
		}
		fprintf(fp_out, "%16.8f	%16.8f	%16.8f\n", x[i], y[i], Nex[i]);
	}
	//printf("%s\n", buffer);
	fclose(fp_in);
	fclose(fp_out);
	return 0;
}
