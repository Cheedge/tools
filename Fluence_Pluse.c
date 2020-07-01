#include<stdio.h>
#include<math.h>
#include<stdlib.h>
/*This is a program to calculate the fluence of a laser pulse.
 * notice: because use the function pow(), here should use compile command as:
 * gcc ...... -lm
 * because pow() store in the math library libm.a, math.h only declare it, BUT not define it. math lib libm.a store the defination. so add param -lm to find the def.
*/
#define BUFFSIZE 500
#define BETA 848.89650302
#define ALPHA 0.0072973525693

int main(int argc, char* argv[])
{
	int i, j, k, N;
	double fluence;
	double *Ax, *Ay, *Az, *Ex, *Ey, *Ez, *t;
	char buffer[BUFFSIZE], bu[5];
	char* in_file;
	FILE* fpt_in;
	FILE* fpt_out;

	if(argc < 2)
	{
		printf("problem input, the 2nd input should as <file_input> %s", argv[1]);
		return 1;
	}
	//fpt_in = argv[1];
	if((fpt_in = fopen(argv[1], "r"))==NULL)
	{
		printf("problem input files");
		return 1;
	}
	//N = fgetc(fpt_in);
	i = 0;
	fpt_out = fopen("EFIELD.DAT", "w");

	fgets(buffer, 20, fpt_in);
	sscanf(buffer, "%d %s %s %s %s %s", &N, &bu[0], &bu[1], &bu[2], &bu[3], &bu[4]);
	Ax = (double *)malloc(sizeof(double)*(N+1));
	Ay = (double *)malloc(sizeof(double)*(N+1));
	Az = (double *)malloc(sizeof(double)*(N+1));
	t = (double *)malloc(sizeof(double)*(N+1));
	Ex = (double *)malloc(sizeof(double)*(N+1));
	Ey = (double *)malloc(sizeof(double)*(N+1));
	Ez = (double *)malloc(sizeof(double)*(N+1));
	while(fgets(buffer, BUFFSIZE-1, fpt_in)!=NULL)
	{
		sscanf(buffer, "%d %lf %le %le %le", &k, &t[i], &Ax[i], &Ay[i], &Az[i]);
	//	fprintf(fpt_out, "%d %lf %le %le %le\n", k, t[i], Ax[i], Ay[i], Az[i]);
		i++;
	}
	double dt=t[2];
	Ex[0] = 0.0;
	Ey[0] = 0.0;
	Ez[0] = 0.0;
	//printf("%d\n", N);
	for(i=1; i<N; i++)
	{
		Ex[i] = -ALPHA*(Ax[i+1]-Ax[i])/dt;
		Ey[i] = -ALPHA*(Ay[i+1]-Ay[i])/dt;
		Ez[i] = -ALPHA*(Az[i+1]-Az[i])/dt;
		fprintf(fpt_out, "%d %lf %le %le %le\n", i, t[i], Ex[i], Ey[i], Ez[i]);
	}
	for(j=0; j<N; j++)
	{
		fluence = pow(Ex[j], 2) + pow(Ey[j], 2) + pow(Ez[j], 2)  + fluence;
	}
	fluence = fluence * dt;
	printf("the fluence is %16.8f a.u.\n", fluence);
	printf("also in normal unit it is %16.8f mJ/cm^2\n",fluence*BETA);


	fclose(fpt_in);
	fclose(fpt_out);
	free(Ax);
	free(Ay);
	free(Az);
	free(Ex);
	free(Ey);
	free(Ez);
	return 0;
}
