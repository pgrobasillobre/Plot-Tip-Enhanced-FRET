## Objective

The goal of this code is to reproduce **Figure 1d** from the paper: https://doi.org/10.1038/s41565-022-01142-z.

This code reads fluorescence descriptors (absorption coefficient, radiative decay rate, and non-radiative decay rate), and the electronic energy transfer rates of two phthalocyanine molecules:
- **Donor**: Pt-Pc
- **Acceptor**: Zn-Pc

## Description

In Figure 1d, the Pt-Pc and Zn-Pc molecular distance is fixed, and the microscope tip is placed in three positions on top of the donor molecule (referred to as **positions 4, 5, and 6**). This code plots the tip-mediated fluorescence of both molecules at these three positions.

### Data Sources

- Fluorescence descriptors are computed using **Time-Dependent Density Functional Theory (TDDFT)** with the **Amsterdam Modeling Suite**.
  - Reference: https://doi.org/10.1039/D4NA00080C

- Electronic energy transfer rates are computed using the **FretLab** code:
  - Repository: https://github.com/pgrobasillobre/FretLab

## Usage

Run the main script located at:
```
different-tip-position/__main__.py
```

### Required Arguments (to be modified within __main__.py)

- **Path to the results folder**
- **Names of the folders for different tip positions**
- **Number of states to consider** (e.g., 2 degenerate states per molecule)

## Folder Structure

An example of a results folder is given in example-results/different-tip-position

```
results/
├── tddft/
│   ├── state-1/
│   │   └── pos-4/5/6/  # Contains TDDFT results: radiative, non-radiative decay rates, absorption coefficient
│   └── state-2/
│       └── pos-4/5/6/
├── fret/
    ├── D_state-1_to_A_state-1/
    ├── D_state-1_to_A_state-2/
    ├── D_state-2_to_A_state-1/
    └── D_state-2_to_A_state-2/  # FretLab calculation outputs: electronic energy transfer rates
```

## Output

- A plot showing the globally normalized total fluorescence intensity of the donor-acceptor pair mediated by the nanoparticle.


