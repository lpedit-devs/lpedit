.. reproducible research file, created by ARichards

=====================
Reproducible Research
=====================

Our approach to reproducible research consists of three main components:

  1. :ref:`data_sharing` (repositories)
  2. :ref:`audit_trail`  (version control systems)
  3. :ref:`documentation` (literate programming)
   
The idea of reproduciblity is very simple and aligns well with the
principles of the scientific paradigm.  For each experiment or study,
these guidelines stand to benefit all researchers whether in the
laboratory or as part of an analysis. following these guidelines.
Although, laboratory experiments may be difficult to reproduce and the
list of reasons may be numerous---there are very few, if any, reasons
why a data analysis should not be reproducible.

There are several plausible reasons why the vast majority of scientific
studies do not **share data**, leave and **audit trail** and
**document** their work.

  1. Because it is not the common practice.
  2. There is no established on *one size fits all* approach.
  3. There is a tendency to hold on to the data even after publication.
  4. The learning curve for implementing these steps can be daunting.

Our aim in this web resource is to promote the three mentioned steps
as *best practices* so as to provide a generalizable approach to
reproducible research.  At the same time, this resource along with the
literate programming editor :doc:`lpEdit` providing resources to
reduce the difficulty of implementing these principles.

.. _data_sharing:

Data Sharing
-------------

A best practice for data sharing is through the use of repositories
and supplemental materials to journals.  It is also important to use
formats and include metadata that are generally accepted by the
practitioners of a given field of study.

.. digraph:: foo1

   "Data Sharing" -> "Repositories" [ label = "  " ];


Resources
^^^^^^^^^

  * :doc:`DataSharing`


.. _audit_trail:

Audit Trail
---------------

Audit trails are among the easiest aspect of reproducible research to
implement---via version control systems.

.. digraph:: foo2

   "Audit Trail" -> "Version Control"[ label = "  "];

Resources
^^^^^^^^^

  * :doc:`AuditTrail`

.. _documentation:

Documentation
-------------------------

Documentation is the focus of this resource and numerous tools are
already available for researchers.

.. digraph:: foo3

   "Documentation" -> "Literate Programming"[ label = "  "];

Resources
^^^^^^^^^

.. toctree::
   :maxdepth: 1

   DataSharing
   AuditTrail
   Documentation

External Resources
^^^^^^^^^^^^^^^^^^

There are of course other aspects to reproducible research, like the
usage of appropriate statistical tests.  The following resources are
for those who wish to learn more about several statistical aspects of
reproducible analyses.

  * `Seminar by Jim Berger <http://www.amstat.org/sections/sbss/webinarfiles/berger-webinar10-2-2012.pdf>`_
  * `Article by John P. A. Ioannidis <http://aje.oxfordjournals.org/content/168/4/374>`_
  * `Bayesian alternative to Significance Tests <http://statprob.com/encyclopedia/significancetestcontroversyandthebayesianalternative.html>`_

New and articles in Reproducible Research
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * `Nature news article by Jonathan F. Russell <http://www.nature.com/news/if-a-job-is-worth-doing-it-is-worth-doing-twice-1.12727>`_