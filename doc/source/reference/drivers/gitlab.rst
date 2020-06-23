:title: GitLab Driver

.. _gitlab_driver:

GitLab
======

The GitLab driver supports sources, triggers, and reporters. It can
interact with the public GitLab.com service as well as site-local
installations of GitLab.

.. note:: The driver is not features complete compared to the other
          drivers provided with Zuul.

Configure GitLab
----------------

Zuul needs to interact with projects by:

- receiving events via web-hooks
- performing actions via the API

The Zuul user's API token configured in zuul.conf must have the
following ACL rights: "api". The API token must be created in user Settings,
Access tokens.

Each project to be integrated with Zuul needs in "Settings/Webhooks":

- "URL" set to
  ``http://<zuul-web>/zuul/api/connection/<conn-name>/payload``
- "Merge request events" set to "on"
- "Comments" set to "on"
- Define a "Secret Token"

Connection Configuration
------------------------

The supported options in ``zuul.conf`` connections are:

.. attr:: <gitlab connection>

   .. attr:: driver
      :required:

      .. value:: gitlab

         The connection must set ``driver=gitlab`` for GitLab connections.

   .. attr:: api_token

      The user's API token.

   .. attr:: webhook_token

      The project's webhook secret token.

   .. attr:: server
      :default: gitlab.com

      Hostname of the GitLab server.

   .. attr:: canonical_hostname

      The canonical hostname associated with the git repos on the
      GitLab server.  Defaults to the value of :attr:`<gitlab
      connection>.server`.  This is used to identify projects from
      this connection by name and in preparing repos on the filesystem
      for use by jobs.  Note that Zuul will still only communicate
      with the GitLab server identified by **server**; this option is
      useful if users customarily use a different hostname to clone or
      pull git repos so that when Zuul places them in the job's
      working directory, they appear under this directory name.

   .. attr:: baseurl
      :default: https://{server}

      Path to the GitLab web and API interface.

   .. attr:: cloneurl
      :default: {baseurl}

      Path to the GitLab Git repositories. Used to clone.


Trigger Configuration
---------------------

GitLab webhook events can be configured as triggers.

A connection name with the GitLab driver can take multiple events with
the following options.

.. attr:: pipeline.trigger.<gitlab source>

   The dictionary passed to the GitLab pipeline ``trigger`` attribute
   supports the following attributes:

   .. attr:: event
      :required:

      The event from GitLab. Supported events are:

      .. value:: gl_merge_request

   .. attr:: action

      A :value:`pipeline.trigger.<gitlab source>.event.gl_merge_request`
      event will have associated action(s) to trigger from. The
      supported actions are:

      .. value:: opened

         Merge request opened.

      .. value:: changed

         Merge request synchronized.

      .. value:: comment

         Comment added to merge request.

   .. attr:: comment

      This is only used for ``gl_merge_request`` and ``comment`` actions.  It
      accepts a list of regexes that are searched for in the comment
      string. If any of these regexes matches a portion of the comment
      string the trigger is matched.  ``comment: retrigger`` will
      match when comments containing 'retrigger' somewhere in the
      comment text are added to a merge request.

Reporter Configuration
----------------------
Zuul reports back to GitLab via the API. Available reports include a Merge Request
comment containing the build results. Status name, description, and context
is taken from the pipeline.

.. attr:: pipeline.<reporter>.<gitlab source>

   To report to GitLab, the dictionaries passed to any of the pipeline
   :ref:`reporter<reporters>` attributes support the following
   attributes:

   .. attr:: comment
      :default: true

      Boolean value that determines if the reporter should add a
      comment to the pipeline status to the GitLab Merge Request.


Requirements Configuration
--------------------------

As described in :attr:`pipeline.require` pipelines may specify that items meet
certain conditions in order to be enqueued into the pipeline.  These conditions
vary according to the source of the project in question.

This driver does not support requirements.


Reference pipelines configuration
---------------------------------

Here is an example of standard pipelines you may want to define:

.. literalinclude:: /examples/pipelines/gitlab-reference-pipelines.yaml
   :language: yaml