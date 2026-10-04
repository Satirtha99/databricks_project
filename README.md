# Databricks Asset Bundle – GitHub Actions CI/CD

This repository contains the configuration and source code required to deploy and manage **Databricks Asset Bundles (DABs)** using **GitHub Actions**.

The primary goal of this project is to provide a consistent and automated CI/CD process for deploying Databricks resources such as notebooks, jobs, workflows, and related configurations across different environments.

## Overview

This project uses:

* **Databricks Asset Bundles (DAB)** for packaging and deploying Databricks resources.
* **GitHub** for source code management.
* **GitHub Actions** for CI/CD automation.
* **Databricks CLI** for bundle validation and deployment.

The deployment process is designed to reduce manual changes in Databricks and ensure that infrastructure and application code are deployed consistently through version-controlled workflows.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── resources/
│   ├── jobs.yml
│   └── ...
│
├── src/
│   ├── notebooks/
│   ├── scripts/
│   └── ...
│
├── databricks.yml
├── README.md
└── ...
```

> The exact directory structure may vary depending on the resources managed by the project.

## Prerequisites

Before working with this project, make sure you have:

1. Access to the required Databricks workspace(s).
2. A GitHub repository with permission to run GitHub Actions.
3. Databricks CLI installed locally.
4. Appropriate Databricks authentication configured.
5. Required GitHub Actions secrets/variables configured.

## Databricks Asset Bundles

The main bundle configuration is defined in:

```text
databricks.yml
```

This file defines the bundle configuration, targets, workspace settings, and resources that should be deployed.

A simplified example:

```yaml
bundle:
  name: my-databricks-project

include:
  - resources/*.yml

targets:
  dev:
    mode: development
    workspace:
      host: https://<databricks-workspace-url>

  uat:
    workspace:
      host: https://<databricks-workspace-url>

  prod:
    workspace:
      host: https://<databricks-workspace-url>
```

## Environments

The bundle can be configured for multiple environments.

Typical environments include:

| Environment | Purpose                 |
| ----------- | ----------------------- |
| `dev`       | Development and testing |
| `uat`       | User Acceptance Testing |
| `prod`      | Production              |

Each environment can have its own Databricks workspace, configuration, variables, and deployment rules.

Example:

```bash
databricks bundle deploy -t dev
```

```bash
databricks bundle deploy -t uat
```

```bash
databricks bundle deploy -t prod
```

## Local Development

### 1. Validate the Bundle

Before deploying, validate the bundle configuration:

```bash
databricks bundle validate -t dev
```

This checks whether the bundle configuration is valid.

### 2. Deploy the Bundle

To deploy to a specific environment:

```bash
databricks bundle deploy -t dev
```

For UAT:

```bash
databricks bundle deploy -t uat
```

For Production:

```bash
databricks bundle deploy -t prod
```

### 3. Run a Deployed Job

If the bundle contains Databricks jobs, you can run them using the Databricks CLI after deployment.

```bash
databricks bundle run <job-name> -t dev
```

## GitHub Actions

GitHub Actions is used to automate bundle validation and deployment.

A typical workflow looks like:

```text
Developer
    |
    v
Git Push / Pull Request
    |
    v
GitHub Actions
    |
    +----> Validate Bundle
    |
    +----> Test / Quality Checks
    |
    v
Deploy to Databricks
    |
    +----> DEV
    |
    +----> UAT
    |
    +----> PROD
```

### Example GitHub Actions Workflow

The workflow can be configured in:

```text
.github/workflows/deploy.yml
```

Example:

```yaml
name: Databricks Bundle Deployment

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install Databricks CLI
        uses: databricks/setup-cli@main

      - name: Validate Databricks Bundle
        run: databricks bundle validate -t dev

  deploy:
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install Databricks CLI
        uses: databricks/setup-cli@main

      - name: Deploy Databricks Bundle
        run: databricks bundle deploy -t dev
```

> Adjust the workflow according to your organization's branching strategy and environment promotion process.

## Authentication

GitHub Actions requires authentication to access the Databricks workspace.

Authentication credentials should **not** be hard-coded in:

* `databricks.yml`
* Notebook files
* Python scripts
* GitHub workflow files

Instead, configure credentials using **GitHub Secrets**, environment variables, or your organization's preferred secure authentication mechanism.

Example GitHub repository secrets/variables may include:

```text
DATABRICKS_HOST
DATABRICKS_TOKEN
```

The exact authentication mechanism should follow your organization's security requirements.

## Recommended CI/CD Flow

A recommended deployment flow is:

### Pull Request

When a Pull Request is created:

```text
Pull Request
     |
     v
GitHub Actions
     |
     v
Bundle Validation
     |
     v
Quality / Test Checks
```

The Pull Request should be merged only after the validation checks pass.

### Development Deployment

After merging changes:

```text
main branch
     |
     v
GitHub Actions
     |
     v
Deploy DAB
     |
     v
DEV Workspace
```

### UAT Deployment

Once the changes are ready for testing:

```text
main / release
     |
     v
GitHub Actions
     |
     v
Deploy DAB
     |
     v
UAT Workspace
```

### Production Deployment

Production deployment should preferably require an approval or controlled promotion:

```text
Approved Release
     |
     v
GitHub Actions
     |
     v
Deploy DAB
     |
     v
PROD Workspace
```

## Bundle Commands

Common commands used during development:

### Validate

```bash
databricks bundle validate -t <target>
```

### Deploy

```bash
databricks bundle deploy -t <target>
```

### Run

```bash
databricks bundle run <resource-name> -t <target>
```

### Destroy

Use with caution:

```bash
databricks bundle destroy -t <target>
```

## Development Guidelines

### 1. Use Git for Changes

All Databricks code and configuration should be maintained in Git rather than making unmanaged changes directly in the Databricks workspace.

### 2. Use Pull Requests

Changes should go through Pull Requests so that they can be reviewed before deployment.

### 3. Do Not Commit Secrets

Never commit:

```text
Tokens
Passwords
Client secrets
Private keys
Connection strings
```

Use GitHub Secrets, environment variables, or an approved secret-management solution instead.

### 4. Validate Before Deployment

Run:

```bash
databricks bundle validate -t <target>
```

before deploying changes.

## Deployment Strategy

The recommended deployment strategy is:

```text
Feature Branch
      |
      v
Pull Request
      |
      v
Validation
      |
      v
Merge
      |
      v
DEV
      |
      v
UAT
      |
      v
PROD
```

This ensures that changes are reviewed and validated before reaching production.

## Benefits

Using Databricks Asset Bundles with GitHub Actions provides:

* Version-controlled Databricks resources
* Automated deployments
* Consistent environment configuration
* Reduced manual deployment effort
* Pull Request-based code reviews
* Repeatable deployments
* Environment-specific configuration
* Better CI/CD integration
* Improved deployment traceability

## Troubleshooting

### Bundle validation fails

Run:

```bash
databricks bundle validate -t <target>
```

and review the validation output.

Check:

* `databricks.yml`
* Resource YAML files
* Target configuration
* Variable definitions
* Workspace configuration

### Authentication fails

Verify that the GitHub Actions environment has the required Databricks authentication configuration and that the credentials have the required permissions.

### Deployment fails

First validate the bundle:

```bash
databricks bundle validate -t <target>
```

Then check the deployment logs from GitHub Actions and verify that the configured Databricks principal has permission to create or update the required resources.

## Future Improvements

Potential improvements to this project include:

* Automated unit and integration testing
* Automated code quality checks
* Environment approval gates
* Automated deployment notifications
* Release-based production deployments
* Infrastructure drift detection
* Automated rollback strategies
* Integration with centralized secret management

## Summary

This project provides a Git-based CI/CD approach for managing **Databricks Asset Bundles**.

The combination of **Databricks Asset Bundles + GitHub + GitHub Actions** allows Databricks resources to be developed, reviewed, validated, and deployed through a consistent automated process.

```text
GitHub
   |
   v
GitHub Actions
   |
   v
Databricks Asset Bundle
   |
   +------> DEV
   |
   +------> UAT
   |
   +------> PROD
```
