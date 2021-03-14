# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: ExecuteTime,autoscroll,heading_collapsed,hidden,slideshow,title,-hide_ouput,-code_folding
#     cell_metadata_json: true
#     formats: ipynb,py:percent
#     notebook_metadata_filter: all
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.10.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.8.8
#   latex_envs:
#     LaTeX_envs_menu_present: true
#     autoclose: false
#     autocomplete: false
#     bibliofile: biblio.bib
#     cite_by: apalike
#     current_citInitial: 1
#     eqLabelWithNumbers: true
#     eqNumInitial: 1
#     hotkeys:
#       equation: Ctrl-E
#       itemize: Ctrl-I
#     labels_anchors: false
#     latex_user_defs: false
#     report_style_numbering: false
#     user_envs_cfg: false
# ---

# %% [markdown]
# # Theoretical Foundations of Buffer Stock Saving
#
# <cite data-cite="6202365/8AH9AXN2"></cite>
#
# <p style="text-align: center;"><small><small><small>Generator: BufferStockTheory-make/notebooks_byname</small></small></small></p>
#
# [![econ-ark.org](https://img.shields.io/badge/Powered%20by-Econ--ARK-3e8acc.svg)](https://econ-ark.org/materials/BufferStockTheory)
#

# %% [markdown]
# <a id='interactive-dashboard'></a>
#
# [This notebook](https://econ-ark.org/BufferStockTheory/#launch) uses the [Econ-ARK/HARK](https://github.com/econ-ark/HARK) toolkit to reproduce and illustrate key results of the paper [Theoretical Foundations of Buffer Stock Saving](http://econ-ark.github.io/BufferStockTheory/BufferStockTheory).
#
# #### An [interactive dashboard](https://econ-ark.org/BufferStockStockTheory/#Dashboard) allows you to modify parameters to see how the figures change.
#

# %%
# This cell does some setup

# Import related generic python packages
from HARK.ConsumptionSaving.ConsIndShockModel import PerfForesightConsumerType
from copy import copy
from HARK.ConsumptionSaving.ConsIndShockModel import init_idiosyncratic_shocks as base_params
from HARK.utilities import plot_funcs, plot_funcs_der
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType
from HARK.utilities import find_gui, make_figs, determine_platform, test_latex_installation, setup_latex_env_notebook
import HARK
import numpy as np
from copy import deepcopy

# Plotting tools
import matplotlib.pyplot as plt

# Ignore some harmless but alarming warning messages
import warnings
warnings.filterwarnings("ignore")

# Code to allow a master "Generator" and derived "Generated" versions
#   - allows "$nb-Problems-And-Solutions → $nb-Problems → $nb"
Generator = True  # Is this notebook the master or is it generated?

# Whether to save the figures to Figures_dir
saveFigs = True

# Whether to draw the figures
drawFigs = True

if HARK.__version__ < '0.10.8':
    raise ImportError(
        'This notebook requires at least econ-ark v0.10.8,  please update your installation pip install -U econ-ark or conda install -c conda-forge econ-ark')

pf = determine_platform()
try:
    latexExists = test_latex_installation(pf)
except ImportError:  # windows and MacOS requires manual install
    latexExists = False

setup_latex_env_notebook(pf, latexExists)

# check if GUI is present if not then switch drawFigs to False and force saveFigs to be True
if not find_gui():
    drawFigs = False
    saveFigs = True

# Font sizes for figures
fssml=18
fsmid=22
fsbig=26

# this can be removed if we pass in saveFigs and drawFigs in every call to make('figure')
def make(figure_name, target_dir="../../Figures"):
    make_figs(figure_name, saveFigs, drawFigs, target_dir)

# %% [markdown]
# ## [The Problem](http://econ-ark.github.io/BufferStockTheory/BufferStockTheory/#The-Problem)
#
# The paper defines and calibrates a small set of parameters:
#
# | Parameter | Description | Code | Value |
# |:---:| ---         | ---  | :---: |
# | $\Gamma$ | Permanent Income Growth Factor | $\texttt{PermGroFac}$ | 1.03 |
# | $\mathsf{R}$ | Interest Factor | $\texttt{Rfree}$ | 1.04 |
# | $\beta$ | Time Preference Factor | $\texttt{DiscFac}$ | 0.96 |
# | $\rho$ | Coeﬃcient of Relative Risk Aversion| $\texttt{CRRA}$ | 2 |
# | $\wp$ | Probability of Unemployment | $\texttt{UnempPrb}$ | 0.005 |
# | $\theta^{\large u}$ | Income when Unemployed | $\texttt{IncUnemp}$ | 0. |
# | $\sigma_\psi$ | Std Dev of Log Permanent Shock| $\texttt{PermShkStd}$ | 0.1 |
# | $\sigma_\theta$ | Std Dev of Log Transitory Shock| $\texttt{TranShkStd}$ | 0.1 |
#
# that define the preferences and environment of microeconomic consumers as detailed below.
#
# The objective of such a consumer with a horizon of $n$ periods is to maximize the value obtained from the stream of consumption __**c**__ from period $t=T-n$ to a terminal period $T$:
#
# \begin{equation}
# \mathbf{v}_{t} = \sum_{i=0}^{n} \beta^{n}\mathrm{u}(\mathbf{c}_{t+n})
# \end{equation}
#
# The infinite-horizon solution to the model is defined as the limit of the solution in the first period of life $\mathrm{c}_{T-n}$ as the horizon $n$ goes to infinity.

# %% [markdown]
# ### Details
# For a microeconomic consumer who begins period $t$ with __**m**__arket resources boldface $\mathbf{m}_{t}$ (=net worth plus current income), the amount that remains after __**c**__onsumption of $\mathbf{c}_{t}$ will be end-of-period __**a**__ssets $\mathbf{a}_{t}$,
#
# <!-- Next period's 'Balances' $B_{t+1}$ reflect this period's $\mathbf{a}_{t}$ augmented by return factor $R$:-->

# %% [markdown]
# \begin{eqnarray}
# \mathbf{a}_{t}   &=&\mathbf{m}_{t}-\mathbf{c}_{t}. \notag
# \end{eqnarray}
#
# The consumer's __**p**__ermanent noncapital income $\mathbf{p}$ grows by a predictable factor $\Gamma$ and is subject to an unpredictable multiplicative shock $\mathbb{E}_{t}[\psi_{t+1}]=1$,
#
# \begin{eqnarray}
# \mathbf{p}_{t+1} & = & \mathbf{p}_{t} \Gamma \psi_{t+1}, \notag
# \end{eqnarray}
#
# and, if the consumer is employed, actual income is permanent income multiplied by a transitory shock $\theta^{\large e}$.  There is also a probability $\wp$ that the consumer will be temporarily unemployed and experience income of $\theta^{\large u}  = 0$.  We construct $\theta^{\large e}$ so that its mean value is $1/(1-\wp)$ because in that case the mean level of the transitory shock (accounting for both unemployed and employed states) is exactly
#
# \begin{eqnarray}
# \mathbb{E}_{t}[\theta_{t+1}] & = & \theta^{\large{u}}  \times \wp + (1-\wp) \times \mathbb{E}_{t}[\theta^{\large{e}}_{t+1}] \notag
# \\ & = & 0 \times \wp + (1-\wp) \times 1/(1-\wp)  \notag
# \\ & = & 1. \notag
# \end{eqnarray}
#
#   We can combine the unemployment shock $\theta^{\large u}$ and the transitory shock to employment income $\theta^{\large e}$ into $\theta _{t+1}$, so that next period's market resources are
# \begin{eqnarray}
#     \mathbf{m}_{t+1} &=& \mathbf{a}_{t}\mathsf{R} +\mathbf{p}_{t+1}\theta_{t+1}.  \notag
# \end{eqnarray}

# %% [markdown]
# When the consumer has a CRRA utility function $u(\mathbf{c})=\frac{\mathbf{c}^{1-\rho}}{1-\rho}$, the paper shows that the problem can be written in terms of ratios (nonbold font) of level (bold font) variables to permanent income, e.g. $m_{t} \equiv \mathbf{m}_{t}/\mathbf{p}_{t}$, and the Bellman form of [the problem reduces to](https://econ-ark.github.io/BufferStockTheory/#The-Related-Problem):
#
# \begin{eqnarray*}
# v_t(m_t) &=& \max_{c_t}~~ u(c_t) + \beta~\mathbb{E}_{t} [(\Gamma\psi_{t+1})^{1-\rho} v_{t+1}(m_{t+1}) ] \\
# & s.t. & \\
# a_t &=& m_t - c_t \\
# m_{t+1} &=& a_t \mathsf{R}/(\Gamma \psi_{t+1}) + \theta_{t+1} \\
# \end{eqnarray*}

# %%
# Define a dictionary with baseline parameter values

# Import default parameter values (init_idiosyncratic_shock)
from HARK.ConsumptionSaving.ConsIndShockModel import init_idiosyncratic_shocks as base_params

# Set the parameters for the baseline results in the paper
# using the variable names defined in the cell above
base_params['PermGroFac'] = [1.03]  # Permanent income growth factor
base_params['Rfree']      = Rfree = 1.04  # Interest factor on assets
base_params['DiscFac']    = DiscFac = 0.96  # Time Preference Factor
base_params['CRRA']       = CRRA = 2.00  # Coefficient of relative risk aversion
# Probability of unemployment (e.g. Probability of Zero Income in the paper)
base_params['UnempPrb']   = UnempPrb = 0.005
base_params['IncUnemp']   = IncUnemp = 0.0   # Induces natural borrowing constraint
base_params['PermShkStd'] = [0.1]   # Standard deviation of log permanent income shocks
base_params['TranShkStd'] = [0.1]   # Standard deviation of log transitory income shocks
# %%
# Uninteresting housekeeping and details
# Make global variables for the things that were lists above -- uninteresting housekeeping
PermGroFac, PermShkStd, TranShkStd = base_params['PermGroFac'][0], base_params['PermShkStd'][0], base_params['TranShkStd'][0]

# Some technical settings that are not interesting for our purposes
base_params['LivPrb']      = [1.0]   # 100 percent probability of living to next period
base_params['CubicBool']   = True    # Use cubic spline interpolation
base_params['T_cycle']     = 1       # No 'seasonal' cycles
base_params['BoroCnstArt'] = None    # No artificial borrowing constraint
# %% [markdown]
# ## Convergence of the Consumption Rules
#
# Under the given parameter values, [the paper's first figure](https://econ-ark.github.io/BufferStockTheory/#Convergence-of-the-Consumption-Rules) depicts the successive consumption rules that apply in the last period of life $(c_{T}(m))$, the second-to-last period, and earlier periods $(c_{T-n})$.  The consumption function to which these converge is $c(m)$:
#
# $$
# c(m) = \lim_{n \uparrow \infty} c_{T-n}(m) \notag
# $$
#

# %%
# Create a buffer stock consumer instance by invoking the IndShockConsumerType class
# with the built-in parameter dictionary "base_params"

# Construct finite horizon agent with baseline parameters
baseAgent_Fin = IndShockConsumerType(**base_params)
baseAgent_Fin.cycles = 100   # Set finite horizon (T = 100)

baseAgent_Fin.solve(verbose=0)        # Solve the model
baseAgent_Fin.unpack('cFunc')  # Make the consumption function easily accessible


# %%
# Plot the different consumption rules for the different periods

mPlotMin = 0
mLocCLabels = 9.6  # Defines horizontal limit of figure
mPlotTop = 6.5    # Defines maximum m value where functions are plotted
mPts = 1000      # Number of points at which functions are evaluated

mBelwLabels = np.linspace(mPlotMin, mLocCLabels-0.1, mPts)  # Range of m below loc of labels
m_FullRange = np.linspace(mPlotMin, mPlotTop, mPts)        # Full plot range
# c_Tm0  defines the last period consumption rule (c=m)
c_Tm0 = m_FullRange
# c_Tm1 defines the second-to-last period consumption rule
c_Tm1 = baseAgent_Fin.cFunc[-2](mBelwLabels)
c_Tm5 = baseAgent_Fin.cFunc[-6](mBelwLabels)  # c_Tm5 defines the T-5 period consumption rule
c_Tm10 = baseAgent_Fin.cFunc[-11](mBelwLabels)  # c_Tm10 defines the T-10 period consumption rule
# c_Limt defines limiting inﬁnite-horizon consumption rule
c_Limt = baseAgent_Fin.cFunc[0](mBelwLabels)
plt.figure(figsize=(12, 9))
plt.plot(mBelwLabels, c_Limt, color="black")
plt.plot(mBelwLabels, c_Tm1, color="black")
plt.plot(mBelwLabels, c_Tm5, color="black")
plt.plot(mBelwLabels, c_Tm10, color="black")
plt.plot(m_FullRange, c_Tm0, color="black")
plt.xlim(0, 11)
plt.ylim(0, 7)
plt.text(7.0, 6.0, r'$c_{T   }(m) = 45$ degree line', fontsize=22, fontweight='bold')
plt.text(mLocCLabels, 5.3, r'$c_{T-1 }(m)$', fontsize=22, fontweight='bold')
plt.text(mLocCLabels, 2.6, r'$c_{T-5 }(m)$', fontsize=22, fontweight='bold')
plt.text(mLocCLabels, 2.1, r'$c_{T-10}(m)$', fontsize=22, fontweight='bold')
plt.text(mLocCLabels, 1.7, r'$c(m)       $', fontsize=22, fontweight='bold')
plt.arrow(6.9, 6.05, -0.6, 0, head_width=0.1, width=0.001,
          facecolor='black', length_includes_head='True')
plt.tick_params(labelbottom=False, labelleft=False, left='off',
                right='off', bottom='off', top='off')
plt.text(0, 7.05, "$c$", fontsize=26)
plt.text(11.1, 0, "$m$", fontsize=26)
# Save the figures in several formats

make('cFuncsConverge')  # Comment out if you want to run uninterrupted

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# Use the [interactive dashboard](#interactive-dashboard) to explore the effects of changes in patience, risk aversion, or risk

# %% [markdown]
# ## Factors and Conditions
#
# ### [The Finite Human Wealth Condition](http://econ-ark.github.io/BufferStockTheory/#Human-Wealth)
#
# Human wealth for a perfect foresight consumer is the present discounted value of future income:
#
# \begin{eqnarray}\notag
# \mathbf{h}_{t} & = & \mathbb{E}_{t}[\mathbf{p}_{t} + \mathsf{R}^{-1} \mathbf{p}_{t+1} + \mathsf{R}^{2} \mathbf{p}_{t+2} ... ] \\ \notag
#       & = & \mathbf{p}_{t} \left(1 + (\Gamma/\mathsf{R}) + (\Gamma/\mathsf{R})^{2} ... \right)
# \end{eqnarray}
# which approaches infinity as the horizon extends if $\Gamma/\mathsf{R} \geq 1$.  We say that the 'Finite Human Wealth Condition' [(FHWC)](https://econ-ark.github.io/BufferStockTheory/#FHWC) holds if
# $0 \leq (\Gamma/\mathsf{R}) < 1$.

# %% [markdown]
# ### [Absolute Patience and the AIC](https://econ-ark.github.io/BufferStockTheory/#AIC)
#
# The paper defines the Absolute Patience Factor [(APF)](https://econ-ark.github.io/BufferStockTheory/#APF) as being equal to the ratio $\mathbf{c}_{t+1}/\mathbf{c}_{t}$ for a perfect foresight consumer.  The Old English character <span style="font-size:larger;">"&#222;"</span> used for this object in the paper cannot currently be rendered conveniently in Jupyter notebooks, so we will substitute $\Phi$ here:
#
# \begin{equation}
# \Phi = (\mathsf{R} \beta)^{1/\rho}
# \end{equation}
#
# If $\Phi = 1$, a perfect foresight consumer will spend at exactly the level of $\mathbf{c}$ that can be sustained perpetually (given their current and future resources).  If $\Phi < 1$ (the consumer is 'absolutely impatient'; or, 'the absolute impatience condition holds'), the consumer is consuming more than the sustainable amount, so consumption will fall, and if the consumer is 'absolutely patient' with $\Phi > 1$ consumption will grow over time.
#
#

# %% [markdown]
# ### [Growth Patience and the GICRaw](https://econ-ark.github.io/BufferStockTheory/#GIC)
#
# For a [perfect foresight consumer](https://www.econ2.jhu.edu/people/ccarroll/public/lecturenotes/consumption/PerfForesightCRRA), whether the ratio $c$=__**c**__/__**p**__ is rising, constant, or falling depends on the relative growth rates of consumption and permanent income; that ratio is measured by the [Perfect Foresight Growth Patience Factor](https://econ-ark.github.io/BufferStockTheory/#PFGPF):
#
# \begin{eqnarray}
# \Phi_{\Gamma} & = & \Phi/\Gamma
# \end{eqnarray}
# and whether the $c$ is falling or rising over time depends on whether $\Phi_{\Gamma}$ is below or above 1.
#
# An analogous condition can be defined when there is uncertainty about permanent income.  Defining $\tilde{\Gamma} = (\mathbb{E}[\psi^{-1}])^{-1}\Gamma$, the 'Growth Impatience Condition' [(GICRaw)](https://econ-ark.github.io/BufferStockTheory/#GIC) determines whether, \textit{in expectation}, the stochastic value of $c$ is rising, constant, or falling over time:
# \begin{eqnarray}
#   \Phi/\tilde{\Gamma} & < & 1
# \end{eqnarray}

# %% [markdown]
# ### [The Finite Value of Autarky Condition (FVAC)](https://econ-ark.github.io/BufferStockTheory/#Autarky-Value)


# %% [markdown]
# The paper [shows](https://econ-ark.github.io/BufferStockTheory/#Autarky-Value) that a consumer who planned to spend his permanent income $\{ \mathbf{p}_{t}, \mathbf{p}_{t+1}, ...\} $ in every period would have value defined by
#
# \begin{equation*}
# \mathbf{v}_{t}^{\text{autarky}} = u(\mathbf{p}_{t})\left(\frac{1}{1-\beta \Gamma^{1-\rho} \mathbb{E}[\psi^{1-\rho}]}\right)
# \end{equation*}
#
# and defines the 'Finite Value of Autarky Condition' as the requirement that the denominator be a positive finite number:
#
# \begin{equation*}
# \beta \Gamma^{1-\rho} \mathbb{E}[\psi^{1-\rho}] < 1
# \end{equation*}

# %% [markdown]
# ### [The Weak Return Impatience Condition (WRIC)](https://econ-ark.github.io/BufferStockTheory/#WRIC)
#
# The [Return Impatience Condition](https://econ-ark.github.io/BufferStockTheory/#RIC) $\Phi/\mathsf{R} < 1$ has long been understood to be required for the perfect foresight model to have a nondegenerate solution (a common special case is when $\rho=1$; in this case $\Phi = \mathsf{R} \beta$ so $\Phi<1$ reduces to $\beta < \mathsf{R}$).
#
# If the RIC does not hold, the consumer is so patient that the optimal consumption function approaches zero as the horizon extends indefinitely.
#
# When the probability of unemployment is $\wp$, the paper articulates an analogous (but weaker) condition:
#
# \begin{eqnarray}
#  \wp^{1/\rho} \Phi/\mathsf{R} & < & 1
# \end{eqnarray}

# %% [markdown]
# # Key Results
#
# ## [Nondegenerate Solution Requires FVAC and WRIC](https://econ-ark.github.io/BufferStockTheory/#Sufficient-Conditions-For-Nondegenerate-Solution)
#
# A main result of the paper is that the conditions required for the model to have a nondegenerate solution ($0 < c(m) < \infty$ for feasible $m$) are that the Finite Value of Autarky (FVAC) and Weak Return Impatience Condition (WRIC) hold.

# %% [markdown]
# ## [Natural Borrowing Constraint limits to Artificial Borrowing Constraint](https://econ-ark.github.io/BufferStockTheory/#The-Liquidity-Constrained-Solution-as-a-Limit)

# %% [markdown]
# Defining $\chi(\wp)$ as the consumption function associated with any particular value of $\wp$, and defining $\hat{\chi}$ as the consumption function that would apply in the absence of the zero-income shocks but in the presence of an 'artificial' borrowing constraint requiring $a \geq 0$ (_a la_ Deaton (1991)), the paper shows that
#
# \begin{eqnarray}
# \lim_{\wp \downarrow 0}~\chi(\wp) & = & \hat{\chi}
# \end{eqnarray}
#
# That is, as $\wp$ approaches zero the problem with uncertainty becomes identical to the problem that instead has constraints.  (See [Precautionary Saving and Liquidity Constraints](https://econ-ark.github.io/LiqConstr) for a full treatment of the relationship between precautionary saving and liquidity constraints).

# %% [markdown]
# ## [$c(m)$ can be Finite Even When Human Wealth Is Infinite](https://econ-ark.github.io/BufferStockTheory/#When-The-GICRaw-Fails)
#
# In the perfect foresight model, if $\mathsf{R} < \Gamma$ the PDV of future labor income approaches infinity and so the limiting consumption function is $c(m) = \infty$ for all $m$.  Many models have no well-defined solution when human wealth is infinite.
#
# The presence of uncertainty changes this: Even when limiting human wealth is infinite, the limiting consumption function is finite for all values of $m$.
#
# This is because uncertainty imposes a "natural borrowing constraint" that deters the consumer from borrowing against their unbounded (but uncertain) future labor income.

# %% [markdown]
# A [table](https://econ-ark.github.io/BufferStockTheory/#Sufficient-Conditions-For-Nondegenerate-Solution) puts this result in the context of implications of other conditions and restrictions.
#
#

# %% [markdown]
# ## [Unique and Stable Values of $\mRat$](https://econ-ark.github.io/BufferStockTheory/#Unique-Stable-Points)
#
# Assuming that the **FVAC** and **WRIC** hold so that the problem has a nondegenerate solution, under more stringent conditions its dynamics may also exhibit stability.  Two particularly useful kinds of stability are existence of a 'target' value of market resources $\Trg{\mRat}$ and a 'pseudo-steady-state' value $\StE{\mRat}$.
#
# ### [If the GIC-Nrm Holds, $\exists$ a finite 'target' $\Trg{\mRat}$](https://econ-ark.github.io/BufferStockTheory/#onetarget)
#
# Section [Individual Target Wealth](https://econ-ark.github.io/BufferStockTheory/#onetarget) shows that, under parameter values for which the limiting consumption function exists, if the GICRaw holds then there will be a value $\Trg{m}$ such that:
#
# \begin{eqnarray*}
# \mathbb{E}[m_{t+1}] & > & m_{t}~\text{if $m_{t} < \Trg{m}$} \\
# \mathbb{E}[m_{t+1}] & < & m_{t}~\text{if $m_{t} > \Trg{m}$} \\
# \mathbb{E}[m_{t+1}] & = & m_{t}~\text{if $m_{t} = \Trg{m}$}
# \end{eqnarray*}
#
# [An equation](https://econ-ark.github.io/BufferStockTheory/#mTargImplicit) in the paper tells us that if $\mRat_{t}=\Trg{m}$ then:
# \begin{align}
# (\Trg{\mNrm}-\cFunc(\Trg{\mNrm}))\bar{\RNrm}+1 & = \Trg{\mNrm}
# %\\ \Trg{\mNrm}(1-\bar{\RNrm}^{-1})+\bar{\RNrm}^{-1} & = \Trg{\cNrm}
# %\\ \Trg{\cNrm} & = \Trg{\mNrm} - (\Trg{\mNrm} - 1)\bar{\RNrm}^{-1}
# \end{align}
# which can be solved numerically for the unique $\mNrm$ that satisfies it.
#
# ### [If the GIC Holds, $\exists$ a finite 'pseudo-steady-state' $\StE{\mRat}$](https://econ-ark.github.io/BufferStockTheory/#Collective-Stability)
#
# Section [Collective Stability and the Pseudo-Steady-State](https://econ-ark.github.io/BufferStockTheory/#Collective-Stability) shows that, under parameter values for which the limiting consumption function exists, if the **GIC** holds then there will be a value $\Trg{m}$ such that:
#
# \begin{eqnarray*}
# \mathbb{E}_{t}[\mRatBF_{t+1}/\mRatBF_{t}] & > & \Gamma~\text{if $m_{t} < \StE{m}$} \\
# \mathbb{E}_{t}[\mRatBF_{t+1}/\mRatBF_{t}] & < & \Gamma~\text{if $m_{t} > \StE{m}$} \\
# \mathbb{E}_{t}[\mRatBF_{t+1}/\mRatBF_{t}] & = & \Gamma~\text{if $m_{t} = \StE{m}$}
# \end{eqnarray*}
#
# [An equation](https://econ-ark.github.io/BufferStockTheory/#balgrostableSolve) in the paper tells us that if $\mRat_{t}=\StE{m}$ then:
# \begin{align}
# (\StE{\mNrm}-\cFunc(\StE{\mNrm}))\RNrm+1 & = \StE{\mNrm}
# \end{align}
# which can be solved numerically for the unique $\StE{\mNrm}$ that satisfies it.
#
#
# ### [Example With Finite Pseudo-Steady-State $\StE{\mRat}$ But Infinite Target Wealth $\Trg{\mRat}$](https://econ-ark.github.io/BufferStockTheory/#GICNrmFailsButGICRawHolds)
#
# [A figure](https://econ-ark.github.io/BufferStockTheory/#GICNrmFailsButGICRawHolds) depicts a solution when the **FVAC** (Finite Value of Autarky Condition) and **WRIC** hold (so that the model has a solution), the **GIC** holds, so the model has a pseudo-steady-state $\StE{\mRat}$, but the **GIC-Nrm** fails, so the model does not have an individual target wealth ratio $\Trg{\mRat}$ (or, rather, the target wealth ratio is infinity, as can be seen by the fact that the level of $c$ is always below the level that would keep $\mathbb{E}_{t}[\Delta \mRat_{t+1}] = 0$)
#
# This example was constructed by quadrupling the variance of the permanent shocks from the baseline parameterization

# %%
# GICNrmFailsButGICRawHolds Example
GICNrmFailsButGICRawHoldsDict = dict(base_params)
GICNrmFailsButGICRawHoldsDict['PermShkStd'] = [0.2] # Increase patience by increasing risk

# Because we are trying to solve a problem very close to the critical patience values
# be sure to do it with extra precision

# Solve with twice the normal number of gridpoints
GICNrmFailsButGICRawHoldsDict['aXtraMax'] = base_params['aXtraCount'] * 2

# Solve over a four times larger range 
GICNrmFailsButGICRawHoldsDict['aXtraCount'] = base_params['aXtraCount'] * 4

GICNrmFailsButGICRawHolds = IndShockConsumerType(
    cycles=0, # cycles=0 makes this an infinite horizon consumer
    verbose=3, # by default, check conditions won't print out any information
    **GICNrmFailsButGICRawHoldsDict)

# Solve to a tighter than usual degree of error tolerance
GICNrmFailsButGICRawHolds.tolerance = GICNrmFailsButGICRawHolds.tolerance/100

# The check_conditions method does what it sounds like it would
# verbose=0: Print nothing;
# verbose=3: Print all available info

GICNrmFailsButGICRawHolds.solve(verbose=2) 

# %%
# Plot GICNrmFailsButGICRawHolds

#fig = plt.figure(figsize = (12,8))
# ax  = fig.add_subplot(111)

fig, ax = plt.subplots(figsize = (12,8))
[xMin,xMax] = [0.0,8.0]
yMin = 0.0
yMax = GICNrmFailsButGICRawHolds.solution[0].c_where_Ex_mtp1_minus_mt_eq_0(xMax)*1.3

mPltVals = np.linspace(xMin, xMax, mPts)

if latexExists:
    c_Stable_Ind_txt = "$\mathbb{E}_{t}[\Delta m_{t+1}] = 0$"
    c_Stable_Agg_txt = "$\mathbb{E}_{t}[\pmb{\mathrm{m}}_{t+1}/\pmb{\mathrm{m}}_{t}] = \Gamma$"
else:
    c_Stable_Ind_txt = "$\mathsf{E}_{t}[\Delta m_{t+1}] = 0$"
    c_Stable_Agg_txt = "$\mathsf{E}_{t}[\mathbf{m}_{t+1}/\mathbf{m}_{t}] = \Gamma$"


cVals_Lmting_color="black"
c_Stable_Agg_color="black"#"blue"
c_Stable_Ind_color="black"  #"red"

cVals_Lmting=GICNrmFailsButGICRawHolds.solution[0].cFunc(mPltVals)
c_Stable_Ind=GICNrmFailsButGICRawHolds.solution[0].c_where_Ex_mtp1_minus_mt_eq_0(mPltVals)
c_Stable_Agg=GICNrmFailsButGICRawHolds.solution[0].c_where_Ex_PermShk_times_mtp1_minus_mt_eq_0(mPltVals)

cVals_Lmting_lbl, = ax.plot(mPltVals, cVals_Lmting, color=cVals_Lmting_color)
c_Stable_Ind_lbl, = ax.plot(mPltVals, c_Stable_Ind, 
                            color=c_Stable_Ind_color,linestyle="dashed",label=c_Stable_Ind_txt)
c_Stable_Agg_lbl, = ax.plot(mPltVals, c_Stable_Agg, 
                            color=c_Stable_Agg_color,linestyle="dotted",label=c_Stable_Agg_txt)

ax.set_xlim(xMin,xMax)
ax.set_ylim(yMin,yMax)
ax.set_xlabel("$\mathit{m}$",fontweight='bold',fontsize=fsmid,loc="right")
ax.set_ylabel("$\mathit{c}$",fontweight='bold',fontsize=fsmid,loc="top",rotation=0)
# plt.text(xMin,yMax+0.03, "$c$", fontsize=26)
# plt.text(xMax-0.05,yMin, "$m$", fontsize=26)
ax.tick_params(labelbottom=False, labelleft=False, left='off',
                right='off', bottom='off', top='off')

#ax.arrow(0.98, 0.62, -0.2, 0, head_width=0.02, width=0.001,facecolor='black', length_includes_head='True')
#ax.arrow(2.2, 1.2, 0.3, -0.05, head_width=0.02, width=0.001,facecolor='black', length_includes_head='True')

ax.legend(handles=[c_Stable_Ind_lbl,c_Stable_Agg_lbl])
ax.legend(prop=dict(size=fsmid))

mNrmStE = GICNrmFailsButGICRawHolds.solution[0].mNrmStE
cNrmStE = c_Stable_Agg=GICNrmFailsButGICRawHolds.solution[0].c_where_Ex_PermShk_times_mtp1_minus_mt_eq_0(mNrmStE)
#mNrmStE_lbl, = ax.plot([mNrmStE,mNrmStE],[yMin,yMax],color="green",linestyle="--",label='Pseudo-Steady-State: $\mathbb{E}_{t}[\pmb{m}_{t+1}/\pmb{m}_{t}]=\Gamma$')

ax.plot(mNrmStE,cNrmStE,marker=".",markersize=15,color="black") # Dot at StE point
ax.text(1, 0.6, "$\mathrm{c}(m_{t})$", fontsize=fsmid) # label cFunc

if latexExists:
    ax.text(mNrmStE+0.02,cNrmStE-0.10, r"$\nwarrow$", fontsize=fsmid)
    ax.text(mNrmStE+0.25,cNrmStE-0.18, r"$\phantom{\nwarrow} \StE{\mRat}$", fontsize=fsmid)
else:
    ax.text(mNrmStE+0.02,cNrmStE-0.10, r"$\nwarrow$", fontsize=fsmid)
    ax.text(mNrmStE+0.25,cNrmStE-0.18, r"$\phantom{\nwarrow} \StE{\mRat}$", fontsize=fsmid)

make('GICNrmFailsButGICRawHolds')
print('Finite mNrmStE but infinite mNrmTrg')

# %% [markdown]
# In the [interactive dashboard](#interactive-dashboard), see what happens as changes in the time preference rate (or changes in risk $\sigma_\psi$) change the consumer from _normalized-growth-patient_ $(\Phi > \tilde{\Gamma})$ to _normalized-growth-impatient_ ($\Phi < \tilde{\Gamma}$)

# %% [markdown]
# As a foundation for the remaining figures, we define another instance of the class $\texttt{IndShockConsumerType}$, which has the same parameter values as the instance $\texttt{baseAgent}$ defined previously but is solved to convergence (our definition of an infinite horizon agent type) instead of only 100 periods
#

# %%
# Find the infinite horizon solution
baseAgent_Inf = IndShockConsumerType(cycles=0    # Infinite horizon
                                     , verbose=0 # solve silently 
                                     , **base_params)
baseAgent_Inf.solve()

# %% [markdown]
# ### [Target $m$, Expected Consumption Growth, and Permanent Income Growth](https://www.econ2.jhu.edu/people/ccarroll/papers/BufferStockTheory/#AnalysisoftheConvergedConsumptionFunction)
#
# The next figure, [Analysis of the Converged Consumption Function](https://www.econ2.jhu.edu/people/ccarroll/papers/BufferStockTheory/#cGroTargetFig), shows expected growth factors for the levels of consumption $\mathbf{c}$ and market resources $\mathbf{m}$ as a function of the market resources ratio $\mRat$ for a consumer behaving according to the converged consumption rule, along with the growth factor for an unconstrained perfect foresight consumer which is constant at $\Pat$ and the growth factor for permanent income which is constant at $\Gamma$.  
#
# The growth factor for consumption can be computed without knowing the _level_ of the consumer's permanent income:
# \begin{eqnarray*}
# \mathbb{E}_{t}[\mathbf{c}_{t+1}/\mathbf{c}_{t}] & = & \mathbb{E}_{t}\left[\frac{\mathbf{p}_{t+1}\cNrm_{t+1}(m_{t+1})}{\mathbf{p}_{t}\cNrm_{t}(m_{t})}\right] \\
# & = & \mathbb{E}_{t}\left[\frac{\Gamma \psi_{t+1} \mathbf{p}_{t}}{\mathbf{p}_{t}}\frac{\cNrm_{t+1}(m_{t+1})}{\cNrm_{t}(m_{t})}\right] \\
# & = & \mathbb{E}_{t}\left[\frac{\Gamma \psi_{t+1} \cNrm_{t+1}(m_{t+1})}{\cNrm_{t}(m_{t})}\right]
# \end{eqnarray*}
#
# and similarly the growth factor for market resources is:
# \begin{eqnarray*}
# \mathbb{E}_{t}[\mathbf{m}_{t+1}/\mathbf{m}_{t}] 
# & = & \mathbb{E}_{t}\left[\frac{\Gamma \psi_{t+1} \mNrm_{t+1}}{\mNrm_{t}}\right]
# \end{eqnarray*}
#
#

# %%
# Growth factors as a function of market resource ratio

color_cons = "blue"
color_mrkt = "red"
color_perm = "black"

mPlotMin = 0.0
mCalcMax = 50
mPlotMax = 2.20

# Get StE and target values
mNrmStE=baseAgent_Inf.solution[0].mNrmStE
mNrmTrg=baseAgent_Inf.solution[0].mNrmTrg

pts_num = 200 # Plot this many points

m_pts = np.linspace(1,mPlotMax,pts_num)        # values of m for plot
c_pts = baseAgent_Inf.solution[0].cFunc(m_pts) # values of c for plot 
a_pts = m_pts - c_pts                          # values of a 

Ex_cLev_tp1_Over_pLev_t = [baseAgent_Inf.solution[0].Ex_cLev_tp1_Over_pLev_t_from_at(a) for a in a_pts]
Ex_mLev_tp1_Over_pLev_t = [baseAgent_Inf.solution[0].Ex_mLev_tp1_Over_pLev_t_from_at(a) for a in a_pts]

Ex_cGro = np.array(Ex_cLev_tp1_Over_pLev_t)/c_pts
Ex_mGro = np.array(Ex_mLev_tp1_Over_pLev_t)/m_pts

# Retrieve parameters (makes code readable)
Rfree      = baseAgent_Inf.Rfree
DiscFac    = baseAgent_Inf.DiscFac
CRRA       = baseAgent_Inf.CRRA
PermGro    = baseAgent_Inf.PermGroFac[0]
mNrmStE    = baseAgent_Inf.solution[0].mNrmStE
mNrmTrg    = baseAgent_Inf.solution[0].mNrmTrg

# Absolute Patience Factor = lower bound of consumption growth factor
APF = (Rfree*DiscFac)**(1.0/CRRA)

# Create figure object 
fig = plt.figure(figsize = (12,8))
ax  = fig.add_subplot(111) # axes object 

# Plot the Absolute Patience Factor line
ax.plot([0,mPlotMax],[APF,APF],color=color_cons)

# Plot the Permanent Income Growth Factor line
ax.plot([0,mPlotMax],[PermGro,PermGro],color=color_perm)

# Plot the expected consumption growth factor
ax.plot(m_pts,Ex_cGro,color=color_cons)

# Plot the expected consumption growth factor on the right side of target m
ax.plot(m_pts,Ex_mGro,color="red")

# Axes limits 
GroFacMin = 0.98 #0.98
GroFacMax = 1.06 #1.08
xMin = 1.1 # 1.0

# Vertical lines at StE and Trg
mNrmStE_lbl, = ax.plot([mNrmStE,mNrmStE],[0,GroFacMax],color=color_mrkt,linestyle="--"
                       ,label='$\StE{m}:$ Pseudo-Steady-State: $\mathbb{E}_{t}[\pmb{\mathrm{m}}_{t+1}/\pmb{\mathrm{m}}_{t}]=\Gamma$')
mNrmTrg_lbl, = ax.plot([mNrmTrg,mNrmTrg],[0,GroFacMax],color=color_mrkt,linestyle="dotted"
                       ,label='$\Trg{m}:$ Target: $\mathbb{E}_{t}[m_{t+1}]=m_{t}$')
ax.text(mNrmStE-0.12,0.985, r'$\StE{m}\rightarrow$', fontsize = fsbig,fontweight='bold')
ax.text(mNrmTrg+0.01,0.985, r'$\leftarrow\Trg{m}$', fontsize = fsbig,fontweight='bold')

ax.legend(handles=[mNrmStE_lbl,mNrmTrg_lbl])
ax.legend(prop=dict(size=fsmid))

ax.set_xlim(xMin,mPlotMax * 1.1)
ax.set_ylim(GroFacMin,GroFacMax)

# If latex installed on system, plotting can look better 
if latexExists:
    ax.text(mPlotMax+0.01,1.01,"$\mathbb{E}_{t}[\mathbf{c}_{t+1}/\mathbf{c}_{t}]$",fontsize = fsmid,fontweight='bold')
    ax.text(mPlotMax*0.80,0.985+0.02*0,"$\leftarrow \mathbb{E}_{t}[\mathbf{m}_{t+1}/\mathbf{m}_{t}]$",fontsize = fsmid,fontweight='bold')
    ax.text(mPlotMax,0.998,r'$\pmb{\text{\TH}} = (\mathsf{R}\beta)^{1/\rho}$',fontsize = fsmid,fontweight='bold')
else:
    ax.text(mPlotMax+0.01,1.01,"$\mathsf{E}_{t}[\mathbf{c}_{t+1}/\mathbf{c}_{t}]$",fontsize = fsmid,fontweight='bold')
    ax.text(mPlotMax*0.80,0.985+0.02*0,"$\leftarrow \mathsf{E}_{t}[\mathbf{m}_{t+1}/\mathbf{m}_{t}]$",fontsize = fsmid,fontweight='bold')
    ax.text(mPlotMax,0.998,r'$\Phi = (\mathsf{\mathsf{R}}\beta)^{1/\rho}$',fontsize = fsmid,fontweight='bold')

# Ticks
ax.tick_params(labelbottom=False, labelleft=True,left='off',right='on',bottom='on',top='off')
plt.setp(ax.get_yticklabels(),fontsize=fssml)

ax.text(mPlotMax+0.01,1.029, r'$\Gamma$',fontsize = fsmid,fontweight='bold')
ax.set_ylabel('Growth Factors',fontsize = fsmid, fontweight='bold')

make('cGroTargetFig')


# %% [markdown]
# In the [interactive dashboard](#interactive-dashboard) see how target wealth changes when the consumer's time preference factor β or the growth factor Γ change.

# %% [markdown]
# ### [Consumption Function Bounds](https://www.econ2.jhu.edu/people/ccarroll/papers/BufferStockTheory/#AnalysisOfTheConvergedConsumptionFunction)
# [The next figure](https://www.econ2.jhu.edu/people/ccarroll/papers/BufferStockTheory/#cFuncBounds)
# illustrates theoretical bounds for the consumption function.
#
# We define two useful variables: lower bound of $\kappa$ (marginal propensity to consume) and limit of $h$ (Human wealth), along with some functions such as the limiting perfect foresight consumption function $\bar{c}(m)$, the upper bound function $\bar{\bar c}(m)$, and the lower bound function \underline{_c_}$(m)$.

# %%
# Define κ_Min, h_inf and PF consumption function, upper and lower bound of c function 

# Retrieve parameters (makes code below more readable)
R = Rfree      = baseAgent_Inf.Rfree
β = DiscFac    = baseAgent_Inf.DiscFac
ρ = CRRA       = baseAgent_Inf.CRRA
Γ = PermGro    = baseAgent_Inf.PermGroFac[0]
℘ = UnempPrb   = baseAgent_Inf.UnempPrb

mNrmTrg    = baseAgent_Inf.solution[0].mNrmTrg
mNrmStE    = baseAgent_Inf.solution[0].mNrmStE

κ_Min = 1.0-(R**(-1.0))*(R * β)**(1.0/ρ)
h_inf = (1.0/(1.0-Γ/R))

cFunc_Uncnst = lambda m: (h_inf -1)* κ_Min + κ_Min*m
cFunc_TopBnd = lambda m: (1 - ℘ ** (1/ρ)*(R*β)**(1.0/ρ)/R)*m
cFunc_BotBnd = lambda m: (1 -(R*β)**(1/ρ)/R) * m


# %%
# Plot the consumption function and its bounds

cMaxLabel=r'$\overline{c}(m)= (m-1+h)\underline{\kappa}$'
cMinLabel=r'Lower Bound: $\underline{c}(m)= (1-\pmb{\text{\TH}}_{R})\underline{\kappa}m$'
if not latexExists:
    cMaxLabel=r'$\overline{c}(m) = (m-1+h)κ̲' # Use unicode kludge
    cMinLabel=r'Lower Bound: c̲$(m)= (1-\Phi_{R})m = κ̲ m$'

mPlotMax = 25
mPlotMin = 0
# mKnk is point where the two upper bounds meet
mKnk = ((h_inf-1)* κ_Min)/((1 - UnempPrb**(1.0/CRRA)*(Rfree*DiscFac)**(1.0/CRRA)/Rfree)-κ_Min)
mBelwKnkPts = 300
mAbveKnkPts = 700
mBelwKnk = np.linspace(mPlotMin,mKnk,mBelwKnkPts)
mAbveKnk = np.linspace(mKnk,mPlotMax,mAbveKnkPts)
mFullPts = np.linspace(mPlotMin,mPlotMax,mBelwKnkPts+mAbveKnkPts)

plt.figure(figsize = (12,8))

plt.plot(mFullPts,baseAgent_Inf.solution[0].cFunc(mFullPts), color="black")
plt.plot(mBelwKnk,cFunc_Uncnst(mBelwKnk)          , color="black",linestyle="--")
plt.plot(mAbveKnk,cFunc_Uncnst(mAbveKnk)          , color="black",linewidth=2.5)
plt.plot(mBelwKnk,cFunc_TopBnd(mBelwKnk)          , color="black",linewidth=2.5)
plt.plot(mAbveKnk,cFunc_TopBnd(mAbveKnk)          , color="black",linestyle="--")
plt.plot(mBelwKnk,cFunc_BotBnd(mBelwKnk)          , color="black",linewidth=2.5)
plt.plot(mAbveKnk,cFunc_BotBnd(mAbveKnk)          , color="black",linewidth=2.5)
plt.tick_params(labelbottom=False, labelleft=False,left='off',right='off',bottom='off',top='off')
plt.xlim(mPlotMin,mPlotMax)
plt.ylim(mPlotMin,1.12*cFunc_Uncnst(mPlotMax))
plt.text(mPlotMin,1.12*cFunc_Uncnst(mPlotMax)+0.05,"$c$",fontsize = 22)
plt.text(mPlotMax+0.1,mPlotMin,"$m$",fontsize = 22)
plt.text(2.5,1,r'$c(m)$',fontsize = 22,fontweight='bold')
if latexExists:
    plt.text(6,5,r'$\overline{\overline{c}}(m)= \overline{\kappa}m = (1-\wp^{1/\rho}\pmb{\text{\TH}}_{R})m$',fontsize = 22,fontweight='bold')
else:
    plt.text(6,5,r'$\overline{\overline{c}}(m)= \overline{\kappa}m = (1-\wp^{1/\rho}\Phi_{R})m$',fontsize = 22,fontweight='bold')
plt.text(2.10,3.8, cMaxLabel,fontsize = 22,fontweight='bold')
plt.text(9,4.1,r'Upper Bound $ = $ Min $[\overline{\overline{c}}(m),\overline{c}(m)]$',fontsize = 22,fontweight='bold')
plt.text(8,0.9,cMinLabel,fontsize = 22,fontweight='bold')
plt.arrow(2.45,1.05,-0.5,0.02,head_width= 0.05,width=0.001,facecolor='black',length_includes_head='True')
plt.arrow(2.15,3.88,-0.5,0.1,head_width= 0.05,width=0.001,facecolor='black',length_includes_head='True')
plt.arrow(8.95,4.20,-0.8,0.05,head_width= 0.1,width=0.015,facecolor='black',length_includes_head='True')
plt.arrow(5.95,5.05,-0.4,mPlotMin,head_width= 0.05,width=0.001,facecolor='black',length_includes_head='True')
plt.arrow(14,0.70,0.5,-0.1,head_width= 0.05,width=0.001,facecolor='black',length_includes_head='True')


make('cFuncBounds')


# %% [markdown]
# ### [Upper and Lower Limits of the Marginal Propensity to Consume](https://www.econ2.jhu.edu/people/ccarroll/papers/BufferStockTheory/#MPCLimits)
#
# The paper shows that as $m_{t}~\uparrow~\infty$ the consumption function in the presence of risk gets arbitrarily close to the perfect foresight consumption function.  Defining \underline{κ}
# as the perfect foresight model's MPC, this implies that $\lim_{m_{t}~\uparrow~\infty} c^{\prime}(m) = $ \underline{κ}
# .
#
# The paper also derives an analytical limit $\bar{\kappa}$ for the MPC as $m$ approaches 0., its bounding value.  Strict concavity of the consumption function implies that the consumption function will be everywhere below a function $\bar{\kappa}m$, and strictly declining everywhere.  The last figure plots the MPC between these two limits.

# %%
# The last figure shows the upper and lower limits of the MPC

# Retrieve parameters (makes code readable)
Rfree      = baseAgent_Inf.Rfree
DiscFac    = baseAgent_Inf.DiscFac
CRRA       = baseAgent_Inf.CRRA
PermGro    = baseAgent_Inf.PermGroFac[0]
mNrmTrg    = baseAgent_Inf.solution[0].mNrmTrg
mNrmStE    = baseAgent_Inf.solution[0].mNrmStE
UnempPrb   = baseAgent_Inf.UnempPrb

mPlotMax=8    

plt.figure(figsize = (12,8))
# Set the plot range of m
m = np.linspace(0.001,mPlotMax,mPts)

# Use the HARK method derivative to get the derivative of cFunc, and which constitutes the MPC
MPC = baseAgent_Inf.solution[0].cFunc.derivative(m)

# Define the upper bound of MPC
κ_Max = (1 - UnempPrb ** (1.0/CRRA)*(Rfree*DiscFac)**(1.0/CRRA)/Rfree)

# Define the lower bound of MPC
MPCLower = κ_Min

kappaDef=r'$\underline{\kappa}\equiv(1-\pmb{\text{\TH}}_{R})$'
if not latexExists:
    kappaDef=r'κ̲$\equiv(1-\Phi_{R})$'

plt.plot(m,MPC,color = 'black')
plt.plot([mPlotMin,mPlotMax],[κ_Max,κ_Max],color = 'black')
plt.plot([mPlotMin,mPlotMax],[κ_Min,κ_Min],color = 'black')
plt.xlim(mPlotMin,mPlotMax)
plt.ylim(0,1) # MPC bounds are between 0 and 1 
plt.text(1.5,0.6,r'$\kappa(m) \equiv c^{\prime}(m)$',fontsize = 26,fontweight='bold')
if latexExists:
    plt.text(5,0.87,r'$(1-\wp^{1/\rho}\pmb{\text{\TH}})\equiv \overline{\kappa}$',fontsize = 26,fontweight='bold') # Use Thorn character
else:
    plt.text(5,0.87,r'$(1-\wp^{1/\rho}\Phi_{R})\equiv \overline{\kappa}$',fontsize = 26,fontweight='bold') # Use Phi instead of Thorn (alas)

plt.text(0.5,0.07,kappaDef,fontsize = 26,fontweight='bold')
plt.text(mPlotMax+0.05,mPlotMin,"$m$",fontsize = 26)
plt.arrow(1.45,0.61,-0.4,mPlotMin,head_width= 0.02,width=0.001,facecolor='black',length_includes_head='True')
plt.arrow(2.2,0.07,0.2,-0.01,head_width= 0.02,width=0.001,facecolor='black',length_includes_head='True')
plt.arrow(4.95,0.895,-0.2,0.03,head_width= 0.02,width=0.001,facecolor='black',length_includes_head='True')

make('MPCLimits')


# %% [markdown]
# # Summary
#
# [Two tables in the paper](https://econ-ark.github.io/BufferStockTheory/#Factors-Defined-And-Compared) summarize the various definitions, and then articulate conditions required for the problem to have a nondegenerate solution.  Among the nondegenerate cases, the most interesting result is that if the Growth Impatience Condition holds there will be a target level of wealth.

# %% [markdown]
# ### Appendix: Options for Interacting With This Notebook <a id='optionsForInstalling'></a>
#
# 1. [View (static version)](https://github.com/llorracc/BufferStockTheory/blob/master/Code/Python/BufferStockTheory.ipynb) on GitHub (warning:  GitHub does not render Jupyter notebooks reliably)
# 1. [Launch Online Interactive Version](https://econ-ark.org/materials/BufferStockTheory/#launch)
# 1. For fast (local) execution, install [econ-ark](http://github.com/econ-ark) on your computer ([QUICK START GUIDE](https://github.com/econ-ark/HARK/blob/master/README.md)) then follow these instructions to retrieve the full contents of the `BufferStockTheory` [REMARK](https://github.com/econ-ark/REMARK):
#    1. At a command line, change the working directory to the one where you want to install
#        * On unix, if you install in the `/tmp` directory, the installation will disappear after a reboot:
#        * `cd /tmp`
#    1. `git clone https://github.com/econ-ark/REMARK --recursive`
#    1. `cd REMARK/REMARKs/BufferStockTheory`
#    1. `jupyter notebook BufferStockTheory.ipynb`

# %% [markdown]
# ### Appendix: Perfect foresight agent failing both the FHWC and RIC

# %%
from copy import copy
from HARK.ConsumptionSaving.ConsIndShockModel import PerfForesightConsumerType
fig6_par = copy(base_params)

# Replace parameters.
fig6_par['Rfree'] = 0.98
fig6_par['DiscFac'] = 1
fig6_par['PermGroFac'] = [0.99]
fig6_par['CRRA'] = 2
fig6_par['BoroCnstArt']  = 0
fig6_par['T_cycle'] = 0
fig6_par['cycles'] = 0
fig6_par['quiet'] = False

# Create the agent
RichButPatientAgent = PerfForesightConsumerType(**fig6_par)
# Check conditions
RichButPatientAgent.check_conditions(verbose = 3)
# Solve
RichButPatientAgent.solve()

# Plot
mPlotMin, mPlotMax = 1, 9.5
plt.figure(figsize = (8,4))
m_grid = np.linspace(mPlotMin,mPlotMax,500)
plt.plot(m_grid-1, RichButPatientAgent.solution[0].cFunc(m_grid), color="black")
plt.text(mPlotMax-1+0.05,1,r"$b$",fontsize = 26)
plt.text(mPlotMin-1,1.017,r"$c$",fontsize = 26)
plt.xlim(mPlotMin-1,mPlotMax-1)
plt.ylim(mPlotMin,1.016)

make('PFGICRawHoldsFHWCFailsRICFails')


# %% [markdown]
# ----------------------------------------------------------