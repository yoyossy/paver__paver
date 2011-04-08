"""Convenience functions for working with git.

This module does not include any tasks, only functions.

At this point, these functions do not use any kind of library. They require
the git binary on the path."""

from paver.easy import sh, Bunch, path
import os, re

def _format_path(provided_path):
    if provided_path:
        return provided_path
    else:
        return os.getcwd()

def clone(url, dest_folder):
    sh("git clone %(url)s %(path)s" % dict(url=url, path=dest_folder) )

def pull(destination, remote="origin", branch="master"):
    """Perform a git pull. Destination must be absolute path.
    
    Will raise 
    """
    sh("cd %(destination)s; git pull %(remote)s %(branch)s" % dict(
        destination=destination, remote=remote, branch=branch) )

def branch_list(path="", __override__=None):
    """Returns a Python tuple. The first item in the tuple will be the current
    branch, and the other item will be a list of branches for the repository.
    
    Optional parameter path: the path to the git repo. Else uses os.getcwd()
    """
    
    git_output = None
    
    if __override__ == None:
        git_output = sh(  "cd %(repo_path)s; git branch" % dict(
            repo_path = _format_path(path) )  )
    else:
        git_output = __override__
    
    if git_output == None:
        return ( None, [] ) # should only hit this condition in testing...
    
    current_branch = ""
    branches = []
    found_a_match = False
    regex = re.compile(r"(\*?)\W*(.+)")
    
    for line in git_output.split("\n"):
        match_obj = regex.match(line)
        if match_obj:
            found_a_match = True
            if match_obj.group(1):
                current_branch = match_obj.group(2).strip()
            if match_obj.group(2).strip():
                branches.append( match_obj.group(2).strip() )
        
    if found_a_match == False:
        raise "git branch did not return output expected. Returned %s" % (git_output)
    
    return (current_branch, branches)

def branch_checkout(branch_name, path=""):
    """Checkout a git branch.
    
    Take the branch name to checkout, and optional path parameter
    (the path to the git repo. Else uses os.getcwd())
    """
    
    sh( "cd %(repo_path)s; git checkout %(branch_name)s" % dict(
        repo_path = _format_path(path),
        branch_name=branch_name) )