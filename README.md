Storyboard issue closer
=======================

This is a simple script to close issues on a storyboard project as invalid.
It's primarily meant for declaring-bug-bankruptcy style migrations to a new
bugtracker.

Usage
-----
- Create a venv, install requests and click, then activate it
- `python sb-issue-closer.py --base-url=https://storyboard.openstack.org/api/v1 --project-id=1234 --token=mytoken --message="We moved to a different bugtracker. Sorry for the inconvenience."`

Troubleshooting
---------------
* "ironic" isn't a valid project_id
  * You need the int project_id. Load up storyboard in your browser with dev tools open and find the API call the frontend makes when you open your project. Get the int from there.
* "mytoken" isn't a valid token
  * Get a token by logging into storyboard, then click on the top right settings button and provision a new Authentication Token. Use that.
* Something else went wrong
  * You can open an issue but I have no special knowledge.
  * Check some docs and fix it yourself! https://docs.openstack.org/infra/storyboard/webapi/v1.html

  License
  -------
  This repo is released under MIT license. 