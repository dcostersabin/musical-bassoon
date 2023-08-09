# Musical Bassoon

Your ultimate solution for efficient artist and song management. Designed exclusively for backend operations, Musical Bassoon Backend empowers you to effortlessly handle the CRUD (Create, Read, Update, Delete) operations for artists and songs. 



## Installation

Say goodbye to the 'It works on my machine' blues and hello to the Docker dazzle with our app! 
```bash

    git clone https://github.com/dcostersabin/musical-bassoon.git

    cd musical-bassoon

    docker build -t musical-bassoon .

    docker run --rm -d  -p 5000:5000 musical-bassoon:latest


```
    
## Health Check

When executed, the command should gracefully pirouette, unveiling a symphony of flawless output – a true code choreography!

```bash
  curl localhost:5000/

```
### Output 
```
{
  "status": "If You See This The Server Is Healthy"
}
```

