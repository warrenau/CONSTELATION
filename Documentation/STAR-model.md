# STAR-CCM+ Model

This document details the STAR-CCM+ portion of **CONSTELATION**. Obtaining, verifying, and validating the model is up to the user. 

---

## Import CAD Model

Help from *NieDesign* on [YouTube](https://www.youtube.com/channel/UCMN7B3Im9NFivSo6b1203_w/videos).

1. `import surface mesh` button
    - select file
    - `create new part`
    - `fine` or `very fine` tessalation density
2. Split surfaces
    - right click on `faces`
    - `Split by patch`
    - select faces and name surfaces
3. Mesh and Regions
    - prepare surfaces for meshing `Surface Preparation`
    - `Boolean` if needed
    - `Mesh`
        - Automatic Surface Repair
        - Select volume mesher
            - polyhedral mesh for volume mesher
            - prism layer mesher for boundary layer
    - Fluid region