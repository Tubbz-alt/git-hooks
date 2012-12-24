"""Handling of Git Notes updates."""

from git import git, is_null_rev, is_valid_commit
from updates import AbstractUpdate
from updates.emails import Email
from updates.notes import GitNotes
from utils import indent, InvalidUpdate

NOTES_COMMIT_EMAIL_BODY_TEMPLATE = """\
The annotations of the following commit have been updated.

%(annotated_rev_info)s

Diff:

%(diff)s
"""

class NotesUpdate(AbstractUpdate):
    """Update object for Git Notes creation or update.

    The difference between Notes creation and Notes update is very
    small, so this class has been implemented in a way to support
    both (in other words, self.old_rev may be null).
    """
    def self_sanity_check(self):
        """See AbstractUpdate.self_sanity_check."""
        assert self.ref_name == 'refs/notes/commits'

    def validate_ref_update(self):
        """See AbstractUpdate.validate_ref_update."""
        # Only fast-forward changes are allowed.
        self.__ensure_fast_forward()

        # Also iterate over all new notes, and verify that
        # the associated commit is available. We need these
        # associated commits in order to create the emails
        # to be sent for those notes.
        for notes_commit in self.added_commits:
            notes = GitNotes(notes_commit.rev)
            if not is_valid_commit(notes.annotated_rev):
                error_message = [
                    'The commit associated to the following notes update',
                    'cannot be found. Please push your branch commits first',
                    'and then push your notes commits.',
                    '',
                    'Notes commit:     %s' % notes.rev,
                    'Annotated commit: %s' % notes.annotated_rev,
                    '',
                    'Notes contents:',
                    ] + \
                    notes.contents.splitlines()
                raise InvalidUpdate(*error_message)

    def pre_commit_checks(self):
        """See AbstractUpdate.pre_commit_checks."""
        # No pre-commit checks needed for Git Notes.
        pass

    def get_update_email_contents(self, email_info):
        """See AbstractUpdate.get_update_email_contents."""
        # No update email needed for notes (this is always
        # a fast-forward commit)...
        return  None

    def email_commit(self, email_info, commit):
        """See AbstractUpdate.email_commit."""
        notes = GitNotes(commit.rev)

        # Get a description of the annotated commit (a la "git show"),
        # except that we do not want the diff.
        #
        # Also, we have to handle the notes manually, as the commands
        # get the notes from the HEAD of the notes/commits branch,
        # whereas what we needs is the contents at the commit.rev.
        # This makes a difference when a single push updates the notes
        # of the same commit multiple times.
        annotated_rev_info = git.log(notes.annotated_rev, no_notes=True,
                                     max_count="1")
        if notes.contents is not None:
            annotated_rev_info += '\n\nNotes:\n%s' % indent(notes.contents,
                                                            ' ' * 4)

        diff = git.show(commit.rev, pretty="format:", p=True)

        subject = '[%s] notes update for %s' % (email_info.project_name,
                                                notes.annotated_rev)

        body = NOTES_COMMIT_EMAIL_BODY_TEMPLATE % {
            'annotated_rev_info' : annotated_rev_info,
            'diff' : diff,
            }

        email = Email(email_info, subject, body, self.ref_name,
                      commit.base_rev, commit.rev)
        email.send()

    def __ensure_fast_forward(self):
        """Raise InvalidUpdate if the update is not a fast-forward update.
        """
        if is_null_rev(self.old_rev):
            # Git Notes creation, and thus necessarily a fast-forward.
            return

        # Non-fast-foward updates are characterized by the fact that
        # there is at least one commit that is accessible from the old
        # revision which would no longer be accessible from the new
        # revision.
        if git.rev_list("%s..%s" % (self.new_rev, self.old_rev)) == "":
            return

        raise InvalidUpdate(
            'Your Git Notes are not up to date.',
            '',
            'Please update your Git Notes and push again.')
