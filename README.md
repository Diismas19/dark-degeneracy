# Dark Degeneracy

[![arXiv](https://img.shields.io/badge/arXiv-2508.17955-b31b1b.svg)](https://arxiv.org/abs/2508.17955)

This repository contains the data and code used in the cosmology research paper "Dark Degeneracy". The project was developed by Vitor Petri, Valerio Marra, and Rodrigo von Marttens.

Here you will find the Markov Chain Monte Carlo (MCMC) chains generated using `cobaya`, the `.yaml` configuration files used for sampling, and the necessary modifications to the `CLASS` code to replicate our results.

## Citation

If you use this code or data in your research, please cite our paper:

```bibtex
% Adicione aqui a entrada BibTeX do seu artigo quando estiver disponível no INSPIRE-HEP ou similar.
@article{Petri:2025,
    author = "Petri, Vitor and Marra, Valerio and von Marttens, Rodrigo",
    title = "{Dark Degeneracy in DESI DR2: Interacting or Evolving Dark Energy?}",
    eprint = "2508.17955",
    archivePrefix = "arXiv",
    primaryClass = "astro-ph.CO",
    month = "8",
    year = "2025"
}
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:
* Python 3.8+
* `pip` and `venv` (or `conda`)
* A C compiler (e.g., `gcc`)
* `git`

## Installation and Setup

Follow these steps to set up the environment and all necessary packages to reproduce our analysis.

### 1. Create a Virtual Environment

It is highly recommended to work within a virtual environment.

* **Using `venv`:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* **Using `conda`:**
    ```bash
    conda create -n dark_degeneracy python=3.9
    conda activate dark_degeneracy
    ```

### 2. Install Cobaya and Cosmological Codes

First, install `cobaya` and the required cosmological packages.

```bash
# Install Cobaya
pip install cobaya

# Install the standard cosmological code support for Cobaya
cobaya-install cosmo -p /path/to/your/install/dir
```
For more details, follow the official `cobaya` [cosmology installation guide](https://cobaya.readthedocs.io/en/latest/installation_cosmo.html).

### 3. Install the ACT DR6 Likelihood

The Atacama Cosmology Telescope (ACT) DR6 likelihood is required for our analysis but is not installed by default.

```bash
# Install the likelihood package
pip install act_dr6_lenslike

# Register it with Cobaya
cobaya-install act_dr6_lenslike
```

### 4. Prepare the Modified CLASS Code

Our model requires modifications to the standard `CLASS` Boltzmann code. Follow the steps below.

**4.1. Clone and Navigate:**
```bash
git clone github.com/lesgourg/class_public.git
cd class_public
git checkout <commit_hash_or_tag> # Use the same version as above
```

**4.2. Edit `include/background.h`:**
In the `struct background`, add the new `w0_int` and `wa_int` parameters.
```c
/* ... (conteúdo existente) ... */
struct background {
  /* ... (variáveis existentes) ... */
  double w0_int;
  double wa_int;
  /* ... (resto do struct) ... */
};
```

**4.3. Edit `source/input.c`:**
-   Add the lines to read the new parameters from configuration files. Find the section `/* 7) ADDITIONAL SPECIES */` and add below it:
    ```c
    class_read_double("w0_int",pba->w0_int);
    class_read_double("wa_int",pba->wa_int);
    ```
-   Set default values for these parameters inside the `input_default_params` function:
    ```c
    pba->w0_int = -1.;
    pba->wa_int = 0.;
    ```

**4.4. Edit `source/background.c`:**
Modify the evolution equations for Cold Dark Matter (`rho_cdm`) and Dark Energy (`rho_lambda`).
-   Replace the line for `pvecback[pba->index_bg_rho_cdm]` with:
    ```c
    pvecback[pba->index_bg_rho_cdm] = (pba->Omega0_cdm * pow(pba->H0,2)
      + pba->Omega0_lambda*pow(pba->H0,2)*(1+pba->w0_int+pba->wa_int*(1-a))
      * exp(-3*pba->wa_int*(1-a))*pow(a,-3*(pba->w0_int+pba->wa_int))) / pow(a,3);
    ```
-   Replace the line for `pvecback[pba->index_bg_rho_lambda]` with:
    ```c
    pvecback[pba->index_bg_rho_lambda] = -pba->Omega0_lambda*pow(pba->H0,2)*(pba->w0_int+pba->wa_int*(1-a))
      * exp(-3*pba->wa_int*(1-a))*pow(a,-3*(1+pba->w0_int+pba->wa_int));
    ```

**4.5. Edit `source/perturbations.c`:**
Modify the CDM perturbation equation for `dy[pv->index_pt_delta_cdm]`.
```c
dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity)+(a/pvecback[pba->index_bg_rho_cdm])
  * (metric_euler/k2-y[pv->index_pt_delta_cdm])*3*(3*pba->w0_int*(1+pba->w0_int)+pba->wa_int*(3+6*pba->w0_int-2*a*(1+3*pba->w0_int))+3*pow(pba->wa_int,2)*pow(1-a,2))
  * ((pba->Omega0_cdm/pba->Omega0_lambda)*pow(a,3*(pba->w0_int+pba->wa_int))+exp(-3*pba->wa_int*(1-a)))
  / (3*(pba->w0_int+pba->wa_int*(1-a))*((pba->Omega0_cdm/pba->Omega0_lambda)*pow(a,3*(pba->w0_int+pba->wa_int))+(1+pba->w0_int+pba->wa_int*(1-a))*exp(-3*pba->wa_int*(1-a))))*pvecback[pba->index_bg_H]
  * ((pvecback[pba->index_bg_rho_cdm]*pvecback[pba->index_bg_rho_lambda])/(pvecback[pba->index_bg_rho_cdm]+pvecback[pba->index_bg_rho_lambda]));
```

**4.6. Install the Modified Code:**
```bash
pip install .
```
---

## How to Reproduce Our Results

With the environment fully configured, you can now run the MCMC analysis using the provided `.yaml` files.

For example, to run the main analysis:
```bash
cobaya-run your_analysis_file.yaml
```

The resulting chains and data products will be stored in the directory specified within the `.yaml` file.
