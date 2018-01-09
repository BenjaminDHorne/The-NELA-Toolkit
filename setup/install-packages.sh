#!/usr/bin/env bash

do_sudo=
which sudo &> /dev/null && do_sudo="sudo"

# Note, do not install numpy and scipy using apt-get or you may get an older
# version. Only install them using pip.

# Install the following packages on Ubuntu:
python -mplatform | grep -q Ubuntu
if [ $? -eq 0 ]; then
  $do_sudo apt-get remove python-numpy python-scipy
  $do_sudo apt-get install libblas-dev liblapack-dev gfortran python-pil python-qt4
fi

$do_sudo pip install flask nltk textblob goose-extractor tldextract || exit 1
$do_sudo pip install numpy scipy || exit 1
$do_sudo pip install itsdangerous click idna requests_file feedparser bs4 werkzeug jinja2 vaderSentiment sklearn || exit 1

python -c 'import nltk ; nltk.download("subjectivity")'
python -c 'import nltk ; nltk.download("punkt")'
python -c 'import nltk ; nltk.download("averaged_perceptron_tagger")'
