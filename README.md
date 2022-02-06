# rl-traingenerator

Automatic code generator for training Reinforcement Learning policies:joystick:

<p align="center">
    <img src="docs/assets/rl-traingenerator.gif" width=600>
</p>

<h3 align="center">
    Try it out: <br>
    <a href="https://rl-traingenerator.herokuapp.com/">https://rl-traingenerator.herokuapp.com/</a>
</h3>

<br>

Generate custom template code to train you reinforcement learning policy using a simple web UI built with [streamlit](https://www.streamlit.io/).
It includes different environments and can be expanded to support multiple policies and frameworks with an high level of flexible hyperparameters customization.
The generated code can be easily downloaded as .py file or Jupyter Notebook so to immediately start training your model or use it as a baseline for your project.
The backbone of this project has been taken from this [repository](https://traingenerator.jrieke.com) where you can contribute with your own template.

## Features

Supported frameworks:
- [Tianshou](https://github.com/thu-ml/tianshou)

Supported policies:
- DQN
- More to come...

Compatible environments:
- Atari: Pong, Breakout, MsPacman, ...
- Classic Control: CartPole, Acrobot
- Box2D: LunarLander

---

## Usage

Clone this repository and set up the environment:
```bash
git clone https://github.com/davide97l/rl-traingenerator/
cd rl-traingenerator
pip install -r requirements.txt
```
Run it locally:
```bash
streamlit run app/main.py
```
Deploying to Heroku:
```
heroku create
git push heroku main
heroku open
```
Update deployed app:
```
git push heroku main
```

## Support
If you found this project interesting please support me by giving it a :star:, I would really appreciate it :grinning: