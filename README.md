# Clone Reference
Clone Reference is a tool for Maya to clone or create multiple copies of external references keeping transforms from initial reference.

<img src="https://github.com/AlbertoGZ-dev/cloneReference/blob/main/cloneReference.png"></img>

## Setup

#### Manual installation

Place the *cloneReference.py* and *\_\_init\_\_.py* files in a folder named *cloneReference* in your Maya scripts directory and create a python shell button with the following code:

```python
from cloneReference import matchMcloneReferenceultiObject

try:
    md_win.close()
except:
    pass
md_win = cloneReference.cloneReference(parent=cloneReference.getMainWindow())
md_win.show()
md_win.raise_()
```
