main(){FILE*f=fopen("input/day01_input.txt","r");int a,b,c,d,s=0;fscanf(f,"%d\n%d\n%d\n",&a,&b,&c);while(!feof(f)){fscanf(f,"%d\n",&d);s+=a<d;a=b;b=c;c=d;}printf("%d\n",s);}