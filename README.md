# ARIADNE

![ARIADNE Logo](https://github.com/IGOR-bioDGPs/ARIADNE/blob/master/testbook/ARIADNE_Logo.png)


*The freely available, curated and dynamically “living” tool ARIADNE spans the whole research process and is translated to a dynamic interface for easier use and search for the individual resources.*

Included in this repo, is the network backend of *ARIADNE-resource* and the Jupyter-notebook instance of the living book.

## Authors of ARIADNE:
- Helena Hartmann [@helenahartmann](https://www.github.com/helenahartmann)
- Çağatay Gürsoy [@caggursoy](https://www.github.com/caggursoy)
- Marie Mückstein [@mamuerie](https://www.github.com/mamuerie)
- Matthias F. J. Sperl [@matthias-sperl](https://www.github.com/matthias-sperl)
- Gordon B. Feld [@flashgordon1983](https://www.github.com/flashgordon1983)
- Alina Koppold [@alkoppold](https://www.github.com/alkoppold)
- Alex Kastrinogiannis [@alkastrinogiannis](https://www.github.com/alkastrinogiannis)
- Alex Lischke
- Suzanne Vogel [@SusanneVo](https://www.github.com/SusanneVo)
- Yu-Fang Yang [@ufangyang](https://www.github.com/ufangyang)

## License

[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/license/mit/)

## Usage / Reproducing
If you want to reproduce and host the book by yourself.

This cookiecutter creates a simple boilerplate for a Jupyter Book.

### Building the book

If you'd like to develop and/or build the TestBook book, you should:

1. Clone this repository
2. Run `pip install -r requirements.txt` (it is recommended you do this within a virtual environment)
3. (Optional) Edit the books source files located in the `testbook/` directory
4. Run `jupyter-book clean testbook/` to remove any existing builds
5. Run `jupyter-book build testbook/`

A fully-rendered HTML version of the book will be built in `testbook/_build/html/`.

### Hosting the book

Please see the [Jupyter Book documentation](https://jupyterbook.org/publish/web.html) to discover options for deploying a book online using services such as GitHub, GitLab, or Netlify.

For GitHub and GitLab deployment specifically, the [cookiecutter-jupyter-book](https://github.com/executablebooks/cookiecutter-jupyter-book) includes templates for, and information about, optional continuous integration (CI) workflow files to help easily and automatically deploy books online with GitHub or GitLab. For example, if you chose `github` for the `include_ci` cookiecutter option, your book template was created with a GitHub actions workflow file that, once pushed to GitHub, automatically renders and pushes your book to the `gh-pages` branch of your repo and hosts it on GitHub Pages when a push or pull request is made to the main branch.

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/mamuerie/testbook/graphs/contributors).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
