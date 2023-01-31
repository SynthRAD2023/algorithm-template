<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU GPL-v3.0][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://synthrad2023.grand-challenge.org/">
    <img src="./SynthRAD_banner.png" alt="Logo" width="770" height="160">
  </a>


  <p align="center">
    Algorithm template docker for submissions to
<a href="https://synthrad2023.grand-challenge.org/"><strong>SynthRAD2023 Grand Challenge</strong></a>
  <br />
    <a href="https://github.com/SynthRAD2023/algorithm-template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SynthRAD2023/algorithm-template">View Demo</a>
    ·
    <a href="https://github.com/SynthRAD2023/algorithm-template/issues">Report Bug</a>
    ·
    <a href="https://github.com/SynthRAD2023/algorithm-template/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Goal](#goal)
* [Getting Started](#getting-started)
  * [Dependencies](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Function Descriptions](#functions-descriptions)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
<!--
* [Acknowledgements](#acknowledgements)
-->


<!-- ABOUT THE PROJECT -->
## Goal

The source code for the participant algorithm container for
SynthRAD2023, generated with
evalutils version 0.3.1.

<!-- GETTING STARTED -->
## Getting Started

### Dependencies

The user should have access to Docker [https://docs.docker.com/].
The requirements, specified in `requirements.txt` are:
* evalutils v0.3.1
* scikit-learn v0.24.2
* scipy v1.6.3
* scikit-image v0.19.3

### Installation

1. Clone the repo
```sh
git clone https://github.com/SynthRAD2023/algorithm-template.git
```
or
```sh
git clone git@github.com:SynthRAD2023/algorithm-template.git
```

<!-- USAGE EXAMPLES -->

## Usage

1. Data is to be organized so that the input files to run the algorithm on are placed in the `test` folder.
The names of the files should match. 
2. Run `test.sh`

### Functions Descriptions

**test.sh**

	description:
	create the docker and run the algorithm-template
	
	command line usage:
	./test.sh

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/SynthRAD2023/algorithm-template/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create.
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Suraj Pai - b.pai@maastrichtuniversity.nl
Matteo Maspero - [@matteomasperonl](https://twitter.com/matteomasperonl) - m.maspero@umcutrecht.nl

Project Link: [https://github.com/SynthRAD2023/algorithm-template](https://github.com/SynthRAD2023/algorithm-template)


<!-- ACKNOWLEDGEMENTS 
## Acknowledgements

* []()
* []()
* []()
-->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/
#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/SynthRAD2023/repo.svg?style=flat-square
[contributors-url]: https://github.com/SynthRAD2023/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SynthRAD2023/repo.svg?style=flat-square
[forks-url]: https://github.com/SynthRAD2023/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/SynthRAD2023/repo.svg?style=flat-square
[stars-url]: https://github.com/SynthRAD2023/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/SynthRAD2023/repo.svg?style=flat-square
[issues-url]: https://github.com/SynthRAD2023/repo/issues
[license-shield]: https://img.shields.io/github/license/SynthRAD2023/repo.svg?style=flat-square
[license-url]: https://github.com/SynthRAD2023/repo/blob/master/LICENSE.txt