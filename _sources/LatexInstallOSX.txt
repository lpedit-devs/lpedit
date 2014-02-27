.. reproducible-research Version Control file, created by ARichards

=======================
LaTeX Installation OS X
=======================

Basic installation
__________________

On OS X in order to install LaTeX there are a couple of options.

MacTeX
^^^^^^

    1. Go to `http://www.tug.org/mactex <http://www.tug.org/mactex>`_
    2. Download the latest MacTex package
    3. If it does not start automatically go to Downloads and open the zip
    4. Run the installer (MacTeX-20**.mpkg)

Mac Ports
^^^^^^^^^

    .. code-block:: none

        ~$ sudo port -v install texlive
        ~$ sudo port -v install texlive-math-extra texlive-latex-extra texlive-bibtex-extra

distribution which comes as a bundle called `MiKTeX
<http://miktex.org>`_.  Under the list of MiKTeX releases go to the
download link for the most recent version.  From that page download
the installer.


Resources
_________

  * `Guide from Macrumors <http://guides.macrumors.com/Installing_LaTeX_on_a_Mac>`_ 
  * `MacTex <http://www.tug.org/mactex>`_
  * `Install lpEdit from source (OS X)
    <http://bitbucket.org/ajrichards/reproducible-research/wiki/os_x_mountain_lion_from_source>`_
