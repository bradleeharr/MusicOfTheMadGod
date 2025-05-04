from pathlib import Path
import os


import yaml

def no_children():
    pass

def generate_ref():
    root = Path("ref/")
    if root.exists():
        print(f"Reference directory {root.absolute()} already exists! Please delete this directory and rerun to regenerate songs.")
        return
    
    os.mkdir(root)
    with open("./config.yaml", "r") as f:
        y = yaml.load(f, Loader=yaml.FullLoader)


        print(y.keys())

        for k in y.keys():

            print(y[k])



            os.mkdir(Path(root, k))

        
if __name__ == '__main__': 
    generate_ref()