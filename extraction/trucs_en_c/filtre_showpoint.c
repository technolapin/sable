#include <stdio.h>

// ce petit programme sert à filter la sortie de showpoint
// usage: showpoint image.pgm x y z | 
int
main(void)
{
  char typ[10];
  int rs, cs, ds, x, y, z, val;
  scanf("rs=%d cs=%d ds=%d type=%s x=%d y=%d z=%d \n%d", &rs, &cs, &ds, typ, &x, &y, &z, &val);
  printf("%d %d %d\n", x, y, val);
  return 0;
}
