# April Tag Wavy Hand Auto Controller

## Install
you will likely need to modify the `requirements.txt` file
 - Remove the -e line and replace it with `apriltag==0.0.16`
 - If this doesn't work, you will need to build and install the april tag library yourself

### .env setup
 - Copy `example.env` to `.env`
   - ### There are a few options to do this
   - `cp example.env .env`
   - `cat example.env > .env`
   - Or use your OS's gui tools of choice
 - Set your RoboRIO ip address in the `.env` file -- See [Ip Configurations](https://docs.wpilib.org/en/latest/docs/networking/networking-introduction/ip-configurations.html)


## Usage
 - To run: `python main.py`

The only command line option that I added on top of the standard april tag options is `-a` or `--always-active` which enables continuous detection, even when not connected to network tables

 - Get all options: `python main.py -h`

