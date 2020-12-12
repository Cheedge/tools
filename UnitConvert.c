#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#include<stddef.h>
/*2020-12-11 11:59*/
/*convert unit Hartree(a.u.)<-->SI
convert atomic unit or SI unit to other energy unit:
omega(eV), freq(THz), freq(cm-1), lambda(nm), period(fs) convert to others.
*/
#define pi 3.141592653589793
#define csol 299792458

int main(int argc, char *argv[])
{
	double atomuni, hw, freq_cm1, freq_thz, lambda, period;
	double num;
	//char *unit;
	//notice here cant use *unit, it still charactor cant get argv[2]'s value.
	char unit[5];
	FILE* fp_out;
	fp_out = fopen("unit_convert_file.dat", "w");

	if (argc != 3)
	{
		printf("command as \"%s value unit\", \"unit can be one of \"a.u.\", \"eV\", \"nm\", \"cm-1\", \"THz\", \"fs\" six units\n", argv[0]);
		exit(1);
	}
	if (sscanf(argv[1], "%lf", &num) != 1)
	{
		printf("first input is the value you need to convert\n");
		exit(1);
	}
	if (sscanf(argv[2], "%s", unit) != 1)
	{
		printf("%s is the input unit\n", argv[2]);
		printf("2nd input is one of \"a.u.\", \"eV\", \"nm\", \"cm-1\", \"THz\", \"fs\" six units\n");
		exit(1);
	}
	
	if (strcmp(unit, "a.u.")==0) 
	{
		//1 hartree = 27.211386245988 eV
		atomuni = num;
		hw = 27.211386245988 * num;
		freq_thz = 1000*hw/4.135667694389856;
		freq_cm1 = pow(10,10)*freq_thz/csol;
		lambda = csol*0.001/freq_thz;
		period = 1000.0/freq_thz;
	}
	else if (strcmp(unit, "eV")==0)
	{
		hw = num;
		atomuni = num / 27.211386245988;
		freq_thz = 1000*num/4.135667694389856;
		freq_cm1 = pow(10,10)*freq_thz/csol;
		lambda = csol*0.001/freq_thz;
		period = 1000.0/freq_thz;
	}
	else if (strcmp(unit, "nm")==0)
	{
		//1 bohr = 0.529177210903 A = 5.29177210903 nm
		//lambda(wave length: nm)=csol/freq(tHz) *10^5
		lambda = num;
		freq_cm1 = 10000000.0/num;
		atomuni = num / 5.29177210903;
		freq_thz = 0.001*csol / num;
		hw = 4.135667694389856*freq_thz*0.001;
		period = 1000.0/freq_thz;
	}
	else if (strcmp(unit, "cm-1")==0)
	{
		//1 cm-1= 10^-7 nm-1
		//1 cm-1=csol
		freq_cm1 = num;
		freq_thz = freq_cm1*csol/pow(10,10);
		hw = freq_thz * 4.135667694389856 * 0.001;
		atomuni = hw/27.211386245988;
		period = 1000.0/freq_thz;
		lambda = csol*0.001/freq_thz;
	}
	else if (strcmp(unit, "THz")==0)
	{
		//1 hbar*omega= 1 eV =1.602176634×10^−19 J
		//1 hbar = 1.054571817×10^−34 Js
		//omega = 1.602/1.055 * 10^15 1/s =1.5192674488095106*10^15 1/s 
		//omega = 2*pi*freq_hz
		//thz-->eV: hw=hbar*omega (J)= hbar*omega/1.602 (eV)= 1.055/1.602 *10^-15 * 2pi* freq_thz *10^12= 0.6582119565476074*10^-3*2pi (eV)=4.135667694389856*10^-3*freq_thz(eV)= 4.135667694389856*freq_thz(meV)
		//period = 1/freq_hz
		freq_thz = num;
		hw = 4.135667694389856*freq_thz*0.001;
		atomuni = hw/27.211386245988;
		freq_cm1 = pow(10,10)*freq_thz/csol;
		period = 1000.0/freq_thz;
		lambda = csol*0.001/freq_thz;
	}
	else if (strcmp(unit, "fs")==0)
	{
		//1 atomuni = 24.188843265857 as = 0.024188843265857 fs
		period = num;
		freq_thz = 1000.0/period;
		hw = 4.135667694389856*freq_thz*0.001;
		atomuni = 0.001 * num / 24.188843265857;
		freq_cm1 = pow(10,10)*freq_thz/csol;
		lambda = csol*0.001/freq_thz;
	}
	else
	{
		printf("only \"a.u.\", \"eV\", \"nm\", \"cm-1\", \"THz\", \"fs\" units can be converted\n");
		exit(1);
	}
	//decide the type of light by range of wave length (lambda)
	//refer to web: http://halas.rice.edu/conversions
	fprintf(fp_out, "input is %18.16lf %s\n", num, unit);
	fprintf(fp_out, "=%3.16e a.u.\n", atomuni);
	fprintf(fp_out, "=%3.16e eV\n", hw);
	fprintf(fp_out, "=%3.16e nm = %3.16e A\n", lambda, 10*lambda);
	fprintf(fp_out, "=%3.16e cm-1\n", freq_cm1);
	fprintf(fp_out, "=%3.16e THz\n", freq_thz);
	fprintf(fp_out, "=%3.16e fs\n", period);
//input atom number and force, calculte corresponding phonon displacement: dis.
	fclose(fp_out);
	return 0;
}

