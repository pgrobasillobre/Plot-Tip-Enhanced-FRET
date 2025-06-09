# Tip-Enhanced FRET Spectra

## Objective

The goal of this repository is to reproduce **Figure 1d** from the paper:
**Kong, FF., Tian, XJ., Zhang, Y. et al.**
**Wavelike electronic energy transfer in donor–acceptor molecular systems through quantum coherence**
*Nat. Nanotechnol. 17, 729–736 (2022)*
[https://doi.org/10.1038/s41565-022-01142-z](https://doi.org/10.1038/s41565-022-01142-z)

---

## Description

This code reads **fluorescence descriptors**—including the absorption coefficient, radiative decay rate, and non-radiative decay rate—computed at the **Time-Dependent Density Functional Theory (TDDFT)** level. It also uses **electronic energy transfer rates** between two phthalocyanine molecules, calculated using **FretLab**.

Below is a schematic of the donor–acceptor molecules:

<img src="./_static/molecules_labels.png" alt="Molecule Labels" width="400"/>


The simulation models **tip-mediated fluorescence spectra** where a silver tip is positioned near the donor molecule at three locations (A, B, and C). The donor and acceptor are placed **2.21 nm** apart, while the tip is located **0.5 nm** away from the nearest donor atom.

![Tip Positions](./_static/tip-positions.png)

Simulated spectra for each tip position are compared to experimental data. All spectra are normalized to the **maximum simulated fluorescence intensity**.

---

## Data Sources

- **Fluorescence descriptors (TDDFT)**:
  - Computed using **Amsterdam Modeling Suite**
  - Reference:
    **P. Grobas Illobre**, P. Lafiosca, T. Guidone, F. Mazza, T. Giovannini, C. Cappelli
    *Nanoscale Adv., 2024, 6, 3410*
    [https://doi.org/10.1039/D4NA00080C](https://doi.org/10.1039/D4NA00080C)

- **Electronic energy transfer rates (FretLab)**:
  - Repository: [https://github.com/pgrobasillobre/FretLab](https://github.com/pgrobasillobre/FretLab)

---

## Usage

An example simulation is provided in the `data/simulation/` directory. Ensure the following folder structure:

```
simulation/
├── tddft/
│   ├── state-1/
│   │   └── pos-4/5/6/
│   └── state-2/
│       └── pos-4/5/6/
├── fret/
│   ├── D_state-1_to_A_state-1/
│   ├── D_state-1_to_A_state-2/
│   ├── D_state-2_to_A_state-1/
│   └── D_state-2_to_A_state-2/
```

### Run the script:

```bash
python3 Plot-Tip-Enhanced-FRET-change-tip-position
```

---

## Output

The script generates the following figure comparing experimental and simulated spectra for different tip positions:

![FRET Comparison](./_static/fret_tip-position_experiment_vs_simulation.png)


## License

This code is licensed under the **GNU General Public License v3.0**.

## Funding

Development of this code has been supported by the FARE 2020 program — “Framework per l’attrazione e il rafforzamento delle eccellenze per la ricerca in Italia.”

## Contact

- Email: **pgrobasillobre@gmail.com**
