## Backend

1. Prerequisites

    - Python >= 3.12
    - Git
    - [uv](https://docs.astral.sh/uv/getting-started/installation/)
    - Fork this repository to your GitHub account

2. Installation and setup

   Clone your forked repository:

   ```shell
   git clone https://github.com/<your account>/fastapi_best_architecture.git
   ```

   Go to the root directory of the project, open the terminal, and run the following command:

   ```sh
   uv run fba init --auto
   ```

3. Checkout

   Checkout a new branch and make your changes

   ```shell
   git checkout -b your-new-feature-branch
   ```

4. Format and Lint

   ```shell
   fba format
   ```

5. Commit and push

   Commit your changes and push your branch to the GitHub.

6. PR

   Create a PR via GitHub

## Scripts

> [!WARNING]
>
> The following script may not apply to the Windows platform
>
> It is recommended to execute under the backend directory, and chmod authorization may be required

- `migrate.sh`: Perform automatic database migration

- `scripts/format.sh`: Perform ruff format with preview

- `scripts/lint.sh`: Perform prek formatting

- `scripts/export.sh`: Execute uv export dependency package
