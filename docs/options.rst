.. _Configuration Options:

Configuration Options
=====================

You can change many options for how this extension works via

.. code-block:: python

  app.config[OPTION_NAME] = new_options

Options:
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{6cm}|p{7cm}|

=================================== =========================================
``INVALID_CONTENT_TYPE_ABORT_CODE`` default is 406
``KEY_MISSING_ABORT_CODE``          default is 400
``INVALID_TYPE_ABORT_CODE``         default is 400
``VALIDATION_FAILURE_ABORT_CODE``   default is 400
``VALIDATION_ERROR_ABORT_CODE``     default is 400
=================================== =========================================