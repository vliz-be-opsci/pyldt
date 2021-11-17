TODO: describe how to use the docker thingy 


build image

```bash
$ docker build . -t pysubyt
```

test if it runs
```bash 
$ docker run pysubyt --help
```

actually run pysubyt in the docker container accessing templates and input from the host

```bash
$ docker run \
    -v $(realpath .)/tests/templates:/tpl \
    -v $(realpath \.)/tests/in:/in  \
    pysubyt -t /tpl -i /in/data.csv -n 01-basic.ttl
```



TODO consider a bash function dock-subyt() that takes arguments to execute pysubyt via docker
- then provide that as a sh file that can be sourced
- as well as have a ```make docker``` target to have image build + source that ```docker build -t pysubit && source pysubyt-docker-define.sh```


dock-subyt 
**  args to manipulate (all optional)
   -t «path that should be made absolute and mapped to /tpl» 
   -i «path that should be made absolute and mapped to /in»/inputname
   -o «path that should be made absolute and mapped to /out»/outputname
   -s KEY «path that should be made absolute and mapped to /set-${KEY}/inputname
** args to pass through
   -n «name to pass through»
   -m «modifier to pass through»
   -h
   

