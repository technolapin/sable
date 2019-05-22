#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <math.h>



const int TAILLEBUF = 64;

char * lit_ligne(int fd)
{
  int i = 0;
  char *c = malloc(TAILLEBUF+1);
  do {
    if( (read(fd, &c[i],1) <= 0) || (i == TAILLEBUF)){
      free(c);
      return NULL;
    }
    i++;
  } while(c[i-1] != '\n');
  c[i] = '\0';
  return c;
}

int ecrit_ligne(int fd, char *c)
{
  int taille = strlen(c);
  if(write(fd, c, taille) == taille)
    return 1;
  else return 0;
}



int
main(int argc, char ** argv)
{
  if (argc != 4)
  {
    printf("Usage: fusionne_proches in.list out.list\n");
    return 0;
  }

  char* nom_entree = argv[1];
  char* nom_sortie = argv[2];
  double circlisme;
  sscanf(argv[3], "%lf", &circlisme);
  printf("criclisme = %lf \n", circlisme);
  int fd;
  fd = open(nom_entree, 0);

  char* ligne;
  int x, y , a;
  int n_el;
  char mode;
  sscanf(lit_ligne(fd), "%c %d\n", &mode, &n_el);

  int centres[n_el][3];

  for (int i = 0; i<n_el; i++)
  {
    ligne = lit_ligne(fd);
    sscanf(ligne, "%d %d %d", &x, &y, &a);
    centres[i][0] = x;
    centres[i][1] = y;
    centres[i][2] = a;
  }
  close(fd);


  printf("A n_el = %d \n", n_el);

  int flag = 1;
  while (flag)
  {
    flag = 0;
    for (int i_a=0; i_a < n_el && !flag; i_a++)
    {
      for (int i_b=0; i_b < n_el && !flag; i_b++)
      {
	if (i_a != i_b)
	{
	  double x_a = (double) centres[i_a][0];
	  double x_b = (double) centres[i_b][0];
	  double y_a = (double) centres[i_a][1];
	  double y_b = (double) centres[i_b][1];
	  double area_a = (double) centres[i_a][2];
	  double area_b = (double) centres[i_b][2];
	  
	  double dist =
	    sqrt( pow(x_a - x_b, 2) +
		  pow(y_a - y_b, 2) );
	  
	  double r_a = sqrt(area_a/3.141592653589793);
	  double r_b = sqrt(area_b/3.141592653589793);
	  printf("dist entre %d et %d = %lf %lf\n", i_a, i_b, dist, (r_a+r_b)*circlisme);
	  if (dist < (r_a+r_b)*circlisme)
	  {
	    printf("-1\n");
	    centres[i_a][0] = (int) (x_a*area_a + x_b*area_b)/(area_a+area_b);
	    centres[i_a][1] = (int) (y_a*area_a + y_b*area_b)/(area_a+area_b);
	    centres[i_a][2] = (int) area_a+area_b;
	    
	    n_el--;
	    centres[i_b][0] = centres[n_el][0];
	    centres[i_b][1] = centres[n_el][1];
	    centres[i_b][2] = centres[n_el][2];
	    flag = 1;
	  }
	}
      }
    }
  }
  printf("B n_el = %d \n", n_el);
  fd = open(nom_sortie, O_WRONLY|O_CREAT|O_TRUNC, 0666);
  
  sprintf(ligne, "_ %d\n", n_el);
  ecrit_ligne(fd, ligne);

  for (int i = 0; i < n_el; i++)
  {
    sprintf(ligne, "%d %d %d\n", centres[i][0], centres[i][1], centres[i][2]);
    ecrit_ligne(fd, ligne);
  }
  
  close(fd);


  
  
  return 0;
}
