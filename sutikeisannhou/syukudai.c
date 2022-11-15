# include<stdio.h>
# include<math.h>
# include<stdlib.h>

#define N 3

double A[N][N];
double x[N], x_new[N];

int main(){
	int t,i,k;
	double r,r1,r2;
	double r_old;

	/*Matrix*/
	A[0][0]=rand()%10+1;	
	A[0][1]=rand()%10+1;
	A[0][2]=rand()%10+1;

	A[1][0]=A[0][1];	
	A[1][1]=rand()%10+1;
	A[1][2]=rand()%10+1;

	A[2][0]=A[0][2];	
	A[2][1]=A[1][2];
	A[2][2]=rand()%10+1;

	/*Initial vector*/

	x[0]=0.2;
	x[1]=0.3;
	x[2]=0.6;

	/*Loop Calculation*/

step1:
	t=t+1;
	/* new_x=A*x */

	for(i=0;i<N;i++){
		x_new[i]=0;
		for(k=0;k<N;k++){
			x_new[i]+=A[i][k]*x[k];
 
		}	
	}

	/*Reyleigh quotient*/
	r1 = r2 = 0.0;
	for(k=0;k<N;k++){
		r1+=x_new[k]*x[k];	
	}
	for(k=0;k<N;k++){
		r2+=x[k]*x[k];	
	}
	for(k=0;k<N;k++){
		x[k]=x_new[k];	
	}
	r=r1/r2;

	printf("r=%lf\n",r);

	if(t==1)goto step1;
	if(fabs(r-r_old)<10e-6) goto finish;

	r_old = r;
	goto step1;

finish:
	printf("The largest eigenvalue = %f\n",r);

	
}
