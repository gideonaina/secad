## Setup

### Pre-requisite (Required)

- Install Docker (recommend v27). It comes with docker compose (minimum need is v2, v1 version will not work with this lab.
    - Mac: https://docs.docker.com/desktop/setup/install/mac-install/
    - Windows: https://docs.docker.com/desktop/setup/install/windows-install/ 
    - Run docker --version  to confirm  the version of docker
    - Run docker compose version  to confirm version of docker compose

- Install vscode: https://code.visualstudio.com/download
- Install the devcontainer extension in vscode. See details here: https://code.visualstudio.com/docs/devcontainers/tutorial

### Pre-requisite (Optional)

- Install pgAdmin: This help inspect the content of the vector database
    - Mac: https://www.pgadmin.org/download/pgadmin-4-macos/
    - Windows: https://www.pgadmin.org/download/pgadmin-4-windows/

- Just: Install this make it easier to run the necessary commands as receipes (See Justfile in the repo for details)
    - Mac: run `brew install just`
    - Window: 
        * Install Scoop or Chocolatey
        ``` 
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
        ```
        * Once installed run `scoop install just`

### Running SECAD
- Go to https://platform.openai.com/settings/organization/api-keys, register/login into your account and create a key. Load $10 into your account.
- Create a `.env` at the root of this project and copy the content of the `.env.sample` file into it. Provide the `OPENAI_API_KEY` value. Leave the rest as default if you choose. 
- To run, press Cmd + Shift + P (Mac) or Ctrl + Shift + P (Windows). From the dropdown, select `Devcontainers: Rebuild and Open in Container`
- Give it sometime to install all the dependencies.
- Open new terminal, you should see `workspaces/secad/secad/` as the currently working dir. If not, something might not be properly setup.
- If everything looks good, run `just start`
- SECAD should be running on `localhost` on port `8501`. i.e. `localhost:8501`