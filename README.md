# micro VADR ( a VADR microservice for validating SARS-CoV2 sequences)

## About
This repo wraps VADR (https://github.com/ncbi/vadr) into a deployable containerized  REST server where one can post sequences and get results. 

## Usage
Clone the repo and run command `docker-compose up`. You may want to pull the image from Dockerhub prior to running this command to skip building the image yourself. Once the server is running, you can find a swagger front end at http://localhost:5001/ (default port as specified in docker-compose).

### Endpoints
There are two main endpoints...

#### /vadr/
This accepts a post request of the form...
```
    {
        "sequence_name": string,
        "sequence": string,
        "password": string,
    }
```
and returns a paylod of the form...
```
    {
        "status": "success",
        "message": "New run submitted",
        "process_id": NNNNNNNN
    }
```
* unless something goes wrong
The process_id will always be a random 8 digit number which can be passed into the next endpoint via a get request. The password field is included as a cheap way to make sure only good requests go on to use compute resources to processes the submitted sequece. The password can be changed via the MICROVADRPASS enviornment variable in the docker-compose file. 

#### /vadr/<process_id>
This endpoint accepts a process_id. If the run has finished, the response will look like...
```
{
  "sequence_name": "[INPUT_SEQUENCE_NAME]]",
  "sequence": [INPUT_SEQUENCE],
  "results": {
    "VADR_status": [PASS/FAIL],
    "seq_length": "29903",
    "model_used": "NC_045512",
    "sequence_features": [
      {
        "type": "gene",
        "name": "ORF1ab",
        "start": "266",
        "end": "21555",
        "seq_coords": "266..21555:+",
        "alerts": "-"
      }...
    ]
}
```

## Dockerhub image...
https://hub.docker.com/r/notmaurox/micro_vadr
