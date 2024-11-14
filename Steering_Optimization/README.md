## WORKFLOW
1. Set up simulation parameters in Run_Optimizaiton.py
2. Run Run_Optimizaiton.py with sys arguments of the search resolution and desired output filename (e.g test.csv)
    - ex: if I wanted to run at a 3mm resolution and dump the output to the file 'example.csv', I would use the command: python Run_Optimization.py 3 example.csv
3. Visualize results with Visualize_steering.py with sys argument of the filename to read

# Notes
- I am including the output file 'example.csv' which I ran with arbirary geometry at 2mm resolution retaining 5 geometries
- Please update your .gitignore to not upload any output files if you are pushing
