# Algorithms and Data Structures: Grazioso Salvare Rescue Dog Dashboard (Python, Dash, MongoDB)
This repository contains the original and enhanced versions of my Grazioso Salvare Rescue Dog Dashboard. The artifact began as a CS-340 Client/Server Development project built in a Jupyter Notebook using a single anchored regex pattern to filter dogs by breed. Because the original implementation only supported exact matches, mixed breeds were excluded and the dashboard could not as accurately reflect the dataset.

## Overview
For this enhancement, I migrated the dashboard from a Jupyter Notebook to a standalone Python script to ensure consistent execution and proper rendering of the Dash interface. Running the project outside of Jupyter resolved issues with embedded output, restored the intended layout, and provided a stable environment for further algorithmic improvements.

The core enhancement was the redesign of the breed‑matching logic into a dual‑mode filtering algorithm. A new dropdown allows users to switch between **Strict Mode** (anchored regex for exact matches) and **Expanded Mode** (unanchored regex for partial matches). This design required analyzing how MongoDB executes regex queries, understanding the time‑complexity differences between anchored and unanchored patterns, and balancing accuracy with performance. Anchored patterns reduce the search space and behave closer to O(n), while unanchored patterns can approach worst‑case O(n·m) depending on pattern length. I also evaluated the memory implications of returning larger result sets in Expanded Mode and designed the algorithm to handle these tradeoffs predictably.

To support the new filtering model, I added a `dcc.Store` component to preserve the last selected rescue type. This resolved UI conflicts where changing the dropdown would reset the dashboard to “All Animals.” The dropdown now resets to Strict Mode when switching rescue categories, ensuring consistent and intuitive behavior. I validated the algorithm by comparing results directly in the DataTable and confirming that differences between Strict and Expanded modes aligned with the underlying dataset.

## Key Improvements
- Migration from Jupyter Notebook to a standalone Python/Dash application
- Dual‑mode breed‑matching algorithm using anchored and unanchored regex
- Analysis of MongoDB regex execution and associated time‑complexity tradeoffs
- Improved UI state management using `dcc.Store` for predictable filtering behavior
- More accurate and inclusive breed filtering, especially for mixed breeds
- Stable Flask‑based execution environment independent of Jupyter

## Repository Structure
`/original`
The initial Jupyter Notebook implementation from CS‑340 Client/Server Development

`/enhanced`
Standalone Python/Dash application with dual‑mode breed‑matching algorithm

`/zips`
Full project ZIPs for SNHU submission (original and enhanced)

## Related Artifacts
Additional documentation, narrative, and demo video for this enhancement are available in my ePortfolio: https://sarahhayduk.github.io/

## Technologies Used
- Python
- Dash / Plotly
- MongoDB
- Flask

This enhancement demonstrates my ability to design and evaluate computing solutions using algorithmic principles while managing real‑world tradeoffs. The dual‑mode regex model reflects thoughtful analysis of time complexity, memory behavior, and data‑driven filtering accuracy. It also highlights my ability to refactor academic prototypes into stable, maintainable, and user‑friendly applications.
