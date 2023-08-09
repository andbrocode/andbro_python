#!/usr/bin/python
#
# script to delete a project tree of salvus 
#(since overwriting is not a given option)
#

def __del_project(project_name):
    """ 
    delete specified project file structure

    dependencies: 
        - import os 
    
    example: 
        >>> __del_project(project_name)
    """
    from os import popen
    from os.path import isdir
    
    ans = input(f"you intend to delete {project_name} (y/n):")

    if ans is "yes" or ans is "y":
        if isdir(project_name): 
            popen("rm -rf $project_name")
            print(f"deleted: {project_name}")
        else: 
            print(f"{project_name} does not exist!")


# END OF FILE
