---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(launch:thebe)=
## Code


```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt

ϵ_values = np.random.randn(100)
plt.plot(ϵ_values)
plt.show()
```

<!-- ```{code-cell} ipython3
from myst_nb import glue
my_variable = "here is some text!"
glue("cool_text", my_variable)
```
 -->
<!-- ```{code-cell} ipython3
:tags: [hide-input, thebe-init]

my_hidden_variable = 'wow, it worked!'
```

```{code-cell} ipython3
# The variable for this is defined in the cell above!
print(my_hidden_variable)
```
 -->

