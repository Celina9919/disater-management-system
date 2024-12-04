## ALGODAT <3
In this README.md, there are instructions on how to push/pull or any other common git commands that u might forget :) under these, there are also a brief idea on how the project will flow throughout the weeks :) .

---

# **Disaster Management Planning Tool for the City of Schilda**

## **Project Overview**
This project aims to create a disaster management tool for the city of Schilda. The tool is designed to assist in disaster preparedness and response by providing functionalities such as:
- Loading and visualizing the city map (B1).
- Modifying the city map for road closures or damages (B2).
- Planning evacuation routes (F2).
- Routing emergency services (F3).
- Setting up supply points (F4).
- Deploying emergency services effectively (F5).

The tool uses an adjacency matrix to represent the city map and integrates various algorithms for planning and decision-making.

---

## **Features**
- **Load and Display City Map** (B1): Visualize the city's road network.
- **Modify City Map** (B2): Simulate disaster scenarios like road closures or infrastructure damage.
- **Rebuild Communication Infrastructure** (F1): Identify and reconnect disconnected areas.
- **Plan Evacuation Routes** (F2): Compute safe and efficient evacuation paths.
- **Route Emergency Services** (F3): Optimize response times for emergency vehicles.
- **Set Up Supply Points** (F4): Strategically place supply points using clustering techniques.
- **Deploy Emergency Services** (F5): Allocate resources effectively during a disaster.

---

## **Getting Started**

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd algodat
   ```
   the cd algodat are based on our project name in GIT. 

2. To install any required Python libraries (if any):
   ```bash
   pip install 
   ```

---


## **Using Git for Version Control**

### Initialize a Repository
1. Create a new repository in GitLab and copy the repository URL.
2. Initialize Git in your project folder (if not already initialized):
   ```bash
   git init
   ```
3. Add the GitLab repository as the remote origin:
   ```bash
   git remote add origin <repository_url>
   ```

---

### Basic Git Commands

#### **1. Push Changes**
1. Add changes to the staging area:
   ```bash
   git add .
   ```
2. Commit the changes with a meaningful message:
   ```bash
   git commit -m "Describe the changes here"
   ```
3. Push the changes to the GitLab repository:
   ```bash
   git push origin main
   ```

#### **2. Pull Changes**
Before making changes, ensure your local copy is up to date:
   ```bash
   git pull origin main
   ```

#### **3. Check Repository Status**
View the status of your working directory and staged files:
   ```bash
   git status
   ```

#### **4. View Commit History**
See the commit history of the project:
   ```bash
   git log
   ```

#### **5. Create a New Branch**
For developing features or fixing bugs, create a separate branch:
   ```bash
   git checkout -b feature/new-feature-name
   ```

#### **6. Merge a Branch**
After developing in a branch, merge it back to the `main` branch:
   ```bash
   git checkout main
   git merge feature/new-feature-name
   ```

#### **7. Delete a Branch**
Remove an old or unnecessary branch:
   ```bash
   git branch -d feature/old-branch-name
   ```

---

## **Publishing the Project to GitLab**
1. After initializing Git and setting the remote:
   ```bash
   git push -u origin main
   ```
---


## **Understanding the Project**

### Objective:
To create a tool that helps city planners and emergency managers handle disasters efficiently by:
1. Visualizing the city map.
2. Simulating disaster scenarios (e.g., road closures, damaged areas).
3. Planning essential actions (e.g., evacuations, routing emergency services).

---

### Key Features:
The tool should:
1. **Load and Display City Map (B1):**
   - Read a city map from a file, represented as an adjacency matrix.
   - Display the map for reference.

2. **Modify City Map (B2):**
   - Allow updates like marking road closures and damaged areas.

3. **Functional Features (F1–F5):**
   - Rebuild communication infrastructure (F1).
   - Plan evacuation routes (F2).
   - Plan routes for emergency services (F3).
   - Set up supply points (F4).
   - Plan emergency service deployments (F5).

---

## **Project Structure**

The project should be modular for ease of development and testing. Here's a suggested structure:

### **1. Modules**
- **Data Management (City Map):**
  - Handles map input, storage, and modifications (B1, B2).
  
- **Disaster Planning Tools:**
  - Provides algorithms for F1–F5 features.
  
- **User Interface:**
  - A command-line or graphical interface for interacting with the tool.

### **2. Key Files and Directories**
```
/disaster_management_tool
    |-- main.py              # Entry point for the tool
    |-- data/
    |     |-- city_map.txt   # Adjacency matrix for the city map
    |-- modules/
    |     |-- city_map.py    # Functions for B1 and B2
    |     |-- planning.py    # Algorithms for F1–F5
    |-- tests/
    |     |-- test_city_map.py  # Tests for city_map.py
    |     |-- test_planning.py  # Tests for planning.py
    |-- requirements.txt     # List of dependencies (if any)
    |-- README.md            # Project description and usage instructions
```


## **Step-by-Step Plan **

### **Step 1: Implement Basic Features (B1 and B2)**
1. **B1: Load and Display City Map**
   - Develop a function to read the adjacency matrix from a file.
   - Test it with a sample matrix.

2. **B2: Modify City Map**
   - Add functionality to:
     - Mark roads as closed by setting weights to `-1` (or a large value like `9999` for inaccessible).
     - Highlight damaged areas.

---

### **Step 2: Add Functional Features (F1–F5)**
Each feature involves specific algorithms:

1. **F1: Rebuild Communication Infrastructure**
   - POSSIBLE SOLUTION : Use a graph traversal algorithm (DFS or BFS) to identify disconnected areas.
   

2. **F2: Plan Evacuation Routes**
   - Use a shortest path algorithm (Dijkstra maybe)
   - TAKE INTO ACCOUNT!!! --> Possible road closure(?)

3. **F3: Plan Routes for Emergency Services**
   - Similar to F2
   - TAKE INTO ACCOUNT!!! --> time taken to respond??? like how much time needed for the rescue service to go and help.

4. **F4: Set Up Supply Points**
   - idk yet

5. **F5: Plan Deployment of Emergency Services**
   - idk yet

---

### **Step 3: Documentation**
- everytime we finished a task, immediately do the documentation.

---

## **Implementation Plan**

Timeline:
1. **Week 1(5 Dec - 8 Dec) :**
   - Set up project structure.
   - Implement B1 (load and display city map).
   - Implement B2 (modify city map).


2. **Week 2(9 Dec- 15 Dec) :**
   - Finish B2 if not yet finished.
   - Start developing F1 (rebuild communication infrastructure).

3. **Week 3(16 Dec - 22 Dec) :**
   - Develop F2 and F3 (evacuation and emergency service routes).

4. **Week 4(23 Dec - 29 Dec) :**
   - Add F4 and F5 (supply points and deployments).

5. **Week 5(30 Dec  - 5 Jan) :**
   - Implement F4, F5 if not finished.
   - Test all features.
   - Finalize and document.

