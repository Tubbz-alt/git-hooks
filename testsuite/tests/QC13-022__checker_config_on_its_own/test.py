        # to the refs/meta/config branch. However, the file it points
        # to does not exist in that reference, nor is is added by
        # the commit we're pusing. So this should be rejected.

        p = Run('git push origin meta-config-missing:refs/meta/config'.split())
        expected_out = """\
remote: *** Cannot find style_checker config file: `style.yaml'.
remote: ***
remote: *** Your repository is configured to provide a configuration file to
remote: *** the style_checker; however, this configuration file (style.yaml)
remote: *** cannot be found in commit adcecf2c1d321ff7e35dae44c41f46b885925bd0.
remote: ***
remote: *** Perhaps you haven't added this configuration file to this branch
remote: *** yet?
remote: error: hook declined to update refs/meta/config
To ../bare/repo.git
 ! [remote rejected] meta-config-missing -> refs/meta/config (hook declined)
error: failed to push some refs to '../bare/repo.git'
"""

        self.assertNotEqual(p.status, 0, p.image)
        self.assertRunOutputEqual(p, expected_out)

        # Do the same as above, but this time with a commit which
        # provides both the config file at the same time it adds
        # the style-checker-config-file option.  This time, the update
        # should be accepted.

remote: *** cvs_check: `--config' `style.yaml' `repo' < `project.config' `style.yaml'
remote: *** # A YaML file (with nothing in it)
remote: ***
remote: Bcc: filer@example.com
remote: X-Git-Oldrev: e7b927eb2e249cf2aed16c3da9c6ebcaa0f768b9
remote: X-Git-Newrev: 0cfbca7db5e102b2cbb6deeec0d951ee258b40e1
remote: commit 0cfbca7db5e102b2cbb6deeec0d951ee258b40e1
remote:  style.yaml     | 1 +
remote:  2 files changed, 2 insertions(+)
remote: index 05e3cbe..f24e088 100644
remote: @@ -2,3 +2,4 @@
remote:  	filer-email = filer@example.com
remote: diff --git a/style.yaml b/style.yaml
remote: new file mode 100644
remote: index 0000000..b3fcae2
remote: --- /dev/null
remote: +++ b/style.yaml
remote: @@ -0,0 +1 @@
remote: +# A YaML file (with nothing in it)
   e7b927e..0cfbca7  meta-config -> refs/meta/config
remote: *** Cannot find style_checker config file: `style.yaml'.
remote: *** the style_checker; however, this configuration file (style.yaml)
remote: *** cannot be found in commit 555923ece17519f0afeed78625afc6ab7e64e592.
remote: Bcc: filer@example.com
remote: Bcc: filer@example.com
remote: Bcc: filer@example.com
remote: Bcc: filer@example.com