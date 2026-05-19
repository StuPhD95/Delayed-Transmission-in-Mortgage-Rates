# Delayed Transmission in Mortgage Rates

This project investigates whether adding multiple constant time-delays can improve the predictive power of a standard memoryless model in a simple fixed-income setting. The motivating question is:

> Do past Treasury-yield movements help predict mortgage rates better than using only the current Treasury-yield movement?

Using weekly U.S. interest-rate data, it is shown that the fixed-delay model reduces out-of-sample RMSE by **26.06%** relative to the no-delay benchmark. In simple terms, allowing the model to remember past yield movements helps explain mortgage-rate behaviour more accurately than using only the current yield movement.

## Motivation

A key concept in fixed-income markets is the **yield curve**. It shows how the expected yearly return on bonds, known as the **yield**, changes across different maturities, from short-term bonds to longer-term bonds.

The yield curve is closely watched because it reflects market expectations about future interest rates, inflation and economic growth. When those expectations change, yields often move across the curve. However, the adjustment need not happen everywhere at once.

This project studies a simple example of delayed transmission: the pass-through from the **10-year Treasury yield** to the **30-year fixed mortgage rate**.

Treasury yields are market rates and can update quickly. Mortgage rates are retail lending rates, so they may adjust more slowly through lender pricing, mortgage-market conditions and borrower-facing rate-setting processes.

The main question is therefore:

> When Treasury yields move, do mortgage rates respond immediately, or does part of the response arrive with a delay?

To test this, I compare a no-delay benchmark with a fixed-delay model that includes one-week and two-week lagged Treasury-yield changes. The aim is to see whether adding delayed information improves out-of-sample prediction of mortgage-rate changes.

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

