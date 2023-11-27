'''
Error code handling library, please use with caution.
Made with love - noerlol
For luiobot with Love

Do not mix with other projects.
'''

import sys, os
def programquit(return_code: int):
    if not isinstance(return_code, int):
        return;
    sys.exit(return_code)
class Error:
    db_error: str = "An error occurred while trying to access the database. luiobot.errors.Error.db_error";
    permission_error: str = "You do not have enough permissions.";
    permission_error_terminal: str = "You do not have enough permissions. luiobot.errors.Error.permission_error_terminal";
    file_not_found_error: str = "A file was not downloaded properly or is corrupted. luiobot.errors.Error.file_not_found_error";
    config_error: str = "Configuration was not found (config.py not found). luiobot.errors.Error.config_error";
    class fatal_errors:
        def memory_error(self):
            print("Invalid memory, program force exiting.");
            programquit(0);