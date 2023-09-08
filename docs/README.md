# cloneReference
**cloneReference** is a tool for Maya to clone or create multiple copies of external references keeping transforms from initial reference.

<img src="https://github.com/AlbertoGZ-dev/gzCloneReference_Maya/blob/master/docs/gzCloneReference.png"></img>

## Setup
Download package from [here](https://github.com/AlbertoGZ-dev/gzCloneReference_Maya/releases/)

### Automatic installation
1. Close all instances of any opened version of Maya.
2. Run the installer for your plattform.

    - Windows by double clicking *install_win.bat* file.
    - MacOS by double clicking *install_mac* file.
    - Linux open shell and execute *install_linux.sh* file.

Note: on MacOS and Linux you may need to set execution permissions the installer file. Ex. *chmod +x install_linux.sh*

#### Manual installation

Place the *cloneReference.py* and *\_\_init\_\_.py* files in a folder named *cloneReference* in your Maya scripts directory and create a python shell button with the following code:

```python
from cloneReference import cloneReference

try:
    md_win.close()
except:
    pass
md_win = cloneReference.cloneReference(parent=cloneReference.getMainWindow())
md_win.show()
md_win.raise_()
```
