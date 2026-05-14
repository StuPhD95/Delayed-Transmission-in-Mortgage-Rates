# Delayed Volatility Responses to Market Shocks

When the stock market falls, volatility often rises. However, the response to a market shock may not occur all at once. Part of the effect may unfold over the following days as investors adjust their positions, hedge risk and respond to new information. Delay differential equations (DDEs) provide a natural way to model this delayed response, capturing effects that standard ordinary differential equation (ODE) or partial differential equation (PDE) models may overlook.

For ODEs, the exponential function plays a fundamental role. As a deliberately simplified model of volatility growth, consider

$$\frac{du(t)}{dt}=au(t), \quad a>0,$$

where $u(t)$ represents a measure of volatility and $a$ is a growth parameter. The solution of this equation is

$$u(t)=u(0)e^{at}.$$

This solutions describes how the effect of the initial condition evolves over time. Although this model is too simple to be realistic on its own, it provides a useful benchmark in that the current rate of change depends only on the current volatility value. 

For DDEs, the analogous delay model is 

$$ \frac{du(t)}{dt}=bu(t-\tau), \quad b>0,$$

where $\tau>0$ is a delay parameter. In this case, the current rate of change depends on the past value., which captures the idea that volatility may respond to previous market conditions after a time lag. The solution of this equation with zero history before $t=0$ and a unit initial value at $t=0$ is given by 

$$u(t)=\sum_{n=0}^\infty\frac{b^n(t-n\tau)^n}{n!}\Theta\left(t-n\tau\right),$$

where $\Theta(t)$ is the Heaviside function that is defined to be zero for $t<0$ and one for $t\ge 0$. The below plots illustrate the dynamics of the aforementioned solutions over different time periods.

Small Time Dynamics            |  Large Time Dynamics
:-------------------------:|:-------------------------:
 ![Small Time](Figures/Solution_Small_Time.png) | ![Large Time](Figures/Solution_Large_Time.png) 
