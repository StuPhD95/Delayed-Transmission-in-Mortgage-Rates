# Delayed Transmission in Mortgage Rates

This project tests whether adding multiple constant time-delays improves a simple memoryless benchmark in a fixed-income setting. The motivating question is:

> Do mortgage rates respond immediately to changes in Treasury yields, or does part of the response arrive with a delay


## Motivation

A key concept in fixed-income markets is the yield curve. It illustrates how the expected yearly return on bonds, known as the yield, changes across different maturities (e.g. short-term bonds to longer-term bonds). The yield curve is closely watched because its shape reflects how investors think about future interest rates, inflation and economic growth. 

When expectations about future interest rates change, bond yields often move across the curve. However, not every part of the curve reacts in the same way or at the same time. Short-maturity yields may react quickly to changes in expected policy rates, while longer-maturity yields may adjust over subsequent days as investors reassess inflation, growth and the risks associated with holding longer-term bonds. Delay differential equations (DDEs) provide a natural way to model this gradual transmission, because they allow current yield movements to depend on past values. This can capture delayed effects that standard memoryless ordinary differential equation (ODE) or partial differential equation (PDE) models may overlook.

As a deliberately simplified benchmark for a memoryless yield response, consider

$$\frac{du(t)}{dt}=au(t),$$

where $u(t)$ represents the change in a longer-maturity bond yield after $t$ days and $a>0$ controls the strength of the response. The solution is given by

$$u(t)=u(0)e^{at}.$$

This model is not intended to be realistic on its own. It simply illustrates that the current rate of change depends only on the current value $u(t)$, so the response begins immediately.

For DDEs, the analogous delay model is 

$$ \frac{du(t)}{dt}=au(t-\tau),$$

where $\tau>0$ is a delay parameter. In this case, the current rate of change depends on the value of the system $\tau$ days earlier, which captures the idea that longer-maturity yields may respond to earlier short-rate or policty shocks only after a time lag. The solution of this equation with history $u(t)=0$ for $t<0$ and $u(0)=1$ is given by 

$$u(t)=\sum_{n=0}^\infty\frac{a^n(t-n\tau)^n}{n!}\Theta(t-n\tau),$$

where $\Theta(t)$ is the Heaviside function that is defined as $\Theta(t)=0$ for $t<0$ and $\Theta(t)=1$ for $t\ge 0$. The plots below illustrate the dynamics of these solutions over two different time periods where $a=\tau=0.5$. 

Small Time Dynamics            |  Large Time Dynamics
:-------------------------:|:-------------------------:
 ![Small Time](Figures/Solution_Small_Time.png) | ![Large Time](Figures/Solution_Large_Time.png) 

The key distinction is that the ODE model produces an immediate response, whereas the DDE model allows the response to begin only after the delay period has passed. In a fixed-income setting, this reflects the idea that shocks to short-rate expectations may not be transmitted instantaneously to longer-maturity yields. Instead, part of the adjustment may unfold over subsequent trading days as the market reassesses the implications for inflation, growth and term premia.

This distinction is useful in a financial setting. A standard non-delay model can test whether volatility reacts to a market shock at the same time the shock occurs. A delay model can instead test whether part of the volatility response appears after a lag. In other words, the non-delay model captures an immediate reaction, whereas the delay model captures delayed propagation.


## Non-Delayed Model

It assumes that t
$$\Delta m_t=c+\beta_0\Delta^{10Y}_t+\epsilon_t,$$

where


## Delayed Model

The delayed model allows mortgage-rate changes to depend on both current and historical tresury-yield changes. It is given by

$$ \Delta m_t=c+\beta_0\Delta y^{10}_t+\beta_1\Delta y^{10Y}_{t-1}+\beta_2\Delta y^{10Y}_{t-2}+\epsilon_t,$$

where $\Delta m_t$ is the change in the, $\Delta y^{10Y}_{t-i}$ is the change in the 10-year Tresury yield $i$ weeks ago, $\beta_i$ are response coefficients, $c\in\mathbb{R}$ and $\epsilon_t$ denotes the model error.


---

## Results

The fixed-delay model improves the no-delay benchmark. The no-delay model uses only the same-week change in the 10-year Treasury yield to predict the weekly change in the 30-year fixed mortgage rate:

$$\Delta m_t=c+\beta_0 \Delta y^{10Y}_t+\varepsilon_t.$$

The fixed-delay model adds one-week and two-week lagged Treasury-yield changes:

$$\Delta m_t=c+\beta_0 \Delta y^{10Y}_t+\beta_1 \Delta y^{10Y}_{t-1}+\beta_2 \Delta y^{10Y}_{t-2}+\varepsilon_t.$$

The key question is whether these delayed terms improve prediction out of sample.

They do. The fixed-delay model reduces out-of-sample RMSE by **26.06%** relative to the no-delay benchmark.

This means that mortgage-rate changes are better explained by a combination of current and lagged Treasury-yield changes than by current Treasury-yield changes alone.

---

## RMSE Comparison

The improvement is measured using

$$
100
\times
\frac{
\text{RMSE}_{\text{no delay}}
-
\text{RMSE}_{\text{fixed delay}}
}{
\text{RMSE}_{\text{no delay}}
}.
$$

A positive value means the fixed-delay model has lower prediction error than the benchmark.

In this case, the improvement is **26.06%**, so the result is clearly positive.

<p align="center">
  <img src="Figures/Mortgage_Delay_RMSE_Comparison.png" width="700">
</p>

The RMSE comparison shows that the fixed-delay model has lower out-of-sample prediction error than the no-delay benchmark.

<p align="center">
  <img src="Figures/Mortgage_Delay_RMSE_Improvement.png" width="700">
</p>

The improvement plot highlights the main quantitative result: adding fixed delays reduces out-of-sample RMSE by **26.06%**.

---

## Interpretation

This result supports the idea of delayed pass-through from Treasury yields to mortgage rates.

Treasury yields are market rates that adjust quickly to new information. Mortgage rates, however, are retail lending rates and may adjust more slowly due to lender pricing, mortgage-market conditions and borrower-facing rate-setting processes.

The result suggests that this week’s mortgage-rate change is not explained only by this week’s Treasury-yield movement. It also depends on Treasury-yield movements from previous weeks.

In other words, the fixed-delay model captures information that the no-delay benchmark misses.

---

## Takeaway

The main result is:

> Adding one-week and two-week fixed delays reduces out-of-sample RMSE by **26.06%** relative to the no-delay model.

This provides a simple, data-driven example where delay-based modelling improves a standard benchmark.

The result does not prove that mortgage rates follow a delay differential equation. However, it does show that fixed-delay terms add useful predictive information in this mortgage-rate pass-through setting.

