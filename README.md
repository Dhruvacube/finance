<p align="center">
  <a href="https://github.com/student-finance/finance/">
    <img src="https://raw.githubusercontent.com/student-finance/finance/master/static/logo.png" alt="finance logo" height="75">
  </a>
</p>


<h3 align="center">Finance</h3>

<p align="center">
  <img src="https://img.shields.io/github/pipenv/locked/python-version/student-finance/finance" alt="GitHub Pipenv locked Python version">
  <img src="https://img.shields.io/github/pipenv/locked/dependency-version/student-finance/finance/django" alt="GitHub Pipenv locked dependency version">
  <img src="https://img.shields.io/github/license/student-finance/finance" alt="GitHub">
  <img src="https://img.shields.io/github/v/tag/student-finance/finance" alt="GitHub tag (latest by date)">
  <img src="https://img.shields.io/github/commits-since/student-finance/finance/v1.5.7" alt="GitHub commits since latest release (by date)">
</p>

<p align="center">
  A simple web app to understand and control your expenses.
  <br>
  Designed to be self-hosted.
  <br>
  <em>Inspired by <a href="https://github.com/inoda/ontrack">OnTrack</a>.</em>
</p>

## Table of contents
* [About](#About)
* [Features](#Features)
* [Installation & Configuration](#installation--configuration)
  * [Docker method](#docker-method)
* [Updating](#updating)
  * [Docker method](#docker-method-1)
* [License](#license)
* [Contributing](#contributing)
* [Developer documentation](#developer-documentation)
  * [The development environment](#the-development-environment)
    * [Set up](#set-up)
    * [Usage](#usage)




## About

[![Mentioned in Awesome Selfhosted](https://awesome.re/mentioned-badge.svg)](https://github.com/awesome-selfhosted/awesome-selfhosted)

It is important to control your budget and know where your money goes. I've tried lots of different apps and methods, but none have really convinced me. So I designed and developed finance, a simple and efficient application that meets my needs.

And it's also available for you.

## Features

A basic authorization system exists but this application is not intended to be hosted on a public network (yet?). It is designed to be self-hosted locally (e.g. on a Raspberry Pi) and used by a few users within the same household. Also you can use [Cloudflare Zero Trust](https://www.cloudflare.com/products/zero-trust/) if you want it to be hosted on the public internet.

#### 1. Categories

Define categories, and their color.


#### 2. Sheet

Add dated and categorized expenses. They are automatically grouped by month (i.e. sheet).

#### 3. Overview

Analyze the overall statistics.

#### 4. History

Explore and filter all expenses.

## Installation & Configuration

   **Currency formatting**

   In finance, money is represented by positive decimals of the form "xxxxxxxx.yy". The user is free to change the formatting to use the currency of their choice, by setting the following environment variables:

   * `CURRENCY_GROUP_SEPARATOR`: A single character which separates the whole number into groups of 3 digits.<sup>1</sup>
   * `CURRENCY_DECIMAL_SEPARATOR`: A single character that separates the whole part from the decimal part.<sup>1</sup>
   * `CURRENCY_PREFIX`: A string placed in front of the number.<sup>1</sup>
   * `CURRENCY_SUFFIX`: A string placed behind the number.<sup>1</sup>

   By default, it formats money as French euros. For instance, here's how to format as US dollars:

   ```
   CURRENCY_GROUP_SEPARATOR=,
   CURRENCY_DECIMAL_SEPARATOR=.
   CURRENCY_PREFIX=$
   CURRENCY_SUFFIX=
   ```

   ---

   <sup>1</sup>: Note: If it contains spaces, make sure to use [non-breaking spaces](https://en.wikipedia.org/wiki/Non-breaking_space). This is simply to prevent visual "glitches".


8. Start cron inside the container:

   ```bash
   docker-compose exec finance service cron start
   ```


## License

Distributed under the GPLv3 License. See `COPYING` for more information.


## Contributing

I maintain this project primarily for my own use. If you can think of any relevant changes that should be incorporated into the code, you can contribute by opening an issue or submitting a pull request.

See the [Developer documentation](#developer-documentation) section below for more information.

## Developer documentation

**_This section is WIP_**

### The development environment

#### Set up

1. Install [Pipenv](https://pypi.org/project/pipenv/), if you haven't already.

   Pipenv is used to manage dependencies and the virtual environment.
   Note: finance currently targets **Python 3.8**, so **make sure it is installed too**.

2. Set up the virtual environment by executing the following command:

   ```bash
   pipenv install --dev
   ```

   This action will install both develop and default packages.

#### Usage

When you start a new development session, run the following command:

```bash
pipenv shell
```

This action spawns a shell within the virtualenv.


---

**You should now be able to work.**

Since finance is primarily a Django project, you should read [Django's documentation](https://docs.djangoproject.com/en/3.1/) if you are not familiar with it already.

