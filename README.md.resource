# [Application name] 

Provide a description of application

## Future plans

List a roadmap or future plans for the repo work.

- [ ] 

## Repo checklist

Repo checklist:

* [ ] Run foundation.py with the destination project folder as a command line argument.
    * This will copy all important files to your project, renaming at least one for your repo.
    * Don't worry.  It won't overwrite existing files with the same names there.
* [ ] Add your favorite [git aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases) to .git/config.
    * Don't have favorites?  Try out the aliases from [Ned Batchelder's](https://github.com/nedbat) [dot repo](https://github.com/nedbat/dot), extracted into [this file](https://github.com/ErikPohl444/resources/blob/main/git_aliases.txt). 
* [ ] Complete a starter [.gitignore](https://git-scm.com/docs/gitignore#:~:text=A%20gitignore%20file%20specifies%20intentionally,gitignore%20file%20specifies%20a%20pattern.)
    * [ ] Keep the current starter .gitignore and add to it.
    * [ ] OR delete the starter I'm providing and either create one via template in GitHub by typing in the name .gitignore in the file name after choosing to create a file
    * [ ] OR create one [using this tool.](https://www.toptal.com/developers/gitignore/)
* [ ] Populate AUTHORS.md with the authors of the work in the repo. 
    * Foundation will populate the first commit author if it can find a git repo and at least one commit.
    * Refer to [these instructions](https://opensource.google/documentation/reference/releasing/authors) for other ways to create and maintain this reference. 
* [ ] Add a [sponsor button](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository), if you intend to solicit funding for the work in your repo.
* [ ] Add a [social media image](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview), if you'd like your repo to have a specific image when referenced in social media.
* [ ] Add [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) to your repo to help the repo be searchable and comprehensible.
* [ ] Enter any acknowledgements into ACKNOWLEDGEMENTS.md to acknowledge inspirations, code you've used, and people who helped you in your journey to this repo.
* [ ] Accept a license to define how people can legally use, share, etc. your repo:
    * The default license provided by this process is the [MIT License](https://en.wikipedia.org/wiki/MIT_License).  **This is automated in Foundation, but it needs to see a git repo with a commit to change this.**
    * If you don't want that one, delete it from your repo and use GitHub to [select one easily](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
* [ ] Accept a code of conduct to indicate how members of the community around your repo should interact:
    * Delete the current CODE_OF_CONDUCT.md if you don't want the recommended code of conduct for small projects, as currently available from GitHub.
    * If you prefer another code of conduct, you can make your own or use GitHub's [easy instructions](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project).
* [ ] Accept a CODEOWNERS file to enforce who the code owners are.
    * Blank is fine to start out with.
    * Use [these instruction](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) from Github if you'd like to develop CODEOWNERS more.
* [ ] Modify CONTRIBUTING.md, if you want [instructions for contributing to your repo](https://contributing.md/how-to-build-contributing-md/).
    * More detail can be found [here](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors).
* [ ] Add a [CITATIONS.cff file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files) if you'd like to specify how others cite your work.
* [ ] Update README.md to pull all of the above together, along with other items important to understanding your repo.
* [ ] If you need a Makefile for builds, [make one](https://makefiletutorial.com/)
* [ ] If you need a Manifest, [manifest one](https://docs.github.com/en/apps/sharing-github-apps/registering-a-github-app-from-a-manifest).
* [ ] Consider releasing a [release plan](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
* [ ] Do you need/want a config file in json, yaml, or .ini?
* [ ] Incorporate a [CI/CD pipeline](https://github.com/resources/articles/devops/ci-cd):
    * [ ] Create GitHub Actions [for your repo](https://github.com/features/actions).
        * Other tools like [Travis](https://www.travis-ci.com/) and [Jenkins](https://www.jenkins.io/solutions/pipeline/) and [Azure DevOps Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/what-is-azure-pipelines?view=azure-devops) are available.    
    * [ ] Create [Git hooks](https://git-scm.com/book/ms/v2/Customizing-Git-Git-Hooks), if you'd like.
        * I recommend [pre-commit](https://pre-commit.com/).
        * [Husky](https://typicode.github.io/husky/) is also available.
    * [ ] Confirm the following items are captured using Sonarqube or other static analysis tools and that you have a minimum tolerance for each metric which is tested against:
        * Code Complexity:
            * Cognitive complexity
            * Cyclomatic code complexity
        * Duplications
        * Maintainability
        * Issues metrics
        * Reliability
        * Size
        * Test Coverage
        * Passing and failing test metrics
        * Security
        * Linting  
* [ ] Containerize the code for distribtion, if you'd like.
    * Add, for example, a Dockerfile or compose.yaml, if using Docker.   
* [ ] This is a parent checkbox for all Python-specific items:
  * [ ] Populate [requirements.txt](https://pip.pypa.io/en/stable/reference/requirements-file-format/) and keep it populated through pip freeze > requirements.txt
  * [ ] Confirm tests are in /tests.
      * [ ] Leverage [pytest](https://docs.pytest.org/en/stable/) or another fully-modernized test framework for  testing.
      * [ ] Leverage [coverage.py](https://coverage.readthedocs.io/en/7.6.10/) or a similar tool for code coverage analysis.
  * [ ] Confirm source code is in /src
      * [ ] For a linting tool in your CI/CD pipeline or for integration with your IDE, consider ruff, pylint, flake8.
      * [ ] For a type-checking tool in your CI/CD pipeline, consider mypy.
      * [ ] There is a very primitive [setup_logging.py](https://github.com/ErikPohl444/resources/blob/main/src/setup_logging.py) file included here to import for [logging purposes](https://docs.python.org/3/library/logging.html).  Delete it, make your own, etc.  
  * [ ] Confirm docs are in /docs
  * [ ] If you'd like eventually to make a Python package, there's a starter [pyproject.toml](https://packaging.python.org/en/latest/tutorials/packaging-projects/#configuring-metadata) you can edit, or you can delete this file.
    * Because this resources utility is Python build tool agnostic, I am not including a setup.py for setuptools, or any other files or configurations specific to Hatchling, Poetry, setuptools, Flit, or PDM.
    * More in-depth pyproject.toml information [here](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).
        
## Important disclaimer

If any disclaimer exists, add it here.

## Getting Started

Provide non-setup instructions for getting started using the work in the repo.

## Prerequisites

This section has overlap with minimum system requirements, requirements.txt, and technologies.
I consider this anything which needs to be on your machine or available to you before installing and using the work in the repo.

## Installing

Provide installation steps here.

## Running the tests

Provide instructions on running the tests here.

## Technologies used

List the technologies used here.

e.g.
* Written in Chicken 2.0

## Minimum system requirements

List the minimum system requirements for the application to run.

e.g.
* Must be run on VALIS.

## Contributing

I invite contributions.  See the [Contribution Guidelines](CONTRIBUTING.md) for any guidelines.

## Authors

See the [Authors doc.](AUTHORS.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Thanks to everyone who has motivated me to learn more.
* These folks were key to this particular effort: [ACKNOWLEDGEMENTS](ACKNOWLEDGEMENTS.md)
