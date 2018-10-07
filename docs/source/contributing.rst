============
Contributing
============
This repo uses the `Git Branching Model <https://nvie.com/posts/a-successful-git-branching-model/>`_. The head of master branch should always be production ready. The head of the develop branch should contain the latest delivered development changes for the next release. Features should be created in feature branches that branch from the develop branch.

Create virtualenv (recommended, but not required). Then get the repo::

    $ git clone https://github.com/brettelliot/ecal.git
    $ pip install -e .

Run the tests::

    $ python setup.py test

Creating a new feature branch from the ``develop`` branch::

    $ git checkout -b be-sqlite-cache develop

Committing code to the new ``be-sqlite-cache`` branch::

    $ git add .
    $ git commit -am 'Commit message'
    $ git push --set-upstream origin be-sqlite-cache

Committing code to an existing ``be-sqlite-cache`` branch::

    $ git add .
    $ git commit -am 'Commit message'
    $ git push

Creating the documentation for the first time (from the docs/ directory)::

    $ sphinx-quickstart

Building the documentation (again, from the docs/ directory)::

    $ sphinx-apidoc -f -o source/ ../ecal/
    $ make html

Incorporating a finished feature onto ``develop``::

    $ git checkout develop
    $ git merge --no-ff be-sqlite-cache
    $ git push origin develop
    $ git branch -d be-sqlite-cache
    $ git push origin --delete be-sqlite-cache

Create a release branch from ``develop``, and merge it into ``master``::

    $ git checkout -b release-1.0.0 develop
    $ git checkout master
    $ git merge --no-ff release-1.0.0
    $ git push
    $ git tag -a 1.0.0 -m "release 1.0.0"
    $ git push origin 1.0.0

Merge the release branch changes back into ``develop`` so it's up to date::

    $ git checkout develop
    $ git merge --no-ff release-1.0.0
    $ git branch -d release-1.0.0
    $ git push origin --delete release-1.0.0

Generating distribution archives::

    $ git checkout master
    $ python setup.py check --strict --metadata
    $ rm -rf dist/
    $ python3 setup.py sdist bdist_wheel

Upload to test.pypi.org::

    $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

To test the package from test.pypi.org, create a new virtual env, install the package, then run python and import it::

    $ rm -rf ~/.virtualenvs/ecal_test_pypi
    $ mkvirtualenv ecal_test_pypi
    $ python3 -m pip install --no-cache-dir --extra-index-url https://test.pypi.org/simple/ ecal
    $ python
    >>> import ecal
    >>> ecal.name
    'ecal'

Upload the package to the real pypi.org website::

    $ twine upload dist/*

To test the package from pypi.org, create a new virtual env, install the package, then run python and import it::

    $ rm -rf ~/.virtualenvs/ecal_pypi
    $ mkvirtualenv ecal_pypi
    $ pip install --no-cache-dir ecal
    $ python
    >>> import ecal
    >>> ecal.name
    'ecal'
