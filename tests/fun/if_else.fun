var a = 10;
var b = 20;
var delta = 0;
main {
  delta = a - b;
  if delta < 0 {
    delta = 0 - delta;
  } else {
    delta = delta;
  }
  return delta;
}
