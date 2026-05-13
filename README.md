# Modelling Delayed Market Responses

In markets, sudden and unexpected disturbances (or shocks) do not always transmit instantaneously. 



A standard ordinary differential equation (ODE) of the form

$$ \frac{dx(t)}{dt}=ax(t), \quad a>0,$$


$$ \frac{du(t)}{dt}=bu(t-\tau), \quad b,\tau>0,$$

$$u(t)=\sum_{n=0}^\infty\frac{b^n(t-n\tau)^n}{n!}\Theta\left(t-n\tau\right)$$

Here, $\Theta$ defines the Heaviside function 
