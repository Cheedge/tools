#include<stdio.h>// printf
#include<stdlib.h>//strtol
#include<math.h>

#define twopi 6.283185307179586
#define BUFFSIZE 1000

int main(int argc, char *argv[])
{
	long int N; 
	char* p;// for strtol function.
	int i,j,t=0;
	double freq=0.0, invdt;
	double bufx, bufz;
	double x;
	//double *x;
	double *efieldy;
	double *fft_e_im, *fft_e_rl;
	FILE* f_out;
	FILE* fp;//=fopen(argv[1], "r");
	char buff[BUFFSIZE];
/* get M, dx */
    if((fp = fopen(argv[1], "r"))==NULL)
    {
		// input file is EFIELD.OUT.
        printf("command should be: \"%s <input_file> row_num\" ", argv[0]);
        return 1;
    }
    printf("<file_input> is %s\n", argv[1]);
	printf("num of rows is %s\n", argv[2]);
	//if (sscanf(argv[2], "%d", &N) != 1)
	N=strtol(argv[2], &p, 10);
	if (N==0)
	{
		printf("give M: number of points same as rows\n");
		return 1;
		//exit(1);
	}
	//printf(" %d", N);

//	x=(double*)malloc(sizeof(double)*N);
	efieldy=(double*)malloc(sizeof(double)*N);
	fft_e_rl=(double*)malloc(sizeof(double)*N);
	fft_e_im=(double*)malloc(sizeof(double)*N);

	f_out=fopen("FFT_EFIELD.DAT", "w");
	while(fgets(buff, BUFFSIZE-1, fp) !=NULL)
	{
		sscanf(buff, "%lf %lf %lf %lf", &x, &bufx, &efieldy[t], &bufz);
		t++;
	}
	invdt=1.0/N;
	for (i=0; i<N; i++)
	{
		fft_e_im[i]=0.0;
		fft_e_rl[i]=0.0;
		for (j=0; j<N; j++)
		{
			fft_e_rl[i]+=efieldy[j]*cos(i*j*twopi/N);
			fft_e_im[i]-=efieldy[j]*sin(i*j*twopi/N);
		}
	}

	for (i=0; i<N; i++)
	{
		freq+=invdt;
		fprintf(f_out, "%.11lf  %.11lf\n", freq, sqrt(pow(fft_e_rl[i],2)+pow(fft_e_im[i],2)));
	}
	fclose(f_out);
	fclose(fp);
//	free(x);
	free(efieldy);
	return 0;
}
