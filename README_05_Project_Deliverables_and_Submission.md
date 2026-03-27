# Project Deliverables, Folder Structure, and Submission Guide

This README explains exactly what you are expected to submit for the **Social Media Engagement Analytics Pipeline** mini-project.

Read this file carefully before you submit your work.

The goal of this project is not only to write code. It is also to show that you can organize a small engineering project clearly and professionally.

In real workplaces, technical work is reviewed through:

* project structure
* file organization
* readability
* outputs
* documentation
* clear evidence that the pipeline actually works

This submission guide is designed to help you build those habits.

---

# Submission Goal

By the end of this mini-project, your repository should clearly show that you were able to:

* implement Spark foundations from **Day 1**
* apply DataFrame and Spark SQL processing from **Day 3**
* apply performance awareness and output optimization from **Day 4**
* organize your work in a structured project
* produce outputs that connect technical work to a real business use case

This is not a random folder of files.
It should feel like a small but real data engineering repository.

---

# What You Must Submit

You must submit **one complete GitHub repository** for this project.

Your repository must include:

## 1. The required README files

You must include all project README files:

* `README.md`
* `README_02_Phase1_Spark_Foundations_and_Raw_Data.md`
* `README_03_Phase2_Data_Processing_and_Analytics.md`
* `README_04_Phase3_Performance_and_Output_Optimization.md`
* `README_05_Project_Deliverables_and_Submission.md`
* `README_06_Reflections_and_Questions.md`

These README files are part of the deliverable, not extra optional files.

---

## 2. The Spark project code

Your repository must include the main Spark phase scripts:

* `src/phase1_raw_data_inspection.py`
* `src/phase2_transformations_and_analytics.py`
* `src/phase3_optimization_and_output.py`

If you create helper functions, you may also include:

* `src/utils.py`

### Why this matters

In real projects, reviewers must be able to find the actual implementation quickly and clearly.

---

## 3. The raw data folder structure

You must include the folder structure for the raw data:

```text id="j5r3rc"
data/raw/
```

### Important note

If your instructor has given permission, you may include the raw sample files.
If not, keep the folder structure and mention the expected files clearly.

Example expected raw files:

```text id="i8h66m"
data/raw/posts.csv
data/raw/engagement.csv
data/raw/users.csv
```

If the raw files are not included, your README or comments should clearly state what files are expected.

---

## 4. The processed output folders

Your repository must include the output folder structure created by the project.

At minimum, these folders should exist:

```text id="k4ctse"
data/processed/
data/output/csv/
data/output/parquet/
```

These folders show how your pipeline organizes intermediate and final outputs.

---

## 5. The final output files

Your repository should include the outputs produced by your pipeline where possible.

Examples include:

* category engagement summary
* creator engagement summary
* region engagement summary

Depending on your run, Spark may create folders containing part files rather than single visible CSV names. That is normal.

### Example expected output locations

```text id="u7r5wp"
data/output/csv/category_engagement_summary/
data/output/csv/creator_engagement_summary/
data/output/csv/region_engagement_summary/

data/output/parquet/category_engagement_summary/
data/output/parquet/creator_engagement_summary/
data/output/parquet/region_engagement_summary/
```

### Why this matters

A data pipeline should show its outputs.
If there is no output, it is difficult to prove that the pipeline actually worked.

---

## 6. SQL file for PostgreSQL-related work

Because this course uses **PostgreSQL**, your repository should include:

```text id="8x7kde"
sql/postgresql_reports.sql
```

This file can include:

* example table creation statements
* optional insert/load support
* reporting queries
* notes for how final Spark outputs could be loaded into PostgreSQL

### Important note

Even if you do not complete a full Spark-to-PostgreSQL load, you should still include a PostgreSQL-focused SQL file that reflects the final reporting side of the project.

---

## 7. Reflection answers

You must include your written answers and reflections.

Recommended file:

```text id="yxmxrk"
docs/checkpoint_answers.md
```

This file should contain:

* answers to the checkpoint questions
* reflections on the business use case
* explanations of technical choices
* explanations of performance decisions

This is very important because the project is not only about code.
It is also about showing understanding.

---

## 8. Optional screenshots or proof of execution

You may include:

```text id="0zm44m"
screenshots/
```

This folder can contain:

* terminal output
* Spark `show()` results
* schema output
* output folder screenshots
* PostgreSQL table screenshots if you loaded data there

### Why this helps

Screenshots are not always required, but they can strengthen your submission by showing clear evidence that the project was run successfully.

---

# Expected Project Structure

Your repository should follow a clear structure like this:

```text id="w0ipqr"
social-media-engagement-analytics/
│
├── README.md
├── README_02_Phase1_Spark_Foundations_and_Raw_Data.md
├── README_03_Phase2_Data_Processing_and_Analytics.md
├── README_04_Phase3_Performance_and_Output_Optimization.md
├── README_05_Project_Deliverables_and_Submission.md
├── README_06_Reflections_and_Questions.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
│       ├── csv/
│       └── parquet/
│
├── notebooks/
│
├── src/
│   ├── phase1_raw_data_inspection.py
│   ├── phase2_transformations_and_analytics.py
│   ├── phase3_optimization_and_output.py
│   └── utils.py
│
├── sql/
│   └── postgresql_reports.sql
│
├── docs/
│   └── checkpoint_answers.md
│
└── screenshots/
```

---

# Required Minimum Deliverables Checklist

Before submitting, make sure your repository contains all of the following.

## Required

* [ ] Main project README
* [ ] Phase 1 README
* [ ] Phase 2 README
* [ ] Phase 3 README
* [ ] Deliverables README
* [ ] Reflections README
* [ ] Phase 1 Spark script
* [ ] Phase 2 Spark script
* [ ] Phase 3 Spark script
* [ ] Output folders
* [ ] PostgreSQL SQL file
* [ ] Reflection / checkpoint answers file

## Strongly recommended

* [ ] Sample outputs saved in the repository
* [ ] Screenshots of execution
* [ ] Clean folder naming
* [ ] Clear comments in code

---

# What Your Code Should Show

Your code should clearly demonstrate the learning from the week.

## From Day 1

Your code should show:

* Spark session creation
* reading raw data
* schema inspection
* DataFrame awareness
* transformations vs actions awareness

## From Day 3

Your code should show:

* transformations
* filtering
* grouping
* aggregation
* Spark SQL
* optional UDF

## From Day 4

Your code should show:

* caching
* partition awareness
* repartition or coalesce
* Parquet output
* performance-aware thinking

---

# What Your Submission Should Feel Like

Your submission should feel like:

* a realistic junior data engineering project
* a guided but complete technical implementation
* a repository that another person can open and understand
* work that connects business questions to technical solutions

It should **not** feel like:

* random loose scripts
* code without explanation
* folders with no clear purpose
* outputs with no business meaning

---

# What Should Not Be Missing

Do not submit a project that is missing the following:

* the README structure
* the main Spark scripts
* processed outputs
* reflection answers
* PostgreSQL file
* evidence that the project connects to the social media business scenario

Those are all essential parts of the project.

---

# Naming Rules

Use clean and readable names.

## Recommended script names

* `phase1_raw_data_inspection.py`
* `phase2_transformations_and_analytics.py`
* `phase3_optimization_and_output.py`

## Recommended folder names

* `data/raw/`
* `data/processed/`
* `data/output/csv/`
* `data/output/parquet/`
* `docs/`
* `sql/`

Avoid unclear names like:

* `test.py`
* `finalfinal.py`
* `newscript2.py`
* `myprojectstuff.py`

Professional naming matters.

---

# GitHub Submission Instructions

## Step 1

Create your GitHub repository for the project.

## Step 2

Clone the repository locally.

## Step 3

Build your full project inside that repository.

## Step 4

Add your files:

```bash id="vlqcu4"
git add .
```

## Step 5

Commit your work:

```bash id="l3gdfg"
git commit -m "Complete Week 3 Spark mini-project"
```

## Step 6

Push your work:

```bash id="e13fyb"
git push origin main
```

---

# What Reviewers Will Look For

Your instructor or reviewer will likely look for:

* whether the repository is complete
* whether the README structure is followed
* whether the code runs logically
* whether the outputs exist
* whether Spark concepts from the week were implemented
* whether performance concepts were used correctly
* whether the technical work was explained in a business context

This means your project will not be judged only by whether it “runs.”
It will also be judged by clarity, structure, and understanding.

---

# Example of a Strong Submission

A strong submission would include:

* a clear social media business scenario
* three structured Spark scripts
* proper phase progression
* cleaned outputs
* CSV and Parquet outputs
* evidence of caching and partition-aware writing
* a PostgreSQL reporting SQL file
* thoughtful reflection answers
* a clean GitHub repository structure

---

# Example of a Weak Submission

A weak submission would look like:

* only one script with everything mixed together
* missing README files
* no outputs saved
* no explanation of Parquet or caching
* no reflections
* no PostgreSQL connection to the business workflow
* code that looks disconnected from the scenario

---

# Final Pre-Submission Checklist

Before submitting, ask yourself:

* Did I include all README files?
* Did I implement all three phases?
* Did I reflect Days 1, 3, and 4?
* Did I include Spark outputs?
* Did I explain performance choices?
* Did I include PostgreSQL-related deliverables?
* Does my repository look professional and organized?

If the answer is yes to all of these, your submission is in a strong position.

---

# Final Note

This project is meant to feel like real work.

In real data engineering teams, it is not enough to say:

> “My code runs.”

You also need to show:

* what problem you solved
* how you structured the project
* what outputs you produced
* how your work supports the business
* why your engineering decisions make sense

That is exactly what this submission structure is helping you practice.

---

# Next Step

Continue to:

**`README_06_Reflections_and_Questions.md`**

In the final README, you will answer reflection questions about the business use case, the Spark pipeline, the transformations, and the performance decisions you made throughout the project.
