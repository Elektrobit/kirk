.. SPDX-License-Identifier: GPL-2.0-or-later

Releases
========

Releases follow semantic versioning ``Major.Minor.Patch`` and are scheduled
when there are sufficient new features or important bug fixes.

Release procedure
-----------------

Pre-release
~~~~~~~~~~~

1. Bump ``libkirk.__version__`` in ``libkirk/__init__.py`` to the new version.
2. Commit the version bump, push, and verify that all CI workflows pass.
3. Manually run QEMU integration tests:

   .. code-block:: bash

      pytest libkirk/tests/test_qemu.py

Packaging and publishing
~~~~~~~~~~~~~~~~~~~~~~~~

4. Clean previous build artifacts and create the package:

   .. code-block:: bash

      rm -rf dist/
      python3 -m build

5. Upload the package to PyPI:

   .. code-block:: bash

      twine upload dist/kirk-<version>*

6. Tag the release with a signed tag and push:

   .. code-block:: bash

      git tag -s v<version> -m "Version <version>"
      git push origin v<version>

7. Create and publish the release on GitHub with release highlights.

Post-release
~~~~~~~~~~~~

8. Update the documentation changelog and commit the changes:

   .. code-block:: bash

      ./utils/update_changelog.py
      git add doc/changelog.rst
      git commit -s -m "doc: update changelog for v<version>"
      git push origin master

9. Upgrade the kirk version reference inside the `LTP <https://github.com/linux-test-project/ltp>`_ project.
10. Generate and send the release announcement email to the LTP mailing list:

    .. code-block:: bash

       ./utils/generate_release_email.py
