        Reproduce the situation where the project.config file in
        refs/meta/config does not exist, yet.
        # Push the `meta/config' local branch as the new `refs/meta/config'
        # reference. This should be allowed.
remote: X-Git-Newrev: 7dcb1b7cb71d09ed70b3d64c8ddd993ec1d2d017
remote:  7dcb1b7... Initial config for project
remote: Bcc: filer@example.com
remote: X-Git-Newrev: 7dcb1b7cb71d09ed70b3d64c8ddd993ec1d2d017
remote: commit 7dcb1b7cb71d09ed70b3d64c8ddd993ec1d2d017
remote:  project.config | 4 ++++
remote:  1 file changed, 4 insertions(+)
remote: index 0000000..e565530
remote: @@ -0,0 +1,4 @@
remote: +        filer-email = filer@example.com