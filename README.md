# NeuralWaifu (Temporarily - Jarvis) v1.0.3 (very early)
Voice Assistant created using Python and neural networks
The main project challenges we try to achieve is:
 - 100% offline (no cloud)
 - Open source (full transparency)
 - No data collection (we respect your privacy)

## Neural Networks
Used neural networks:
 - Speech to text (STT):
   - Vosk Speech Recognition Toolkit via Vosk-rs
 - Chat:
   - ChatGPT
 - Text to speech (TTS):
   - Silero TTS

## To run the program(Windows)
For start, you need Python version 3.0 and higher
To compile the project you should create python project venv and build it with ```pip install -r requirements.txt``` command.
Then you need to install num2t4ru library. Actual version you can find at this link: https://github.com/Yuego/num2t4ru?ysclid=mayb995m44884371024
Also, you should download model of Vosk to ```app\modules\core\logic``` folder.
You can get the latest from the official website.
The one I was using is small.
Run ```app\modules\core\logic\main.py```
Also, check ```config.ini``` and ```config.py``` and set required values (api key, device index).

## Supported Languages
Currently, only Russian language is supported.

## Author
Popov Gleb

## Newest version
The last commit you can find at this link: https://github.com/Gleb-a-p/NeuralWaifu.
Also, you can see all commit tree and choose any version.

## License
Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg

See LICENSE.txt file for more details.
