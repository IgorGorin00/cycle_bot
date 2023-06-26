# Overwiev

This Telegram bot applies different styles to the images sent to it using the CycleGAN model. 
It integrates the [CycleGAN](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix) model with the 
[python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/index.html) library.

## Installation

If you want to run this project locally, you need to
1. Clone this repo

- `git clone https://github.com/IgorGorin00/cycle_bot`
- `cd cycle_bot`

2. Create virtual environment and install dependencies


- `python3 -m venv myenv`
- `source myenv/bin/activate`
- `pip install -r requirements.txt`


## Usage

In order to use it, you will need to:

1. Set up the Telegram bot:

- Create a new Telegram bot using the BotFather and obtain the bot token

2. Configure bot token

- Create file `secret.py` by running `touch secret.py`, and in this file add `token = "YOUR_BOT_TOKEN"`

3. Create needed directories 

- In the project root, create the following directories using `mkdir data results data_cache/real data_cache/fake`:
    - data/ (for storing downloaded images)
    - results/ (for storing processed images)
    - data_cache/real/ (for storing cached real images)
    - data_cache/fake/ (for storing cached fake images)

4. Start the bot

- `python cycle_bot.py`

## Bot Commands

- /help: Display help information about the bot.
- /start: Start the bot and initiate the image translation process.
- Send a photo to the bot: The bot will apply different styles to the image and provide the transformed images as output.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, 
please open an issue or submit a pull request.
