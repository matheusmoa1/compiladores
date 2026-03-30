a = 10;
b = 20;
delta = 0;
{
  delta = a - b;
  if delta < 0 {
    delta = 0 - delta;
  } else {
    delta = delta;
  }
  return delta;
}