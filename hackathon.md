## Setup

### Pre-requisite (Required)
- Clone this repo - `git clone git@github.com:gideonaina/secad.git`

- Install Docker (recommend v27). It comes with docker compose (minimum needed is v2, v1 version will not work with this lab).
    - Mac: https://docs.docker.com/desktop/setup/install/mac-install/
    - Windows: https://docs.docker.com/desktop/setup/install/windows-install/ 
    - Run `docker --version`  to confirm  the version of docker.
    - Run `docker compose version`  to confirm the version of docker compose.

- Install vscode: https://code.visualstudio.com/download
- Install the devcontainer extension in vscode. See details here: https://code.visualstudio.com/docs/devcontainers/tutorial

### Pre-requisite (Optional)

- Install pgAdmin: Used to inspect the content of the vector database.
    - Mac: https://www.pgadmin.org/download/pgadmin-4-macos/
    - Windows: https://www.pgadmin.org/download/pgadmin-4-windows/

- Install Just: Makes it easier to run the necessary commands as receipes (See Justfile in the repo for details). It is similar to what `Makefile` does.
    - Mac: run `brew install just`
    - Window: 
        * Install Scoop or Chocolatey
        ``` 
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
        ```
        * Once installed run `scoop install just`

### Running SECAD
- Go to https://platform.openai.com/settings/organization/api-keys, register/login into your account and create an API key. Load some money into your account ($10 is more than enough).
- Create a `.env` at the root of this project and copy the content of the `.env.sample` file into it. Provide the `OPENAI_API_KEY` value. Leave the rest as default. 
- To run, press Cmd + Shift + P (Mac) or Ctrl + Shift + P (Windows). From the dropdown, select `Devcontainers: Rebuild and Open in Container`
- Give it sometime to install all the dependencies.
- Open new a terminal, you should see `workspaces/secad/secad/` as the currently working directory. If not, something might not be properly setup.
- If everything looks good, run `just start`
- SECAD should be running on `localhost` on port `8501`. i.e. `localhost:8501`