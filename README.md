# Python Selenium Tutorial

This page is a guide for crafting a [Selenium][1] script with [Python][2] using the [Selenium with Python][3] bindings.

## Installation

### IDE

You can use any text editor to write a [Python][2] script, but there are a few free IDE which make the experience smoother:
- [VS Code](https://code.visualstudio.com/)
- [PyCharm - Community Edition](https://www.jetbrains.com/pycharm/)
- [Spyder](https://www.spyder-ide.org/)

### Python Interpreter

There are a few approaches to install [Python][2], the most straight foward is to download the installer from
the officail site here and follow the instructions for installing **Python 3.8.11** or greater:
- https://www.python.org/downloads/

Versioning in [Python][2] is typically handled at the minor [symver](https://semver.org/), meaning **3.9** introduces different features
which may be incompatible with code written in **3.8**. Ordinarily this is not a huge concern, but it is 
possible to have multiple versions installed on the same system with the use of [Virtual Environments][4].

A popular package which makes it easier to work with multiple [Virtual Environments][4] is [Anadonda's conda][5]
package. The main difference between these two approaches, is how you switch between the environments,
and remove the need to compile any packages. Either installation will work for this guide, so long as you're 
working on a version in the **3.8** family.

### Selenium

[Selenium][1] comes in a lot of different varieties, and can work with a large number of programming languages.
The installation guide at [Selenium with Python](#selenium-with-python) offers the quickest path, involving
downloading and installing the [Drivers][6].

For this guide, I use the [ChromeDriver][7] for whatever the latest release happens to be. These release numbers
typically follow the same pattern as the [Chrome Browser][8]. Websites that don't work on the [Chrome Browser][8]
may not work with the [ChromeDriver][7] in [Selenium][1].

### Selenium with Python

The documented [Installation][9] guide on the homepage for [Selenium with Python][3] does a detailed job of 
explaining how to install the bindings for [Selenium][1].

### Chrome Extensions

The [Chrome Browser][8] has a number of extensions which can make scraping a website with Selenium easier, these
are available in the [Chrome Web Store][10]. Some I find useful are:
- [XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl)
- [Selenium IDE](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)

These are useful when analyzing a website you wish to create a [Python][2] script to traverse. Although the 
[Chrome DevTools](https://developer.chrome.com/docs/devtools/) are the main source when scraping a site.

## Website Lanugages

There are multiple ways to interact with a rendered HTML website, otherwise refered to as a [DOM][13].

[Selenium][1] works by traversing the [DOM][13], and interacting with elements of that [DOM][13] which are rendered in
the browser. If you're not familiar with website design, it may help to become familiar with the basics. 

For creating a [Python][2] script to interact with a website through Selenium, you don't need to concern yourself with
any JavaScript (Selenium will handle that for you). You also don't need to worry that much about CSS, it's the core
HTML [DOM][13] which we'll need to understand the basics of.

For the [Python][2] script, we're going to be searching for [DOM][13] elements, and interacting with them directly.

### XPath

[XPath][11] is a query language for selecting nodes from an XML document, but also works for selecting nodes
from HTML documents. Some websites will dynamically generate the DOM rendered in the browser, but we can still
use [XPath][11] to query the DOM to extract out the exact elements we want to interact with via [Selenium with Python][3].

There are plenty of guides online to learn the query syntax:
- https://devhints.io/xpath

### CSS Selectors

[CSS][12] is a style sheet language for describing presentation of documents, like HTML. It also has a well
established pattern, which you can write [Selectors](https://en.wikipedia.org/wiki/CSS#Selector) for, to select
specific elements in the rendered DOM. Some people find parsing the DOM through CSS easier, and if you already
know the CSS syntax, it can be.

## My first script

This other guide covers a scalable approach towards scraping data into a database:
- https://github.com/szelenka/prefect-webscraper-example

However, for scraping a simple site to enter in information on a HTML form, there's [example.py](./example.py)
which has comments added to the various methods within.

## Executing from CLI

Once you're comfortable with the code in [example.py](./example.py), you can trigger it from a command terminal. To see a list of all the input variables, you can call the `help` command:

```bash
python example.py -h
```

To run it to look for availability at 8:10 or 8:30 next Tuesday for members "Doe, John" and "Doe, Jane", you can call:

```bash
python example.py --day_of_week="Tuesday" --tee_times="08:10|08:30" --players="Doe, John|Doe, Jane"
```

### User Credentials

For any of this to work, you'll need to provide the user credentials in a text file. This text file should 
be kept in a secure location, and have the structure:

```text
USERNAME PASSWORD
```

Where there's a space character ' ' between the authenticated username and password. 

[1]: https://www.selenium.dev/
[2]: https://www.python.org/
[3]: https://selenium-python.readthedocs.io/index.html
[4]: https://docs.python.org/3.8/library/venv.html
[5]: https://anaconda.org/anaconda/conda
[6]: https://selenium-python.readthedocs.io/installation.html#drivers
[7]: https://sites.google.com/a/chromium.org/chromedriver/downloads
[8]: https://www.google.com/chrome/
[9]: https://selenium-python.readthedocs.io/installation.html
[10]: https://chrome.google.com/webstore/category/extensions
[11]: https://en.wikipedia.org/wiki/XPath
[12]: https://en.wikipedia.org/wiki/CSS
[13]: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction