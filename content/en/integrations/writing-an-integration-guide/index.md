---
title: "How to document an integration"
description: "The information needed to reproduce a connection to a service."
date: 2026-09-29
tags: [integrations, authoring]
---
This is an authoring guide. It does not describe an existing NQ2 API. Fill in actual URLs, parameters, and requirements based on the integration you implement.

## Purpose and requirements

Explain which data moves between the application and the service, in which direction, and when. Specify the required application version and account permissions.

## Configuration

List the configuration fields and explain their meaning. Use placeholders such as `YOUR_TOKEN` instead of real credentials in examples.

## Sample request and response

Include a minimal, reproducible example. Specify the HTTP method, path, data format, and expected status code. Place any configuration attachment next to this Markdown file and link to it.

## Error handling

Describe common authentication errors, service limits, retry rules, and how to verify that synchronization succeeded.
