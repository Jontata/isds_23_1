# Git Setup and SSH Key Configuration

This guide will walk you through the initial setup for Git and the creation of an SSH key for secure communication with your GitHub repositories.

## Initial Git Configuration

Before you start using Git, it's essential to set up your identity. These configurations are stored in the `.gitconfig` file in your home directory.

```bash
# Set your name - this identifies who is making changes in Git's history
git config --global user.name "Your Name"

# Set your email - this should ideally be the same email you use for your GitHub account
git config --global user.email "your.email@example.com"
```

## Generating an SSH Key

SSH keys are a secure way of authenticating to GitHub without needing to enter a password every time.

```bash
# Generate an RSA key pair with a 4096-bit encryption and associate it with your email
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

## Starting the SSH Agent

The SSH agent is a background process that manages your SSH keys for authentication.

```bash
# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your newly created SSH key to the agent
# This allows the agent to use this key for authentication without asking you every time
ssh-add ~/.ssh/id_rsa
```

## Copying SSH Key to Clipboard

To add your SSH key to GitHub, you'll need to copy it. 

```bash
# Copy your public SSH key to clipboard (for Git Bash on Windows)
cat ~/.ssh/id_rsa.pub | clip        
```

## Testing SSH Connection

Before cloning or interacting with GitHub, ensure that your SSH setup is correct.

```bash
# Test the SSH connection to GitHub
ssh -T git@github.com
```

## Cloning a Repository

Now, you can clone repositories securely over SSH.

```bash
# Clone a specific repository to your local machine
git clone git@github.com:Jontata/isds_23_1.git
```

## Connecting After the First Time

Once you've set everything up for the first time, you don't need to redo the entire process. For future interactions:

1. Make sure your SSH agent is running (`eval "$(ssh-agent -s)"`).
2. Use `git` commands like `git clone`, `git pull`, and `git push` as needed.
