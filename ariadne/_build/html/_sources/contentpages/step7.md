# STEP 7: Data analysis

Classically, this step overlaps with Step 6. Initial data analysis refers to the process of data inspection and reorganization that needs to be carried out before formal statistical analyses (Hueber et al., 2016). This process includes metadata setup, data cleaning/screening/refining, updating the research analysis plan, and the documentation of initial data analysis procedures (see Baillie et al., 2022). Ideally, the data analysis procedure for the current project has been thoroughly planned and fixed in advance during Step 3 as part of a preregistration or Registered Report. But even then, many new decisions have to be made at this stage, which may affect the next steps, e.g., how the data can be best shared with others or how results are best visualized (Kroon et al., 2022). Choosing the right analysis framework one feels comfortable with is just one of the many challenges in this step (➜ [RStudio](https://posit.co/), ➜ [JASP](https://jasp-stats.org/) or ➜ [Jupyter Notebook](https://jupyter.org/)). Statistical approaches that are suitable for the research question need to be chosen (e.g., Bayesian versus frequentist statistics; Pek & Van Zandt, 2020; van Zyl, 2018). If applicable, correction methods for multiple comparisons should be considered (Alberton et al., 2020; Noble, 2009), to avoid a potential increase in _Type I error rate_ (see Table 1). In the processing of analyzing results, it is essential to consider the role of visualizations. Effective visual representations can enhance the comprehension of complex data sets and findings (➜ [BioRender](https://www.biorender.com/); ➜ [Mermaid](https://mermaid.js.org/); ➜ [Nipype](https://nipype.readthedocs.io/en/latest/)). Crucially, in recent times, there has been a shift in the focus of group-level to individual trajectory analyses, which has a significant impact on the required sample size and the effect size (Marek et al., 2022). To overcome inherent inaccuracies associated with estimating effect sizes, sequential analyses involve monitoring data collection as it progresses and controlling for Type 1 error rate (Lakens, 2014). At a predetermined stage in the project (e.g., defined in Step 2), an interim analysis can be conducted to determine whether the collected data provide sufficient evidence to conclude that an effect is present, whether more data should be gathered, or whether the study should be terminated if the predicted effect is unlikely to be observed (Lakens, 2014). Of note, data analysis is a critical step that has attracted much attention recently in light of the so-called “replicability crisis” (Anvari & Lakens, 2018), as this is a stage where questionable research practices (John et al., 2012) and biases may occur (even inadvertently).