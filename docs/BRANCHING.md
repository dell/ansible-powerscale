<!--
Copyright (c) 2022 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
-->

# Branching strategy

Ansible modules for Dell PowerScale follows a scaled trunk branching strategy where short-lived branches are created off of the main branch. When coding is complete, the branch is merged back into main after being approved in a pull request code review.

## Branch naming convention

|  Branch Type |  Example                          |  Comment                                  |
|--------------|-----------------------------------|-------------------------------------------|
|  master      |  master                           |                                           |
|  Release     |  release-1.0                      |  hotfix: release-1.1 patch: release-1.0.1 |
|  Feature     |  feature-9-vol-support            |  "9" referring to GitHub issue ID         |
|  Bug Fix     |  bugfix-110-fix-duplicates-issue  |  "110" referring to GitHub issue ID       |


## Steps for working on a release branch

1. Fork the repository.
2. Create a branch off of the master branch. The branch name should follow [branch naming convention](#branch-naming-convention).
3. Make your changes and commit them to your branch.
4. If other code changes have merged into the upstream master branch, perform a rebase of those changes into your branch.
5. Open a [pull request](https://github.com/dell/ansible-powerscale/pulls) between your branch and the upstream master branch.
6. Once your pull request has merged, your branch can be deleted.
