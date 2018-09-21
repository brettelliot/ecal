Contributing
============
This repo uses the `Git Branching Model <https://nvie.com/posts/a-successful-git-branching-model/>`_. The head of master branch should always be production ready. The head of the develop branch should contain the latest delivered development changes for the next release. Features should be created in feature branches that branch from the develop branch.

Create virtualenv (recommended, but not required). Then get the repo::

    $ git clone https://github.com/brettelliot/ecal.git
    $ pip install -e .

Run the tests::

    $ python setup.py test

Creating a new feature branch from the ``develop`` branch::

    $ git checkout -b myfeature develop

Committing code to the new ``myfeature`` branch::

    $ git add .
    $ git commit -am 'Commit message'
    $ git push --set-upstream origin myfeature

Committing code to an existing ``myfeature`` branch::

    $ git add .
    $ git commit -am 'Commit message'
    $ git push

Incorporating a finished feature onto ``develop``::

    $ git checkout develop
    $ git merge --no-ff myfeature
    $ git push origin develop
    $ git branch -d myfeature
    $ git push origin --delete myfeature

Create a release branch from ``develop``, and merge it into ``master``::

    $ git checkout -b release-0.0.2 develop
    $ git checkout master
    $ git merge --no-ff release-0.0.2
    $ git push
    $ git tag -a 0.0.2 -m "release 0.0.2"
    $ git push origin 0.0.2

Merge the release branch changes back into ``develop`` so it's up to date::

    $ git checkout develop
    $ git merge --no-ff release-0.0.2
    $ git branch -d release-0.0.2
    $ git push origin --delete release-0.0.2

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
    $ python3 -m pip install --no-cache-dir --extra-index-url https://test.pypi.org/simple/ be-earnings-calendar
    $ python
    >>> import be_earnings_calendar as ecal
    >>> ecal.name
    'be_earnings_calendar'

Upload the package to the real pypi.org website::

    $ twine upload dist/*

To test the package from pypi.org, create a new virtual env, install the package, then run python and import it::

    $ rm -rf ~/.virtualenvs/ecal_pypi
    $ mkvirtualenv ecal_pypi
    $ pip install --no-cache-dir be-earnings-calendar
    $ python
    >>> import be_earnings_calendar as ecal
    >>> ecal.name
    'be_earnings_calendar'