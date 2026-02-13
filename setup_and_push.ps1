# One-click setup and push script for this project
# Usage: Run from the project folder in an elevated PowerShell if needed:
#   powershell -ExecutionPolicy Bypass -File .\setup_and_push.ps1

param(
    [string]$RepoName = "document",
    [ValidateSet("public","private")][string]$Visibility = "public"
)

function Check-Command($name) {
    return (Get-Command $name -ErrorAction SilentlyContinue) -ne $null
}

Write-Host "Project path: $PWD"

if (-not (Check-Command git)) {
    Write-Host "Git not found. Attempting to install via winget..."
    try {
        winget install --id Git.Git -e --source winget -h
    } catch {
        Write-Warning "winget install failed or winget is not available. Please install Git manually from https://git-scm.com/downloads and re-run this script."
        exit 1
    }
} else {
    Write-Host "Git is installed."
}

if (-not (Check-Command gh)) {
    Write-Host "GitHub CLI (gh) not found. Attempting to install via winget..."
    try {
        winget install --id GitHub.cli -e --source winget -h
    } catch {
        Write-Warning "winget install failed or winget is not available. Please install GitHub CLI manually from https://cli.github.com/ and re-run this script."
        exit 1
    }
} else {
    Write-Host "GitHub CLI is installed."
}

# Initialize git repo if needed
if (-not (Test-Path -Path .git)) {
    Write-Host "Initializing local git repository..."
    git init
} else {
    Write-Host "Local git repository already initialized."
}

Write-Host "Staging files..."
git add .

# Commit (ignore failure if there are no changes)
try {
    git commit -m "Initial commit"
} catch {
    Write-Host "No changes to commit or commit failed: $_"
}

# Ensure main branch exists and is named 'main'
try {
    git branch -M main
} catch {
    # ignore
}

# Authenticate with GitHub
Write-Host "Checking GitHub authentication..."
$auth = gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not authenticated with GitHub. Launching 'gh auth login'..."
    gh auth login
} else {
    Write-Host "Already authenticated with GitHub."
}

$visFlag = if ($Visibility -eq 'public') { '--public' } else { '--private' }

Write-Host "Creating repository '$RepoName' on GitHub (visibility: $Visibility) and pushing..."
try {
    gh repo create $RepoName $visFlag --source=. --remote=origin --push --confirm
    Write-Host "Repository created and pushed."
} catch {
    Write-Warning "'gh repo create' failed. If the repository already exists, try pushing manually with:"
    Write-Host "  git remote add origin https://github.com/<USERNAME>/$RepoName.git"
    Write-Host "  git push -u origin main"
    exit 1
}

# Output final remote URL
try {
    $url = gh repo view $RepoName --json url -q .url
    Write-Host "Repository URL: $url"
} catch {
    Write-Host "Completed; please check your GitHub account for the new repository named '$RepoName'."
}
