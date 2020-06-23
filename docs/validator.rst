XML Validation CLI
==================

This is a command-line interface for validating any given XML file against a specific XSD Schema.

Usage
-----

After this package has been installed, the validation tool is used by by executing ``xml-validate`` in a terminal with specified options/arguments followingly:

.. code-block:: console

    $ xml-validate <option> <xml-file> <schema-file>

The ``<xml-file>`` and ``<schema-file>`` arguments need to be the correct filenames (including path) of a local XML file and the corresponding XSD file.
The ``<option>`` can be ``--help`` for showing help and ``-v`` or ``--verbose`` for delivering a detailed validation error message.


Below is a terminal demonstration of the usage of this tool, which displays the different outputs the CLI will produce:

.. raw:: html

    <script id="asciicast-ykioH41E9Y38fG404hReQedyc" src="https://asciinema.org/a/ykioH41E9Y38fG404hReQedyc.js" async></script>
