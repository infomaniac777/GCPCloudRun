# GKE Experiments

![CI/CD](https://github.com/infomaniac777/GKECloudNative/actions/workflows/build.yml/badge.svg)

A FastAPI app running on Google Kubernetes Engine, deployed via a fully automated CI/CD pipeline.

## Stack

- **App** — FastAPI (Python)
- **Container** — Docker → Google Artifact Registry
- **Orchestration** — GKE (Standard, spot node)
- **Packaging** — Helm
- **CI/CD** — GitHub Actions (build → push → deploy)

## Pipeline

Every push to `main`:
1. Runs unit tests
2. Builds and pushes a Docker image tagged with the git SHA
3. Deploys to GKE via Helm
