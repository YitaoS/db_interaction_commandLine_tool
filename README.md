# IDS706 Complex_SQL_Databricks
![CI Status](https://github.com/YitaoS/db_interaction_commandLine_tool/actions/workflows/cicd.yml/badge.svg)
## Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker (if using DevContainer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YitaoS/db_interaction_commandLine_tool.git
   cd db_interaction_commandLine_tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Build the development environment using DevContainer**:
   - Open the project in Visual Studio Code.
   - Run **Reopen in Container** from the Command Palette (`Ctrl + Shift + P` or `Cmd + Shift + P`).

### Usage

- **Run the main script**:
  ```bash
  python db_interaction_commandLine_tool/main.py <action> [query]
  ```
  - Replace `<action>` with either:
    - `load` - To load data into Databricks.
    - `query` - To execute a SQL query.
  - If using the `query` action, provide the SQL query as an additional argument.

  Example:
  ```bash
  python db_interaction_commandLine_tool/main.py query "SELECT * FROM default.customers;"
  ```

- **Run tests**:
  ```bash
  make test
  ```

- **Format the code**:
  ```bash
  make format
  ```