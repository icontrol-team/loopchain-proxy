# Loopchain-proxy by ICONTROL

 Loopchain is a high-performance Blockchain Consensus & Network engine of ICON project.
However, this is not a origin Loopchain project. If you want. Visit here: https://github.com/icon-project/loopchain

## What is Loopchain-proxy
 This is a relay server to ICON network.
 This proxy can find the best node under the desired conditions.

## Getting Started

### Requirements

 This project uses the original icon-rpc-server, but does not change the original source. 
 This project has its own plugin model. So you can add functionality without changing the original source.

1. **Python 3.7.x**

    We recommend to create an isolated Python 3 virtual environment with [virtualenv].

    ```bash
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```

    > **_NOTE:_** Now we support 3.7.x only. Please upgrade python version to 3.7.x

1. **ICON RPC Server**

    ICON RPC Server
    ```bash
    $ git clone https://github.com/icon-project/icon-rpc-server.git
    $ pip install -e icon-rpc-server
    ```

1. **Other Dependencies**

    If you face some problems before run this project, please refer to the Origin Loopchain Project. 
    This one requires just same execution environment.


### Run

```bash
$ ./launcher.py -p 9000 -c ./conf/mainnet/iconrpcserver_conf.json
```
