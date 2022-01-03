**Open Source Contributor's guide**

# **Contributors**
Contributors are individuals willing to contribute to an open source project in GitHub in order to learn, teach, and gain experience. Contributors have the ability to:

Create issues

Create new feature requests

Contribute to fixing issues via pull request

Helping triage issues - although changing labels will be restricted, contributors can help identify duplicates and provide upvotes on issues Contributors must fork the repository and create a branch from main, which will contain code changes related to an issue.

# Branching
Repositories will use a scaled trunk branching strategy (short-lived branches) in combination with feature flags to allow frequent changes to the main branch without breaking the build with partial features.

Short-lived branches will be created for parts of a feature or a feature in its entirety (depending on the size of the feature)

The main branch is always releasable, meaning code being pushed to main is fully tested and reviewed to ensure it works and does not create and regressions

Maintainers can create branches directly off the main branch Contributors must fork the repository and create a branch from main





# Branch Naming


|**Branch Type**|**Example**|**Comment**|
| :- | :- | :- |
|main|main||
|Release|release-1.0|hotfix: release-1.1 patch: release-1.0.1|
|Feature|feature-9-olp-support|"9" referring to GitHub issue ID|
|Bug Fix|bugfix-110-remove-docker-compose|"110" referring to GitHub issue ID|
## **Release Branches**
A release branch is a branch created from main that will be solely used to release a new version. A release branch follows these rules: Maintainers are the only ones that can create a release branch

The branch is named according to the branch naming conventions listed above

No changes are made directly on the feature branch. If there any critical defects, those commits can be cherry-picked from the main branch into the release branch

Only critical bug fixes will be merged into this branch Release branches are never deleted

Release branches are created 10 days prior to a release to allow time for longevity testing to be executed

A release can contain features and/or partial features from future release that will be labelled as "experimental features". Features designated for future releases are continually be worked on while also being merged into the main branch. These features will be optionally enabled during deployment using feature flags, if the user chooses to use them. This gives users early expose to features so they can use and test them providing valuable feedback.
##
## **Bug Fix Branches**
A bug fix branch is a branch which is created for the purpose of fixing a GitHub bug issue.

Maintainers can create bug fix branches from the main branch

Contributors can create bug fix branches after they have forked the repository

Bug fix branches are merged directly into the main branch once a pull request has been approved Bug fix branches are deleted once they have been merged to the main branch

## **Feature Branches**
A feature branch is created for code changes related to a feature. This can either be dedicated for a full feature, if it is small, or for part of a feature. The goal is deliver feature value incrementally into the main branch so short lived branches delivering partial working feature functionality is the preference.

Maintainers can create feature branches from the main branch

Feature branches are merged directly into main once a pull request has been reviewed Feature branches are deleted once they have been merged to the main branch

## **The Main Branch**
The main branch is where bug fixes and continuous feature value is being delivered. The main branch is ALWAYS releasable, meaning code being pushed to the main branch is fully tested and reviewed to ensure it works and does not create and regressions. When changes are merged into the main branch, a new "main" image will be created and pushed to Docker Hub. This provides continuous access to the latest and greatest features and fixes being worked on so users can use them and provide valuable feedback.

If a feature or partial feature branch is being merged to main, it must contain documentation updates with any new feature flags that have added or other feature flags that have been changed. The providers the user with information on how to enable/disable an experimental feature.




|**Feature Stage**|**Description**|
| :- | :- |
|Alpha|<p></p><p>Disabled by default</p><p>May contain only parts of a feature</p><p>Potentially buggy where enabling the feature may expose bugs Support for the feature may be dropped at any time without notice</p>|
|Beta|<p></p><p>Enabled by default</p><p>The entire feature has been implemented</p><p>The feature is well tested where enabling the feature is considered safe Support for the feature will not be dropped</p>|
|GA|<p></p><p>The feature is always enabled and it cannot be disabled via a feature flag The feature flag has been removed</p><p>Considered stable and will appear in many subsequent versions</p>|
|Deprecated|<p></p><p>Indicates the feature will be deprecated as of a certain version</p><p>When the specific version where it is to be deprecated is released, the feature is disabled and cannot be enabled</p>|

# Example Scenarios
### **New Partial Feature Branch Merged to Main**
Lets consider a case where we are working on a partial feature branch for new feature after 1.0.0 has been released.

The branch contains a fully functional and tested part of the feature that is enabled/disabled by a new feature flag The branch contains an update to the feature flag documentation that has an entry for the feature flag

The feature flag is initially set with the Alpha stage

The first branch merged to the main branch for a particular feature must also contain a change to the feature flags document with the following set of information. In the example below we see a new feature flag in alpha stage that is disabled by default. The "Since" value represents the version that the feature (flag) was originally released in. If the feature (flag) has not been released yet, but is available in the main branch, we can use something like "N

/A" as a value.


|**Feature**|**Default**|**Stage**|**Since**|**Until**|
| :-: | :- | :- | :- | :- |
|new-feature|false|Alpha|N/A||

### **New Release with Partial Feature Destined for Future Release**
Lets consider a case where a release branch is created for a 1.1.0 release. Given the previous example, the release branch will contain the partially developed "new-feature" which is disabled by default. In this case, the feature flag document would be updated to reflect the correct version that "new- feature" became available. If we know the release plan for "new-feature" going forward, we can also provide those details so users are aware. The example below illustrates the release plan for "new-feature" moving from Alpha to GA.


|**Feature**|**Default**|**Stage**|**Since**|**Until**|
| :-: | :- | :- | :- | :- |
|new-feature|false|Alpha|1.1.0|1.1.0|
|new-feature|true|Beta|1.2.0|1.3.0|
|new-feature|true|GA|1.4.0||

When a feature (flag) reaches the GA stage, all entries of the feature flag in the document must be removed. The feature becomes baked into the product at that point and is always enabled.

### **Deprecating a Feature (Flag)**
Lets consider a case where a feature (flag) currently in the Beta stage needs to be deprecated. We would announce that as part of the feature flag documentation. Given that the current release is 1.2.0 and "new-feature" is enabled by default, we want to indicate that "new-feature" will become deprecated in version 1.4.0. The follow examples shows how this is done.


|**Feature**|**Default**|**Stage**|**Since**|**Until**|
| :- | :- | :- | :- | :- |


|new-feature|true|Beta|1.2.0|1.3.0|
| :- | :- | :- | :- | :- |
|new-feature||Deprecated|1.4.0||

This tells the user that the future release 1.4.0 will no longer contain "new-feature".


# **Pull Requests**
Once development on a branch is complete, a pull request is created in accordance with the contributing guide found in the appropriate GitHub repository. A pull request must always link to at least one GitHub issue. If that is not the case, create a GitHub issue and link it.

To increase the chance of having your pull request accepted, make sure your pull request follows these guidelines:

Title and description matches the implementation.

Commits within the pull request follow the formatting guidelines provided in the contributing guide

The pull request can close but may not always close a linked issue - partial feature request pull requests should not close a GitHub feature issue The pull request contains necessary tests that verify the intended behavior

Your branch must be up to date with the main branch before merging If the pull request fixes a bug:

The pull request description must include Fixes #<issue number>.

To avoid regressions, the pull request should include tests that replicate the fixed bug.

When a pull request is merged, all commits are squashed into a single one. It is encouraged to write informative commit messages, as they becomes a part of the Git commit body.

The following pull request template is currently being used and should be used for other open source projects 


## **GitHub Actions**
The following GitHub Actions are used to enforce quality gates when a pull request is created or when any commit is made to the pull request. These GitHub Actions enforce our minimum code quality requirements for any code that gets checked into. If any of the checks fail, it is expected that the contributor will look into the check log, understand the problem and resolve the issue. The maintainer is also responsible for reaching out to contributors when failed checks are noticed in order to help resolve them.

### GitHub Repositories
The following GitHub actions are being used to enforce quality gates on GitHub repositories. No branch can be merged unless the following checks pass.


|**GitHub Action**|**Description**|
| :- | :- |
|Ansible Sanity tests|Inspects Ansible Sanity|
|[Malware](https://github.com/dell/common-github-actions/tree/main/malware-scanner) [Scanner](https://github.com/dell/common-github-actions/tree/main/malware-scanner)|Inspects source code for malwares|
|[Code](https://github.com/dell/common-github-actions/tree/main/code-sanitizer) [Sanitization](https://github.com/dell/common-github-actions/tree/main/code-sanitizer)|Analyzes source code for forbidden words and text. Forbidden words include such as non-inclusive language|
|[Test Coverage](https://github.com/dell/common-github-actions/tree/main/go-code-tester)|Runs ansible unit tests and check that code coverage per package meets a configured threshold (90%). Flags error if given pull request do not meet the test coverage threshold and blocks the merge of the pull request.|
|E2E tests|Captures the results of the maintainer triggered E2E tests executed against the pull request. The check will fail if the tests do not pass.|




**Ansible Code of Conduct:**

Every community can be strengthened by a diverse variety of viewpoints, insights, opinions, skillsets, and skill levels. However, with diversity comes the potential for disagreement and miscommunication. The purpose of this Code of Conduct is to ensure that disagreements and differences of opinion are conducted respectfully and on their own merits, without personal attacks or other behavior that might create an unsafe or unwelcoming environment.
For more details [Ansible Code of conduct](https://docs.ansible.com/ansible/latest/community/code\_of\_conduct.html) can be reffered.
