# Comprehensive Document Translation & Summary Report

**Source Document:** ex06-Dual AI agent race via MCP servers.pdf (17 pages)

---

--- PAGE 1 ANALYSIS ---

This is the title page of a technical document.

**Document Title:**
* Primary Title: Dual AI Agent Conversation via MCP Servers
* Subtitle: Task 6: Pursuit of thieves and autonomous agents in a partial observation environment

**Author and Copyright Information:**
* Author: Dr. Yoram Segal
* Copyright Notice: All rights reserved - (c) Dr. Yoram Segal

**Metadata:**
* Date: 19-06-2026
* Classification/Version: Lesson L09 | Version 1.0

--- PAGE 2 ANALYSIS ---

**Header:**
Lesson Title: AI Agent Conversation via MCP Servers

**1. Keywords**
Model Context Protocol (MCP) | Orchestration of AI Agents | Multi-Agent System | Natural Language Communication | Dec-POMDP | Free Pursuit (Police and Thieves) | Partial Observation | Library | MCP Server | MCP Client | FastMCP | Large Language Model (LLM) | Cloud and Local | Prefect Cloud | Nginx, Localtonet, ngrok, Ollama | Security and OAuth | Q-Learning | Bellman Equation | Application-Policy | Configuration and Reporting File | JSON | Gmail API | Graphical User Interface (GUI) | Game Theory and Prisoner's Dilemma | Teamwork and Time Pressure.

**2. Introduction and Academic Framework**
This lesson is dedicated to the advanced task (Task 6) within the framework of the course "Orchestration of AI Agents" in the Department of Computer Science at the University of Haifa. This is a regular task in the series of ongoing assignments, but it includes an optional bonus of up to 10 points toward the final project (which is published and submitted separately). The overarching goal of the task is to transition the students from thinking about a single agent operating in a static environment to the world of distributed multi-agent systems, where a number of autonomous entities are required to make complex decisions in real-time while coordinating with each other.

Dr. Yoram Segal emphasizes that the main focus is on the optimization of decision-making algorithms, system engineering, and natural language communication between remote agents. Since reinforcement learning is not a prerequisite for the course, the use of complex algorithms is defined as a recommendation only for academic enrichment and is not a mandatory requirement. Students must demonstrate the ability to orchestrate a complex system by building a full pipeline that enables two AI agents to play this game successfully, while coping with partial observation of the board and inherent environmental uncertainty.

**Footer:**
(c) Dr. Segal Yoram - All rights reserved | 2

--- PAGE 3 ANALYSIS ---

**3. Definition of the Core Task and Orchestration Challenge**

The primary task is to design, implement, and operate a full end-to-end game that enables two AI agents—the "Cop" and the "Thief"—to conduct a dynamic pursuit game on a two-dimensional grid. The system orchestration requires the agents to:

1. **Interpret** their messages in natural language.
2. **Infer** conclusions regarding the opponent's location based on partial observation.
3. **Translate** insights into physical steps on the grid network.

The **central success metric** is the communication capability and orchestration of the agent pair—not the game strategy itself. Each group is required to present a proper game session between a pair of agents (Cop and Thief) belonging to it, managed via its MCP server, in a fully autonomous manner—without manual intervention, from the initialization stage to the sending of the summary report.

**4. Game Rules and Scoring System**

**4.1 Structure of the Games and the Match**

The process is based on a clear distinction between two levels:

* **Sub-game:** A single pursuit round, limited to a maximum of 25 moves. In each move, the players are allowed to change location or perform a special action. The game proceeds in turns—usually the thief moves first, followed by the cop, and so on.
* **Game:** A complete sequence of 6 consecutive sub-games; the results of all sub-games are accumulated and reported together at the end of the sequence.

**Footer:**
(c) Dr. Segal Yoram - All rights reserved | 3

--- PAGE 4 ANALYSIS ---

**4.2 The Game Board**
The game board is a two-dimensional grid with a default size of 5x5 squares. The system is required to support a generic architecture that allows for dynamic changes to the board size via a configuration file (not hard-coded). Each square has coordinates, and the thief and the cop start at random locations on the board (or chosen by strategy). Movement is possible in all directions, including diagonally. The game is effectively a state machine; the state changes with every step on the board.

**4.3 Winning Conditions and Barrier Placement**
- **Cop Win:** Achieved when the cop reaches the exact square where the thief is located (capture).
- **Thief Win:** Achieved if the thief survives 25 steps without the cop landing on their square throughout the entire game.
- **Barrier Placement:** As an alternative action to movement, the cop is permitted to place a barrier in the square where they are currently standing. This action prevents them from advancing in that step, but the blocked square becomes impassable for both the thief and the cop (similar to a wall or the edge of the board). The cop is limited to a maximum of 5 barriers per game; the thief cannot place barriers.

**4.4 Scoring System**
The score is calculated for each sub-game separately.

**Table 1: Scoring for a Single Sub-game**

| Game Outcome | Cop Score | Thief Score |
| :--- | :--- | :--- |
| Cop wins | 20 | 5 |
| Thief wins | 5 | 10 |

The maximum possible score for a group in a full game (sequence of 6 sub-games) is 90 points (3 x 20 for the cop and 3 x 10 for the thief), and the minimum score is 30 points.

**Footer:**
(c) Dr. Segal Yoram - All rights reserved | 4

--- PAGE 5 ANALYSIS ---

**4.5 Sanity Checks**

To perform integration tests and prevent technical failures in advanced stages, it is recommended to perform Sanity Checks across different board dimensions:

**Table 2: Recommended Sanity Check Stages**

| Stage | Grid Dimensions | Goal and Validation | Complexity |
| :--- | :--- | :--- | :--- |
| 1 | 2x2 | Algorithmic sanity check, basic integration of the pipeline, and message transmission verification | Very Low |
| 2 | 3x3 / 3x2 | Testing coordination mechanisms, hyper-parameter calibration, and failure identification | Medium |
| 3 | 4x4 / 4x3 | Testing the impact of ambiguity; initial distance increases with visibility radius | High |
| 4 | 5x5 | Final test run, graph extraction, and analysis of the entire game results | Maximum |

**5. MCP Server Architecture and Natural Language Communication**

**5.1 Two Servers, Natural Language, and Tools**

The Model Context Protocol (MCP) is an open standard for connecting Large Language Models (LLMs) to data sources, tools, and external servers. The orchestration basis is the division into two independent MCP servers: one for the Cop and one for the Thief. The core principle: the agents do not communicate via the protocol directly. The agents do not exchange raw coordinates — but rather natural language. In each turn, the agent generates text messages describing its intentions, observations, or attempts at deception; the recipient agent uses tools (Tools) exposed by its MCP server to read the message, analyze it with the help of the LLM, update the state assessment, and choose its next action. The MCP server of each agent is built using the FastMCP package, which exposes the external world to the tools for mutual verification of locations, sending messages, and receiving them.

**Footer:**
(c) Dr. Segal Yoram - All rights reserved | 5

--- PAGE 6 ANALYSIS ---

**5.2 MCP Client vs MCP Server**

A fundamental architectural point: The Large Language Model (LLM) is not operated or hosted within the MCP server. The MCP server is a separate component that exposes tools, resources, and prompt templates. The MCP Client is the game engine or orchestrator that manages the dialogue and logic. The workflow: The client sends a query to the LLM, receives a decision from it to execute a tool (Tool Call), calls the MCP server to perform the action, and returns the result to the LLM for the purpose of completing the environment.

**6. MCP Server Deployment and Management**

- **Phase One - Local Execution:** Setting up and running two servers on the local machine (localhost) in separate ports, and verifying that the game engine and the agents have full interaction with each other.
- **Phase Two - Cloud Deployment:** After verifying the pipeline locally, upload the MCP servers to a public cloud (such as Prefect Cloud or a similar distributed platform).
- **Security and Authentication:** It is mandatory to implement a token-based authentication mechanism that allows for encryption and access revocation when necessary, to prevent unauthorized third-party access.
- **Critical Security and Networking Note:** One must ensure that the MCP server URLs are completely inaccessible from the public internet and are not blocked by a firewall. Therefore, it is not recommended to run them from a workplace or organizational network that tends to block incoming/outgoing traffic on non-standard ports. Each group requires two URLs — one for the cop and one for the thief.

**7. LLM Architecture: Three Approaches for Language Model Connection**

Even in the cloud, the MCP server still requires an LLM. There are three central architectural approaches.

**Footer:**
(c) Dr. Segal Yoram - All rights reserved | 6

--- PAGE 7 ANALYSIS ---

**7. LLM Architecture: Three Approaches for Language Model Connection (Continued)**

**7.1 Approach 1: Public Cloud API Model (The Simple and Recommended Approach)**
Instead of running a local model and exposing it, the MCP client connects directly to a public cloud API provider (such as OpenAI, Anthropic, or Gemini) using an API key.
* **Mechanism of Action:** The game engine sends an HTTP request with the API key to the cloud provider, receives a response from the LLM containing the tool decision (Tool Call), and writes the call to the MCP server in the cloud.
* **Advantages:** A stable and fast solution without the need to expose a personal computer, and without firewall or local hardware issues. Since latency is low and consumption is minimal, it is possible to use even free or low-cost models.

**7.2 Approach 2: Secure Exposure of Local Ollama to the Cloud**
Ollama runs local models and uses port 11434 by default on Loopback (127.0.0.1) only, without a built-in security mechanism; direct exposure constitutes a severe cyber risk. Therefore, if one wishes to run a local LLM while the MCP server is in the cloud, it is mandatory to use tunneling tools that add a security layer:
* **ngrok with Traffic Policy:** Creation of a secure public HTTPS URL that redirects to the local Ollama, while restricting access via Basic Auth defined in the ollama.yaml file, and running the manager via the CLI within the port and policy file. The MCP server accesses the model only with an Authorization Header.
* **Localtonet:** Similar to ngrok, it opens a public tunnel to 127.0.0.1:11434, with convenient options for enabling HTTP Authentication via a management interface.
* **Self-Hosted Nginx Reverse Proxy (For full engineering use):** An Nginx server acting as a Reverse Proxy for Ollama, performing SSL Termination (via Certbot / Let's Encrypt), requiring authentication in an htpasswd file, and blocking the Ollama port in the local firewall (nftables / UFW).

**7.3 Approach 3: Hybrid Architecture (Recommended for Secure Local Development)**
Instead of exposing the local Ollama, the language model and the game client (the orchestrator) are kept on the local computer, and only the MCP server is kept in the cloud. The LLM (via local Ollama) and the game client both run locally; the game client connects to Ollama at the address localhost:11434 with **no exposure at all**.

**Footer:**
(c) Dr. Segal Yoram - All rights reserved | 7

--- PAGE 8 ANALYSIS ---

The client must contact the MCP server by making an outbound HTTPS request to the cloud servers. This is safer because outbound requests do not require opening inbound ports. The Ollama instance remains behind the local firewall, and only the MCP server (which contains no keys or sensitive data) is accessible to the public.

**8. Recommended Reinforcement Learning Algorithm: Simple Q-Table**

The use of Reinforcement Learning is optional and recommended only for specific cases. Groups that are not interested in developing decision-making mechanisms based on heuristics, decision trees, or direct instructions to the language model (Prompt Engineering) may skip this. However, Dr. Segal notes that for integrating reinforcement learning, the developer of a winning adaptive game suggests Q-Learning (Tabular Q-Learning) as a basic integration without the need for training deep neural networks.

**8.1 State, Action, and Reward**

The three fundamental building blocks are:
* **State (s):** Where the agent is located.
* **Action (a):** The move (movement in any direction).
* **Reward (r):** The quality score of the state.

Dr. Segal illustrates this using a drone searching for treasure: every step consumes fuel (a small negative reward), falling into a pit results in a large penalty, and reaching the treasure results in a positive reward. Through trial and error over many episodes, the agent learns which states are more valuable.

---
(c) Dr. Segal Yoram - All rights reserved | 8

--- PAGE 9 ANALYSIS ---

**8.2 Q-Table and Bellman Equation**

In the Q-table, each row represents a state *s*, each column represents an action *a*, and the value *Q(s, a)* represents the "quality" of the action and the expected cumulative reward in the long term. In each step, the agent chooses an action according to an exploration and exploitation policy (Epsilon-Greedy), receives an immediate reward *r*, and moves to the next state *s'*. The table update is performed using the Bellman Equation:

*Equation:*
Q(s, a) ← Q(s, a) + [r + max_{a'} Q(s', a') - Q(s, a)]

Where:
* ** (Learning Rate):** Common values are between 0.01 and 0.5, determining how much the new information influences the existing value.
* ** (Discount Factor):** Between 0 and 1, representing the importance of future rewards. It is the expected maximum reward from the next state.

Below is minimal code for updating the Q-table:

**Updating the Q-table according to the Bellman Equation**

```python
import numpy as np

# 5x5 grid -> 25 states, 4 movement actions
num_states = 25
num_actions = 4
q_table = np.zeros((num_states, num_actions))

# learning hyper-parameters
learning_rate = 0.1
discount_factor = 0.9

def update_q_table(state, action, reward, next_state, done):
 # max Q for the next state
 best_next_q = 0.0 if done else np.max(q_table[next_state])
 
 # TD target and TD error
 td_target = reward + discount_factor * best_next_q
 td_error = td_target - q_table[state, action]
 
 # Q-value update
```

---
9 | (c) Dr. Segal Yoram - All rights reserved

--- PAGE 10 ANALYSIS ---

The page continues the code block from the previous page and introduces section 9 regarding automated email reporting and JSON structures.

**Code Continuation:**
```python
q_table[state, action] += learning_rate * td_error
```

**Textual Summary of the preceding paragraph:**
This method allows agents to improve their operational policies over time through trial and error, without requiring heavy computational resources or deep libraries.

---

**9. Automated Email Reporting and JSON Structure**

At the end of every game, the agent is required to trigger an automated summary email function to the destination address: rmisegal+uoh26b@gmail.com.

**Technology Recommendation:** Use the Google API Client to ensure reliability and avoid being blocked by external mail servers. Dr. Segal explains that it is preferable to use **Token-Based Authentication** rather than a username and password. This is because a password exposes the user to a breach, whereas a one-time, time-limited token (such as those provided by Google) is useless if stolen, as it is only valid for a short time and has limited scope. In the Google Developers Console, the client receives a secret file and a token created during the initial authentication.

**Two additional rules:**
* Games that did not reach a conclusion due to a Technical Loss are defined as failed and must be re-run to complete the quota of 6 games.
* The email body must contain **only** the JSON report, without free text, to allow for automated ingestion and processing by the testing system.

**9.1 Internal Game JSON Report**

This report is intended for games where each group runs independently between agents. It includes a single GitHub link and two URLs for the active MCP servers (one for the agent and one for the opponent).

---
10 | (c) Dr. Segal Yoram - All rights reserved

--- PAGE 11 ANALYSIS ---

This page provides technical specifications for JSON reporting structures used in game reporting, specifically for internal game reports and inter-group bonus games.

**Internal Game JSON Structure**
The page displays a code block representing the structure of an internal game report:

```json
{
 "group_name": "Team-Alpha",
 "students": [],
 "github_repo": "https://github.com/team-alpha/marl-cop-thief",
 "cop_mcp_url": "https://cop-mcp-alpha.prefect.run",
 "thief_mcp_url": "https://thief-mcp-alpha.prefect.run",
 "timezone": "Asia/Jerusalem",
 "sub_games": [],
 "totals": {
 "cop": 90,
 "thief": 40
 }
}
```

**9.2 Inter-Group Bonus Game JSON**
This section describes the reporting format for competitions between different groups in the cloud. It includes documentation for two groups, two separate GitHub links, and four URL links for the MCP servers (a cop server and a thief server for each group).

**Inter-Group Bonus Game JSON Structure**
The page displays a code block representing the structure of an inter-group bonus game report:

```json
{
 "report_type": "bonus_game",
 "groups": {
 "group_1": "Team-Alpha",
 "group_2": "Team-Beta"
 },
 "github_repo_group_1": "https://github.com/team-alpha/marl-cop-thief",
 "github_repo_group_2": "https://github.com/team-beta/marl-cop-thief",
 "mcp_url_group_1_cop": "https://cop-mcp-alpha.prefect.run",
}
```

**Footer Information**
* Page Number: 11
* Copyright Notice: (c) Dr. Segal Yoram - All rights reserved

--- PAGE 12 ANALYSIS ---

This page provides the continuation of the JSON code block for the Inter-Group Bonus Game report initiated on the previous page.

**JSON Code Continuation:**

```json
"mcp_url_group_1_thief": "https://thief-mcp-alpha.prefect.run",
"mcp_url_group_2_cop": "https://cop-mcp-beta.prefect.run",
"mcp_url_group_2_thief": "https://thief-mcp-beta.prefect.run",
"timezone": "Asia/Jerusalem",
"students_group_1": [],
"students_group_2": [],
"sub_games": [],
"totals_by_group": {
"Team-Alpha": 60,
"Team-Beta": 80
},
"bonus_claim": {
"Team-Alpha": 7,
"Team-Beta": 10
},
"mutual_agreement": true
}
```

**Footer Information:**
* Copyright Notice: (c) Dr. Segal Yoram - All rights reserved
* Page Number: 12

--- PAGE 13 ANALYSIS ---

**10 Configuration File**

As part of advanced software development principles, hard-coding game parameters is strictly prohibited. All parameters must be centralized in a configuration file (config.json or config.yaml) which must include at least the following:

**Table 3: Configuration File Parameters**

| Parameter Name | Description | Default Value |
| :--- | :--- | :--- |
| grid_size | Dimensions of the 2D grid in which the game is played | [5, 5] |
| max_moves | Maximum number of steps per game | 25 |
| num_games | Number of games that make up the series | 6 |
| max_barriers | Maximum number of barriers the cop is allowed to place | 5 |
| scoring.cop_win | Score for a successful cop capture | 20 |
| scoring.thief_win | Score for a successful thief evasion | 10 |
| scoring.cop_loss | Score for the cop in case of thief evasion | 5 |
| scoring.thief_loss | Score for the thief in case of capture | 5 |

**11 Submission Requirements and Scientific README Report**

The submission includes two primary deliverables: a public GitHub repository containing all source code, and a documentation and scientific analysis file named README.md located in the root of the repository. The report must be written in high-level scientific language and include:

- **Formal Modeling:** Presentation of the decentralized game problem as a Decentralized Partially Observable Markov Decision Process (Dec-POMDP), including the definition of the mathematical tuple and a description of the state space and observations. The general tuple is:

< n, S, {Ai}, P, R, {Oi}, O, gamma >

**Footer Information:**
* Page Number: 13
* Copyright Notice: (c) Dr. Segal Yoram - All rights reserved

--- PAGE 14 ANALYSIS ---

The page continues the technical requirements for the scientific README report and introduces the Inter-Group Bonus Competition.

**Continuation of Section 11: Scientific README Report Requirements**

The text defines the components of the Dec-POMDP tuple:
* n: Number of agents.
* S: State space (player and barrier locations).
* {Ai}: Actions for each agent (movement and barrier placement).
* P: Transition function.
* R: Reward function.
* {Oi}: Observation space.
* O: Observation function.
* gamma: Discount factor.

Additional required sections for the report:
* **Communication Challenges Analysis:** An in-depth discussion on managing free-text communication, including handling ambiguity and ensuring mutual understanding without a pre-defined protocol.
* **Visualization and Proofs:** Graphs of learning curves (if using Q-Table), screenshots of the Graphical User Interface (GUI) showing game progress, and logs from the Command Line Interface (CLI) demonstrating valid communication with the MCP server in the cloud.

---

**12 Inter-Group Bonus Competition**

Beyond the mandatory requirements, a bonus of 10 points is available for the final project. To qualify, the series of games must be submitted within one week of the assignment's publication. The bonus is intended for two groups that conduct a full series of 6 games in the cloud, where each group sends a separate email report confirming the exact same result (mutual agreement via JSON data).

**12.1 Role Allocation**
* In the first 3 games: The cop from Group A plays against the thief from Group B.
* In the remaining 3 games: The cop from Group B plays against the thief from Group A.

---

**Footer Information:**
* Page Number: 14
* Copyright Notice: (c) Dr. Segal Yoram - All rights reserved

--- PAGE 15 ANALYSIS ---

**12.2 Bonus Accumulation Rules**

* It is permitted and recommended to play against more than one group.
* The group with the highest accumulated score in a series wins 10 points; the losing group wins 5 points; in the case of a complete tie, each receives 5 points.
* The final bonus grade is calculated as the average of the results of all valid series. For example, a group that played two series, winning one (10) and losing the second (7), will receive a final bonus of 8.5 points.
* Disagreement or lack of correlation between the reports leads to the cancellation of the bonus and receipt of 0 points for both parties for that series.

**Footer Information:**
* Page Number: 15
* Copyright Notice: (c) Dr. Segal Yoram - All rights reserved

--- PAGE 16 ANALYSIS ---

**13 Summary and Work Guidelines: Engineering Priorities**

To ensure the product reaches completion and within time constraints, it is recommended to operate according to the following order:

**Table 4: Recommended Development Priorities**

| Step | Required Activity | Functional Focus |
| :--- | :--- | :--- |
| 1 | Game logic and rules | Defining legal grid movement, agent movement, barrier placement, and capture identification |
| 2 | Basic MCP communication infrastructure | Setting up two separate MCP servers that allow mutual location verification |
| 3 | Full local execution | Connecting two agents and preventing the game from running on Localhost to avoid pipe errors |
| 4 | Decision-making mechanism | Developing a strategy (Heuristic-based or Q-Table) |
| 5 | Natural language integration | Exchanging protocols for locations via free-text message exchange |
| 6 | Graphical User Interface (GUI) | Building a visual interface that displays agent and barrier movement in real-time |
| 7 | Cloud deployment | Uploading the MCP server to the cloud while paying attention to firewalls and cyber security |
| 8 | Gmail API connection | Implementing automated JSON report sending to the lecturer at the end of 6 games |

**14 Key Insights**

- **Infrastructure before the game:** The target value is the synchronization capability — setting up two autonomous AI agents that coordinate protocols in natural language via an MCP server — and not the game result or strategy.

**Footer Information:**
* Page Number: 16
* Copyright Notice: (c) Dr. Segal Yoram - All rights reserved

--- PAGE 17 ANALYSIS ---

The page contains a list of technical and project management insights, followed by copyright information.

**Technical and Project Insights:**

* **Natural Language, Not Rigid Protocol:** The agents are autonomous and independent; as long as they understand each other, the internal implementation does not matter. The problem is modeled as a Dec-POMDP with partial observations.
* **Server/Client Separation:** The language model resides in the client (the orchestrator), while the MCP server exposes tools only.
* **From Local to Cloud:** Gradual progression from localhost on separate ports, to cloud deployment, and finally inter-group competition — while dealing with domains, tokens, tunneling, and cyber security.
* **Three LLM Access Approaches:** Cloud API, local Ollama, or hybrid architecture with outbound requests only.
* **Security and Automation:** Tokens (Traffic Policy ngrok, OAuth) replace passwords, and the Gmail API enables autonomous JSON reporting.
* **Soft Skills:** Teamwork, management under uncertainty, and time pressure — inspired by the Prisoner's Dilemma.

**Footer Information:**

* Copyright Notice: All Rights Reserved - Dr. Yoram Segal
* Page Number: 17

---

## Cross-Reference Clarifications

- **Page 3 → Page 4:** Page 4 details the specific winning conditions, barrier placement rules, and the scoring system for the pursuit game.
- **Page 5 → Page 4:** Page 4 provides the recommended grid dimensions and complexity levels for sanity checks.
- **Page 6 → Page 7:** Page 7 outlines the three specific architectural approaches for connecting the LLM to the MCP server.
- **Page 8 → Page 9:** Page 9 provides the mathematical definition of the Bellman Equation and the corresponding Python code for the Q-table update.
- **Page 10 → Page 11:** Page 11 provides the JSON schema structure for the internal game report mentioned on page 10.
- **Page 11 → Page 12:** Page 12 contains the continuation of the JSON code block for the Inter-Group Bonus Game report.
- **Page 13 → Page 14:** Page 14 defines the specific components of the Dec-POMDP tuple introduced on page 13.
- **Page 14 → Page 15:** Page 15 details the specific rules for bonus point accumulation and calculation for the inter-group competition.
