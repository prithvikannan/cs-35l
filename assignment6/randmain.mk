randmain:
	$(CC) $(CFLAGS) -c randmain.c -o randmain.o
	$(CC) $(CFLAGS) -c randcpuid.c -o randcpuid.o
	$(CC) $(CFLAGS) -o randmain randmain.o randcpuid.o -ldl -Wl,-rpath=$(PWD) 

randlibhw.so:
	$(CC) $(CFLAGS) -c -fPIC randlibhw.c -o randlibhw.o
	$(CC) $(CFLAGS) -shared randlibhw.o -o randlibhw.so

randlibsw.so:
	$(CC) $(CFLAGS) -c -fPIC randlibsw.c -o randlibsw.o
	$(CC) $(CFLAGS) -shared randlibsw.o -o randlibsw.so