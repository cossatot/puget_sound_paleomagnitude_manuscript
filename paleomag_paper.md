---
title: "Improving paleoseismic earthquake magnitude estimates with rupture 
length information: application to the Puget Lowland, WA USA"

author:
- name:  Richard Styron
  affiliation:  Earth Analysis 
  email: Richard.h.styron@gmail.com

- name: Brian Sherrod
  affiliation: US Geological Survey 
...

# Introduction

A primary objective of paleoseismology is the estimation of the magnitude of
earthquakes in the geologic record. These paleoearthquakes are typically
described in a shallow trench excavated across a fault scarp, where the data
constraining the offset and age of all earthquakes are taken. The magnitude of
each event is determined by scaling offset measurements from the trench with
empirical displacement-magnitude relations.

Considerable uncertainty exists in this process: In addition to substantial
scatter in the displacements magnitude scaling relations (up to xx%), the
observed offset in or near the trench has its own measurement error, and is
likely not representative of the mean offset along the paleorupture, simply due
to the natural variability of earthquake ruptures. This last problem is
particularly challenging, as it is both hard to accurately address
statistically and can lead to variation in the estimated magnitude of 1-2
magnitude orders (i.e. M 6-8). *Biasi and Weldon* [*2006*] devised an effective
solution using Bayesian methods that use a likelihood function derived from
empirical slip distribution data to reduce the uncertainty in the posterior
magnitude given a point measurement of displacement.

Surface rupture length is better correlated with earthquake magnitude than mean
displacement [e.g., *Wells and Coppersmith, 1994*], and can therefore be used as
a similar predictor of paleoearthquake magnitude. In fact, independent
measurements of both surface rupture length and displacement can be used to
estimate paleoearthquake magnitude more accurately and precisely. In this paper
we provide an implementation as an extension of Biasi and Weldon's
paleomagnitude inversion. We then apply the technique to a compilation of ~30
earthquakes from the Puget Lowland, Washington State (USA). The use of 

# Paleoearthquakes in the Puget Lowland

The Puget Lowland is a low-elevation region in the forearc of the Cascadia
subduction zone (Figure \ref{pug_map}). Subduction of the Juan de Fuca plate
here is quite oblique; some *xx* mm a$^{-1}$ of the total 34 +/- xx mm a$^{-1}$
of plate convergence is right-lateral shear, which manifests as a northward
component to forearc motion.  The northward velocity of the forearc decreases
just north of the US-Canada border, causing several mm yr$^{-1}$ of N-S
shortening across the forearc. An array of east-striking reverse faults,
NE-striking dextral-reverse faults and NW-striking sinistral-reverse faults
cutting the Puget Lowland are mapped based on geologic, geophysical and
topographic data.

![Map of the Puget Lowland. \label{pug_map}](./figures/pug_map_small.pdf)

The retreat of the Pleistocene ice sheets from the region left a 


## Data

### Offset measurements


### Rupture lengths

Rupture lengths for each earthquake were not able to be measured precisely, as
each of the probable rupture extents cross heavily vegetated, urbanized, and
submarine zones. Additionally, most of the studied faults have had multiple
earthquakes in the Holocene, so observed faults scarps are cumulative scarps
and the lengths of individual earthquakes cannot be directly measured.

Therefore, we have bracketed rupture length by maxima and minima. The maxima
are essentially the full length of each fault determined by from geological and
geophysical data. Many of the faults studied are shown geologically to be
confined to the Puget Lowland, and do not extend far into the marginal Cascade
and Olympic mountains. The minima are the lengths between paleoseismic trenches
in which the earthquakes are observed, or the lengths of clear ruptures in the
topographic data.


### Length-offset scaling

Earthquakes in the Puget Lowland have rupture lengths that are limited by the
lengths of the faults that host them. East-striking reverse faults, such as the
Seattle fault zone (SFZ), do not extend into the mountains bounding the eastern
and western margins of the lowland. However, observed offsets for individual
events may be quite large: Offsets of up to 8 meters have been measured from
uplifted shorelines and fault scarps on LiDAR [*Barnett et al., 2015*, *Nelson
et al., 2016*], though most offset measurements are between 1-2.5 m. 

Even moderate observed offsets show ratios of offset to maximum rupture length
that are far higher than that predicted by the empirical scaling relationships
between mean offset and rupture length [*Wells and Coppersmith, 1994*]. As
earthquake magnitude is proportional to the product of displacement and length
[**REF**], predictions of earthquake magnitude based on either rupture length or
displacement will only be accurate if the length : displacement ratio is typical
for the data used to construct the scaling. If the ratio is atypical, the use of
a single datum will bias the predicted earthquake magnitude. 

## Statistical approach

### Earthquake magnitude given displacement

We use rupture length information to aid in paleoearthquake magnitude estimation
by extending the Bayesian magnitude inversion scheme developed by Biasi and
Weldon (2006). Their method is centered around Bayes' Theorem cast appropriately
for this problem:
$$ p(M|D) = p(M) \,\frac{ p(D|M)}{p(D)}$$ {#eq:bw06}
where $p(M)$ is the prior probability of the earthquake magnitude $M$, $p(D|M)$
is the likelihood function, which states the likelihood of observing a
displacement of size $D$ given an earthquake of magnitude $M$, and $p(D)$ is the
probability of $D$, which in this case is essentially a normalization constant.
The solution to the Bayesian inversion is $p(M|D)$, the posterior magnitude
distribution given the displacement observations.

The likelihood function $p(D|M)$ incorporates the intrinsic variability in
the surface displacements at any point in an earthquake surface rupture. This
may not be derived simply from first principles (given our current knowledge of
earthquake physics); instead, *Biasi and Weldon* [*2006*] derived a probability
function based on a compilation of earthquake slip data 

**Likelihood function also incorporates Wells and Coppersmith scaling**

We follow this approach, with a minor modification of the likelihood function:
Biasi and Weldon used histograms of the normalized earthquake slip data to
represent the earthquake slip distribution, leading to a somewhat noisy
function. We instead use a kernel density estimate of the normalized slip data
to yield a smoother distribution function with higher resolution.

We also extend this method by incorporating uncertainty in offset measurements
into the inversion using Monte Carlo methods. A distribution is defined for the
offset measurements, and some large number of samples are drawn from that
distribution. Then, the inversion is run for each of those samples (using the
same prior) and the posteriors are then averaged to yield a final $p(M|D)$ PDF
that incorporates the uncertainty in the offset data.

### Length incorporation

We extend the Bayeisan framework to include rupture length by creating an
additional PDF for the earthquake magnitude based on the rupture length. As an
earthquake has a single rupture length (disregarding epistemic uncertainty), the
sampling problems relating to a point offset measurement from a continuous
displacement profile are not encountered here. Therefore, a complex likelihood
function is not needed, and we simply use an empirical length-magnitude scaling
relationship to derive magnitude estimates from rupture length:
$$ p(M|L) = a + b \log_{10}(L) \;, $$ {#eq:ml_scaling}
where $a$ and $b$ are constants.

Note that the magnitude estimate $p(M(L))$ is not given as a posterior
magnitude such as $p(M|D)$. This reflects the nature of the magnitude estimate
as a simple functional transformation of $L$, rather than a Bayesian inversion. 

However, both the parameters $a$ and $b$ and the length observations $L$ have
uncertainty. This is also propagated to $p(M(L))$ with Monte Carlo techniques:
for each of $n$ samples of $L$, samples of $a$ and $b$ are also drawn, and the
resulting PDFs are averaged.

We then use $p(M(L))$ in the modified relation
$$ p(M|D,L) = p(M) \, p(M|L)\, \frac{p(D|M)}{p(D)} \; .$$ {#eq:pmdl}
An example of this calculation is show in Figure \ref{example_pdf}. 

![Schematic showing Eqn @eq:pmdl for an earthquake
\label{example_pdf}](./figures/pdf_mult.pdf)

# Results

## Magnitudes of Puget Lowland paleoearthquakes

Individial paleoearthquakes in the Puget Lowland have magnitudes between 6.4
and 7.5 (Figure). The uncertainty 
