---
title: "Improving paleoseismic earthquake magnitude estimates with rupture 
length information: application to the Puget Lowland, WA USA"

author:
- name:  Richard Styron
  affiliation:  Earth Analysis 
  email: Richard.h.styron@gmail.com

- name: Brian Sherrod
  affiliation: US Geological Survey 

abstract: "Both earthquake displacement and rupture length correlate with
magnitude, and therefore observations of each from past events can be used to
estimate the magintude of those events in the absence of instrumental records.
We extend the Bayesian inversion of *Biasi and Weldon* [*2006*], which
estimates paleoearthquake magnitude from displacement observations, to
incorporate both rupture length and surface displacement measurements into the
magnitude inversion. We then use this method on 27 late Pleistocene to Holocene
paleoearthquakes in the Puget Lowlands region of Washington and find that all
events were betwen $M$ 6.2 and 7.7. The simultaneous use of both length and
displacement data in the magnitude inversion substantially decreases both the
estimated earthquake magnitudes and the uncertainty. The magnitude reduction in
particular is due to the relatively short rupture lengths possible for Puget
Lowland faults. This implies a decrease in the seismic hazard to a highly
populated and rapidly urbanizing region." 

...


# Tweets
- Bayesian method to estimate paleoearthquake magnitude from length and
  displacement data

- 27 paleoearthquake magnitudes in the Puget Lowland area (WA, USA) between 
  6.2 and 7.7

- Use of length data in inversion reduces magnitude by ~0.4 *M* and uncertainty
  by 50%



# Introduction

A primary objective of paleoseismology is the estimation of the magnitude of
earthquakes inferred from the geologic record. These paleoearthquakes are
typically described in a shallow trench excavated across a fault scarp, where
the data constraining the offset and age of any inferred earthquakes are taken.
The magnitude of each event is then determined by scaling offset measurements
from the trench with empirical displacement-magnitude relations, such as those
by *Wells and Coppersmith* [*1994*].

Considerable uncertainty exists in this process: In addition to 
scatter in the data used to create the displacement-magnitude scaling
relations, the observed offset in or near the trench has its own measurement
error, and is likely not representative of the mean offset along the
paleorupture, simply due to the natural along-strike variability of earthquake
ruptures [*Hemphill-Haley and Weldon, 1999*]. This last problem is particularly
challenging, as it is both hard to accurately address statistically and can
lead to variation in the estimated magnitude of 1-2 magnitude orders (i.e. *M*
6-8). Building on the work of *Hempill-Haley and Weldon* [*1999*], *Biasi and
Weldon* [*2006*] devised an effective solution with a Bayesian method that uses
a likelihood function derived from empirical slip distribution data to reduce
the uncertainty in the posterior magnitude given a point measurement of
displacement.

Surface rupture length is better correlated with earthquake magnitude than mean
displacement [*Wells and Coppersmith, 1994*], and can therefore be used as a
similar predictor of paleoearthquake magnitude. In fact, independent
measurements of both surface rupture length and displacement can be used to
estimate paleoearthquake magnitude more accurately and precisely. In this paper
we provide an implementation as an extension of *Biasi and Weldon*'s
paleomagnitude inversion. We then apply the technique to a compilation of 27
earthquakes from the Puget Lowland, Washington State (USA). The use of rupture
length in the paleoearthquake magnitude inversions is here shown to reduce both
the estimated magnitude and the associated uncertainty by a large margin, which
has positive implications for the seismic hazard of the Puget Sound metro
areas, including the cities of Seattle, Tacoma and Olympia, with an at-risk
population of >4 million [*U.S. Census Bureau, Population Division, 2015*].

# Paleoearthquakes in the Puget Lowland

The Puget Lowland is a low-elevation region in the forearc of the Cascadia
subduction zone (Figure \ref{pug_map}). Subduction of the Juan de Fuca plate
here is quite oblique, which manifests as a northward component to forearc
motion. The northward velocity of the forearc decreases just north of the
US-Canada border, causing several mm yr$^{-1}$ of N-S shortening across the
forearc [*Mazzotti et al., 2002*]. An array of east-striking reverse faults,
NE-striking dextral-reverse faults and NW-striking sinistral-reverse faults
cutting the Puget Lowland are mapped based on geologic, geophysical and
topographic data.

![Map of the Puget Lowland. Paleoseismic sites are shown as white dots.
Ruptures studied here are shown in pink and blue; pink represents the maximum
possible length of each earthquake, and blue represents the minimum. Additional
fault in black are from the USGS Quaternary Fault and Fold database
\label{pug_map}](./figures/pug_map_small.pdf)

Though paleoearthquake scarps are difficult to see from a distance in the
landscape due to thick vegetation, many scarps are quite evident in lidar
imagery of the region. Most of them cut the 16 ka Vashon Till, which blankets
the lowland and serves as an important marker unit in paleoseismic trenches.
The unit is thick enough to mask older scarps and similar geomorphic features,
so that the total vertical separation observed across a fault scarp is known to
be post-16 ka deformation and in many cases attributable to specific Holocene
earthquakes.


## Data 

We have assembled a dataset of 27 paleoearthquakes in the Puget Lowland and
vicinity [Table X, supplementary materials?]. All of the paleoearthquakes have
been described in the literature, and offset measurements are taken from those
sources. Rupture length estimates are taken from the literature, supplemented
by mapping on lidar data of the region assembled by the Puget Sound Lidar
Consortium.

### Offset measurements

Offsets were measured in trenches, field surveys, or lidar scarp profiling. 
Most earthquakes in the dataset had vertical separation given as the component 
of measured slip, as net offset was not able to be constrained directly. In
these instances, vertical separations were converted to net offsets using fault
dip and rake estimates. Uncertainties were estimated for all values, and were
treated as uniform distributions and propagated through using Monte Carlo
simulations. However, the offset distributions produced from Monte Carlo
simulations were not generally uniform because of the nonlinearities in the
trigonometric functions used to convert vertical separation to offset.

Measured vertical separations range from 0.5 ± 0.25 m to 7.0 ± 1.0 m,
corresponding to ~1-10 m offset (near-surface fault dips are generally steep).
The median offset is 2.1 m.


### Rupture lengths

Rupture lengths for each earthquake were not able to be measured precisely, as
each of the probable rupture extents crosses heavily vegetated, urbanized,
and/or submarine zones. Additionally, most of the studied faults have had
multiple earthquakes in the Holocene, so observed faults scarps are cumulative
scarps and the lengths of individual earthquakes cannot be directly measured.

Therefore, we have bracketed rupture length by maxima and minima. The maxima
are essentially the full length of each fault zone determined by from
geological and geophysical data. Many of the faults studied are shown
geologically to be confined to the Puget Lowland, and do not extend far into
the marginal Cascade and Olympic mountains. The minima are the lengths between
paleoseismic trenches in which the earthquakes are observed, or the lengths of
clear ruptures in the topographic data.

The discrepancies between the minimum and maximum rupture lengths are very
large: $L_{\min}$ ranges from 2 to 33 km (median 4 km), while $L_{\max}$ ranges
from 6 to 186 km (median 53 km). The median $L_{\max}:L_{\min}$ ratio is 11.8,
and the mean is 13.8.


### Length-offset scaling

Earthquakes in the Puget Lowland have rupture lengths that are limited by the
lengths of the faults that host them. East-striking reverse faults, such as the
Seattle fault zone (SFZ), do not extend into the mountains bounding the eastern
and western margins of the lowland. However, observed offsets for individual
events may be quite large: Offsets of up to 8 meters have been measured from
uplifted shorelines and fault scarps on lidar [*Sherrod et al., 2000*; *Nelson
et al., 2014*; *Barnett et al., 2015*], though most offset measurements are
between 1-2.5 m. 

![Length-offset scaling for Puget Lowland earthquakes and scaling
relationships. WC94 = scaling of *Wells and Coppersmith* [*1994*] for all
earthquakes. W08 = scaling of *Wesnousky* [*2008*] for continental reverse
faults. \label{ld_scaling}](./figures/l_d_scaling.pdf)

Even moderate observed offsets show ratios of offset to maximum rupture length
that are far higher than that predicted by the empirical scaling relationships
between mean offset and rupture length (Figure \ref{ld_scaling} [e.g., *Wells
and Coppersmith, 1994*], though the scaling is typical for continental reverse
fault ruptures [*Wesnousky, 2008*], despite many of these ruptures being
oblique-slip. As earthquake magnitude is proportional to the product of
displacement and length [*Aki and Richards, 1980*], predictions of earthquake
magnitude based on either rupture length or displacement will only be accurate
if the length to displacement ratio is typical for the data used to construct
the scaling. If the ratio is atypical, the use of a single data type will bias
the predicted earthquake magnitude.




# Paleoearthquake magnitude inversion

## Earthquake magnitude given displacement

We use rupture length information to aid in paleoearthquake magnitude
estimation by extending the Bayesian magnitude inversion scheme developed by
*Biasi and Weldon* [*2006*]. Their method is centered around Bayes' Theorem cast
appropriately for this problem:
$$ p(M|D) = p(M) \,\frac{ p(D|M)}{p(D)}$$ {#eq:bw06}
where $p(M)$ is the prior probability of the earthquake magnitude $M$, $p(D|M)$
is the likelihood function, which states the likelihood of observing a
displacement of size $D$ given an earthquake of magnitude $M$, and $p(D)$ is
the probability of $D$, which in this case is essentially a normalization
constant. The solution to the Bayesian inversion is $p(M|D)$, the posterior
magnitude distribution given the displacement observations.

The likelihood function $p(D|M)$ incorporates the intrinsic variability in
the surface displacements at any point in an earthquake surface rupture. This
may not be derived simply from first principles (given our current knowledge of
earthquake physics). Instead, *Biasi and Weldon* [*2006*] derived a likelihood
function that incorporates a statistical distribution of normalized surface
displacements (which we call $p(D_n)$), and a scaling relationship between
earthquake magnitude $M$ and mean surface displacement. $p(D_n)$ is simply an
empirical distribution of the frequency (or probability) of an offset $D$ 
occurring anywhere along the length of an individual rupture divided by the 
mean displacement for that event; it was made through compilation of 13 
well-mapped ruptures. $D_{pred}(M)$ is the predicted mean surface displacement 
for a given earthquake magnitude, in this case from the empirical scaling 
relationship of *Wells and Coppersmith* [*1994*]. The likelihood function
$p(D|M)$ is then constructed as $$ p(D|M) = p(D_n) / D_{pred}(M)\;.$$ {#eq:pdm}

We follow this approach, with a minor modification of the likelihood function:
*Biasi and Weldon* used histograms of the normalized earthquake slip data to
represent the earthquake slip distribution, leading to a somewhat noisy
function with limited resolution (i.e. 0.1 $M$). We instead use a kernel
density estimate of the normalized slip data to yield a continuous, smooth
distribution function with arbitrary resolution.

We also extend this method by incorporating uncertainty in offset measurements
into the inversion using Monte Carlo methods. A distribution is defined for the
offset measurements, and some large number of samples are drawn from that
distribution. Then, the inversion is run for each of those samples (using the
same prior) and the posteriors are then averaged to yield a final $p(M|D)$ PDF
that incorporates the uncertainty in the offset data.

## Length incorporation

We extend the Bayesian framework to include rupture length by creating an
additional likelihood function for the earthquake magnitude based on the
rupture length. As an earthquake has a single rupture length (disregarding
epistemic uncertainty), the sampling problems relating to a point offset
measurement from a continuous displacement profile are not encountered here.
Therefore, a complex likelihood function is not needed, and we simply use an
empirical length-magnitude scaling relationship to derive magnitude estimates
from rupture length: $$ p(L|M) = a + b \log_{10}(L) \;, $$ {#eq:ml_scaling} 
where $a$ and $b$ are constants. We use $a=5.08 \pm 0.1$ and $b=1.16 \pm 0.7$
(uncertainties are standard error) [*Wells and Coppersmith, 1994*], but updated
or problem-specific relations could work as well.

The stated uncertainty in $a$ and $b$, as well as the wider range between
$L_{\min}$ and $L_{\max}$, are incorporated through Monte Carlo simulations:
for each of $n$ iterations, $L$ is sampled uniformly from
$[L_{\min},L_{\max})$, and $a$ and $b$ are sampled from normal distributions
with their standard errors. This results in a set of $n$ samples of $M$, which
are then converted to the likelihood function $p(L|M)$ through a kernel density
estimation.

We then use $p(L|M)$ to recover the postererior magnitude $p(M|D,L)$ with the 
equation
$$ p(M|D,L) = p(M) \, p(L|M)\, \frac{p(D|M)}{p(D)} \; .$$ {#eq:pmdl} 
An example of this calculation is show in Figure \ref{example_pdf}. 

![Schematic showing Eqn @eq:pmdl for an earthquake
\label{example_pdf}](./figures/pdf_mult.pdf)

## Computation

Code to perform these calculations is incorporated into *culpable*, an
open-source Python library for various fault-related calculations [*Styron,
2016*; https://github.com/cossatot/culpable/]. The paleoearthquake magnitude
calculations rely heavily on the *NumPy* [*Oliphant, 2007*; *van der Walt et
al., 2011*], SciPy [*Jones et al., 2011*], and *Pandas* [*McKinney, 2010*]
packages. A script used to calculate $p(M|D,L)$ for all events in this work is
included in the supplementary information.


# Results

## Magnitudes of Puget Lowland paleoearthquakes

Individial paleoearthquakes in the Puget Lowland have maximum posterior
magnitudes between 6.2 and 7.7, given both offset and rupture length data
(Figures \ref{post_pdfs}, \ref{post_scatter}). In general, the larger
earthquakes are less common, although there are relatively few earthquakes
below $M$ 6.5, consistent with previous observations that $M$ 6.5 and smaller
events frequently do not break the surface [e.g., *Fialko et al., 2005*].

![Posterior magnitude PDFs for Puget Lowland earthquakes. **a**: $p(M|D)$.
  **b**: $p(M|D,L).$ \label{post_pdfs}](./figures/posterior_pdfs.pdf)


### Effects of length incorporation

Incorporating length into the magnitude inversion substantially reduced both
the posterior magnitudes and the uncertainty in the magnitudes. $p(M|D,L)$ was
about 0.4 $M$ smaller than $p(M|D)$ for the same event, on average. The
uncertainty in each estimate is fairly represented by the interquartile range
(IQR, the distance between the 25th and 75th percentiles); the IQR of $p(M|D)$
is, on average, twice the IQR of $p(M|D,L)$ for a given earthquake (Figure
\ref{post_scatter}).

Additionally, the characteristic shape of the $p(M|D)$ PDF has a right skew
(Figure \ref{post_pdfs}a), with a long, high-$M$ tail (relating to the
possibility that the offset measurement occurred on a section of rupture with
an offset distance much lower than the mean offset), though $p(M|D,L)$ is more
symmetrical (Figure \ref{post_pdfs}b). In this analysis, $p(M)$ extended to $M$
8.5, and $p(M|D)$ for several events are non-negligibly truncated at this
limit. However, for no events did $p(M|D,L)$ reach 8.0. This is an effect of
limiting the rupture length, and given the geological controls on fault
dimensions, this is highly unlikely to be simply an underestimation of the
possible rupture dimensions, as could be the case for a 1000 km long
strike-slip fault. 

The only instance in which we feel that rupture could be longer than our
maximum is if the Saddle Mountains and Seattle Fault Zone ruptured in a single
event. This is possible given the estimated timing of the paleoearthquakes: the
Restoration Point earthquake occurred about 1050-1020 calendar years BP (before
1950), the Saddle Mountains East fault ruptured between 1160-310 cal. yr. BP,
and the Saddle Mountains West fault ruptured between 1200-970 cal. yr. BP
[*Sherrod et al., 2000*, *Nelson et al., 2003*, *Witter et al., 2008*, *Barnett
et al., 2015*] (these Saddle Mountains ruptures are considered the same event
in this work). These faults have geometries and kinematics that are not
incompatible: The SMF strikes ~60° and is reverse-dextral while the SFZ strikes
~90° and is reverse. These faults have not been demonstrated to link at depth,
though this has been suggested by *Blakely et al.* [*2009*] based on
interpretation of geological and geophysical data. Furthermore, both of these
events show much larger offsets than the rest in our dataset: a mean of 10.2 m
on the SFZ and 6.7 m on the SMF. Simultaneous rupture of > 5 m on separate
faults with such different strikes and rakes have not been observed, although
the 2008 Wenchuan, China [*Zhang et al., 2011*] and 2016 Kaikoura, New Zealand
earthquakes, both $M$ ~7.9, are close enough to demonstrate the possibility.
The total rupture length of this event would be ~70-150 km, and cursory
analysis indicates a most-likely magnitude of 7.8, though the PDF extends to
$M$ 8.3.


![Scatterplot comparing $p(M|D)$ and $p(M|D,L)$ for each event. Points
  represent the median for each posterior PDF, and error bars represent the
  25th and 75th percentiles. Earthquakes that plot below the black dashed line
  have had posterior magnitudes reduced by the incorporation of length data
  into the magnitude inversions. \label{post_scatter}
  ](./figures/posterior_scatter.pdf)



## Implications for Puget Lowland seismic hazard

The reduction in posterior earthquake magnitudes caused by the incorporation of 
rupture length information directly reduces seismic hazard estimates that are 
based on paleoseismic data. Ground-motion prediction equations are frequently 
of the form $PGA \propto e^M$, where PGA is peak ground acceleration. With this 
exponential scaling, a decrease in 0.5 $M$ reduces PGA by about half. 
Furthermore, the reduction in the higher end of the posteriors---in particular 
the long, high-$M$ tails of $p(M|D)$---are greater than the reduction in mean
or median posterior magnitude, and represent a greater increase in estimated
seismic safety. 

However, the earthquakes studied here, though representing a mostly-complete
record of surface-breaking earthquakes in the Puget Lowland, are far from the
only source of regional seismic hazard, as the area is above the Cascadia
subduction zone. The reduction in earthquake magnitude and hazard given here
only concerns these shallow, upper-plate events and does not reduce the hazard
from Cascadia at all.

Furthermore, though our results indicate a decrease in estimated magnitude for
the earthquakes studied relative to estimates only incorporating offset data,
they still demonstrate that strong earthquakes occur at shallow depths in a
populous region. The largest paleoearthquake, the $M$ 7.7 ca. 1000 A.D.
Restoration Point earthquake, occured on a branch of the Seattle Fault Zone
that underlies a dense part of the city with a high concentration of
unreinforced masonry buildings. A repeat of this event would devastate Seattle.

# Conclusions

The incorporation of earthquake rupture lengths into magnitude estimates for 27
paleoearthquakes in the Puget Lowland region of Washington increases the
precision and decreases the magnitudes of the posterior magntude estimates
$p(M|D,L)$ relative to $p(M,D)$, which only incorporates offset measurements,
in spite of the factor of 10 uncertainty in the length estimates. This is
largely because the rupture lengths are quite short relative to the offsets.
These improved posteriors reduce both the uncertainty and hazard of earthquakes
in the region.

# References

Barnett, E. A., Sherrod, B. L., Hughes, J. F., Kelsey, H. M., Czajkowski, J.
L., Walsh, T. J., ... & Carson, R. J. (2015). Paleoseismic Evidence for Late
Holocene Tectonic Deformation along the Saddle Mountain Fault Zone,
Southeastern Olympic Peninsula, Washington. *Bulletin of the Seismological
Society of America, 105*(1), 38-71.

Biasi, G. P., & Weldon, R. J. (2006). Estimating surface rupture length and
magnitude of paleoearthquakes from point measurements of rupture displacement.
*Bulletin of the Seismological Society of America, 96*(5), 1612-1623.

Blakely, R. J., Sherrod, B. L., Hughes, J. F., Anderson, M. L., Wells, R. E., &
Weaver, C. S. (2009). Saddle Mountain fault deformation zone, Olympic
Peninsula, Washington: Western boundary of the Seattle uplift. *Geosphere,
5*(2), 105-125.

Fialko, Y., Sandwell, D., Simons, M., & Rosen, P. (2005). Three-dimensional
deformation caused by the Bam, Iran, earthquake and the origin of shallow slip
deficit. *Nature, 435*(7040), 295-299.

Hemphill-Haley, M. A., & Weldon, R. J. (1999). Estimating prehistoric
earthquake magnitude from point measurements of surface rupture. *Bulletin of
the Seismological Society of America, 89*(5), 1264-1279.

Jones E, Oliphant E, Peterson P, et al. SciPy: Open Source Scientific Tools for
Python, 2001-, http://www.scipy.org/ [Online; accessed 2017-01-31].

Mazzotti, S., Dragert, H., Hyndman, R. D., Miller, M. M., & Henton, J. A.
(2002). GPS deformation in a region of high crustal seismicity: N. Cascadia
forearc. *Earth and Planetary Science Letters, 198*(1), 41-48.

McKinney, W. (2010), Data structures for statistical computing in Python, in
*Proceedings of the 9th Python in Science Conference*, edited by S. van der
Walt and J. Millman, pp. 51–56, SciPy, Austin, Tex.

Nelson, A. R., Johnson, S. Y., Kelsey, H. M., Wells, R. E., Sherrod, B. L.,
Pezzopane, S. K., ... & Bucknam, R. C. (2003). Late Holocene earthquakes on the
Toe Jam Hill fault, Seattle fault zone, Bainbridge Island, Washington.
*Geological Society of America Bulletin, 115*(11), 1388-1403.

Nelson, A. R., Personius, S. F., Sherrod, B. L., Kelsey, H. M., Johnson, S. Y.,
Bradley, L. A., & Wells, R. E. (2014). Diverse rupture modes for
surface-deforming upper plate earthquakes in the southern Puget Lowland of
Washington State. *Geosphere*, GES00967-1.

Oliphant, T. E. (2007), Python for scientific computing, *Comput. Sci. Eng.,
9*(3), 10–20.

Sherrod, B. L., Bucknam, R. C., & Leopold, E. B. (2000). Holocene relative sea
level changes along the Seattle Fault at Restoration Point, Washington.
*Quaternary Research, 54*(3), 384-393.

Styron, R.S. (2016). culpable v. 0.1 [Software code]. Zenodo.
https://doi.org/xxx

Walt, S. V. D., Colbert, S. C., & Varoquaux, G. (2011). The NumPy array: a
structure for efficient numerical computation. *Computing in Science &
Engineering, 13*(2), 22-30.

Wells, D. L., & Coppersmith, K. J. (1994). New empirical relationships among
magnitude, rupture length, rupture width, rupture area, and surface
displacement. *Bulletin of the Seismological Society of America, 84*(4),
974-1002.

Witter, R. C., Givler, R. W., & Carson, R. J. (2008). Two post-glacial
earthquakes on the Saddle Mountain West fault, southeastern Olympic Peninsula,
Washington. *Bulletin of the Seismological Society of America, 98*(6),
2894-2917.

Zhang, G., Qu, C., Shan, X., Song, X., Zhang, G., Wang, C., ... & Wang, R.
(2011). Slip distribution of the 2008 Wenchuan Ms 7.9 earthquake by joint
inversion from GPS and InSAR measurements: a resolution test study.
*Geophysical Journal International, 186*(1), 207-220.


# Supplemental figures

![$p(M|D,L)$ (blue lines) and $(p(M|D)$ (green dashed lines) for all events,
  with their unique event name. \label{all_pms}
  ](./figures/post_magnitude_stack.pdf)
