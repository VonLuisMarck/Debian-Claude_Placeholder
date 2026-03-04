# Debian · Claude Code — Setup

Placeholder repository with a setup script that fixes common SSL certificate
errors when installing [Claude Code](https://claude.ai/code) on Debian-based
systems.

---

## Problem

When running `npm install -g @anthropic-ai/claude-code` on a Debian system
you may see:

```
npm ERR! code UNABLE_TO_GET_ISSUER_CERT_LOCALLY
npm ERR! errno UNABLE_TO_GET_ISSUER_CERT_LOCALLY
npm ERR! request to https://registry.npmjs.org/… failed,
         reason: unable to get local issuer certificate
```

This happens because npm can't locate the system's root CA bundle.

---

## Quick fix

```bash
sudo bash setup.sh
```

The script will:

1. Install / refresh `ca-certificates` via `apt`.
2. Install Node.js 20 LTS (via NodeSource) if it isn't already present.
3. Point npm at `/etc/ssl/certs/ca-certificates.crt`.
4. Install `@anthropic-ai/claude-code` globally.
5. Persist `NODE_EXTRA_CA_CERTS` in `/etc/environment` for future sessions.

---

## Manual fix (one-liner)

If you only want to fix npm's SSL config without running the full script:

```bash
sudo npm config set cafile /etc/ssl/certs/ca-certificates.crt
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
npm install -g @anthropic-ai/claude-code
```

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Debian / Ubuntu | any supported release |
| Node.js | ≥ 18 (script installs 20 LTS if missing) |
| npm | bundled with Node |

---

## After installation

```bash
claude   # launches Claude Code and prompts for authentication
```
