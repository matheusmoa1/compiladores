fun fib(n) {
  var res = 0;
  if n < 2 {
    res = n;
  } else {
    res = fib(n - 1) + fib(n - 2);
  }
  return res;
}

main {
  return fib(10);
}
