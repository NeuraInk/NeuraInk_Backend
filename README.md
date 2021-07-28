# NeuraInk_Backend

The backend service of NeuraInk uses the [CycleGAN](https://junyanz.github.io/CycleGAN/) machine learning algorithm to implement the inkwash photo transformation.
 
### How to run on AWS EC2 Instance / Locally
1. Create an EC2 Instance (skip this step if you are running locally)
2. git clone the NeuraInk_Backend repo
3. Run `chmod +x ./setup.sh ./start.sh` to give executeable permissions to both bash files
4. Run `./setup.sh` to setup the virtual environment
5. Run `./start.sh` to start the backend services

### Reference
[CycleGAN](https://junyanz.github.io/CycleGAN/)
