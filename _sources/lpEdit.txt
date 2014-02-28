.. reproducible research tutorial file, created by ARichards

======
lpEdit
======

About lpEdit
============

.. INCLUDE ./images/lpEdit-screenshot1.png, ./images/lpEdit-screenshot2.png

lpEdit is a software editor created for biologists and other
researchers in order to help document analyses---the aim being to
ultimately make analyses more reproducible.  From simple statistical tests to
complicated pipelines involving many gigabytes of data, this tool offers a
unified way to document analyses in a transparent way. 

There are many tools available that encompass the ideas of
:doc:`Literate Programming <LiterateProgramming>`.  However, the
challenge of getting the majority of researchers to adopt these
practices still remains.  This editor offers a simple means to mix
code and prose in order to produce reports, presentations and
webpages.

Here are some screenshots from lpEdit.

.. figure:: lpEdit-screenshot1.png
   :scale: 20%
   :align: center
   :alt: lpEdit screenshot 1
   :figclass: align-center



.. figure:: lpEdit-screenshot2.png
   :scale: 20%
   :align: center
   :alt: lpEdit screenshot 2
   :figclass: align-center

Installation
____________

To download lpEdit visit the `application page
<https://bitbucket.org/ajrichards/reproducible-research/wiki/Home>`_.

or for those who wish to install from source the following works on Debian-based distros.

.. code-block:: none

    ~$  sudo apt-get install python-qscintilla2 python-qt4 python-numpy python-matplotlib python-sphinx
    ~$  sudo apt-get install r-base
    ~$  hg clone https://bitbucket.org/ajrichards/reproducible-research
    ~$  cd reproducible-research
    ~$  sudo python setup.py install
    ~$  python lpEdit.py
