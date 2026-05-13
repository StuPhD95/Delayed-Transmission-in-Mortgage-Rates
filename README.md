# Modelling Delayed Market Responses

In markets, sudden and unexpected disturbances (or shocks) do not always transmit instantaneously. 



A standard ordinary differential equation (ODE) of the form

$$ \frac{dx(t)}{dt}=ax(t), \quad a>0,$$

This captures the instantaneous relationship between equity stress and VIX.

$$ \frac{du(t)}{dt}=bu(t-\tau), \quad b>0,$$

where $\tau>0$ is a delay parameter.

$$u(t)=\sum_{n=0}^\infty\frac{b^n(t-n\tau)^n}{n!}\Theta\left(t-n\tau\right)$$

Here, $\Theta$ defines the Heaviside function 
