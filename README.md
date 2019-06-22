# Manga K

This is a program written in python and serves its purpose on console
___
### To Start:
> run main.py

___
### Features:
* Search for manga
* Download manga from mangakakalot or manganel
* View download manga in the default browser
* Composite each chapter into a single image

### Compiling
* Run
```batch
    py -m PyInstaller main.py --onefile --clean
```

### Additional info:
* In case ```style.css``` has been modified, run ```stgen.py``` before compiling to update ```modules/styles.py```
* If ```style.css``` is missing, it is generated upon running main program