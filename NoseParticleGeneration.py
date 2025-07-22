"""
Nose Particle Generation Simulation
===================================
Simulates respiratory droplet particle generation from mouth and nostrils
during breathing cycles for CFD analysis.

Author: Hossein Seyedzadeh
Date: 2023-01-25 (last updated)
Version: 2.0
"""

import math
import random

# === DEBUG CONFIGURATION ===
DEBUG = False
# DEBUG = True

# === OUTPUT FORMATTING FUNCTIONS ===
def Output(ti, pId, coord, file_handle):
    """
    Output particle data in standard CFD format to file.
    
    Args:
        ti: Time step (converted to seconds by dividing by 1000)
        pId: Particle ID
        coord: 3D coordinate array [x, y, z]
        file_handle: File handle to write data to
        
    Returns:
        Incremented particle ID
        
    Output format: x y z u v w start_time diameter density particle_id
    - Position: coord[0], coord[1], coord[2] 
    - Velocity: 0.0, 0.0, 0.0 (initially at rest)
    - Start time: ti/1000.0 (convert ms to seconds)
    - Diameter: 10.0e-6 (10 micrometers)
    - Density: 977.0 kg/m³ (water droplet density)
    """
    file_handle.write('{:.15f}\t{:.15f}\t{:.15f}\t0.0\t0.0\t0.0\t{:7.3f}\t10.0e-6\t977.0\t{}\n'.format(
        coord[0], coord[1], coord[2], ti / 1000.0, pId))
    #file_handle.write('{:.15f}\t{:.15f}\t{:.15f}\t0.0\t0.0\t0.0\t{:7.3f}\t10.0e-6\t977.0\n'.format(
    #    coord[0], coord[1], coord[2], ti / 1000.0))
    return pId + 1

def OutputStar(ti, pId, coord, file_handle):
    """
    Output particle data in simplified star format to file.
    
    Args:
        ti: Time step (unused in this format)
        pId: Particle ID  
        coord: 3D coordinate array [x, y, z]
        file_handle: File handle to write data to
        
    Returns:
        Incremented particle ID
        
    Output format: v, particle_id, x, y, z
    """
    file_handle.write(f'v, {pId+1}, {coord[0]:.15f}, {coord[1]:.15f}, {coord[2]:.15f}\n')
    return pId + 1

# Choose which output function to use
whichOutput = Output
# whichOutput = OutputStar

# === SIMULATION PARAMETERS ===

# --- Timing Configuration ---
# Version 2: Output 5 particles every 5 ms
# Each time step is 5 ms
# Total current time steps = 20,000 (currently running 100,005 for ~100s)
# Planning to extend to 30,000 time steps = 150 s

# --- Breathing Cycle Parameters ---
# Breath cycle = 5 s = 5000 ms
# Exhale phase: 2.5 s (first half of cycle)
# For exhale: 2.5 s / 0.005 s = 500 particles per exhale cycle
# Released from time steps 0 to 360 (1.8 s)
# Use modulo operation (ti % 5000) to determine particle release timing

# Loop: range(0, 150005, 5)  # 5 ms resolution in integer arithmetic
# (0.005 s * 1000 = 5, 2.5 s * 1000 = 2500)

# --- Mesh Coordinate System ---
# For the nose simulation, the mesh was adjusted so that the mouth is centered at y = 0.
# Previous simulation was centered around y = 1.0

# --- Mouth Particle Generation Area ---
xPln = 0.0015                    # X-plane position for mouth particles
ymin = 3.351                    # Minimum Y coordinate
ymax = 3.391                    # Maximum Y coordinate
ydel = ymax - ymin              # Y-axis range for mouth particles
zmin = 1.678                    # Minimum Z coordinate for mouth particles
zmax = 1.6881                   # Maximum Z coordinate for mouth particles
zdel = zmax - zmin              # Z-axis range for mouth particles

# === NOSTRIL PARAMETERS ===

# --- Nostril Geometry ---
# Nostril particle generation radius
# Original radius = 0.00375 (put some particles outside the fastest nose velocity)
# Updated radius as of 2023-01-25 for better particle distribution
radius = 0.001875

# --- Nostril Transformation Matrices ---
# 3D rotation and translation matrices to position nostril particles
# Format: [[rotation matrix], [translation vector]]
# Each matrix transforms local nostril coordinates to global 3D space

# Left nostril transformation matrix
leftRotTrans = [ [ 0.948, 0.000, -0.319, 0.00573 ],
                 [ 0.000, 1.000,  0.000, -0.00875 ],
                 [ 0.319, 0.000,  0.948, 1.71177 ] ]

# Right nostril transformation matrix  
rightRotTrans = [ [ 0.948, 0.000, -0.319, 0.00573 ],
                  [ 0.000, 1.000,  0.000, -0.00875 ],
                  [ 0.319, 0.000,  0.948, 1.71177 ] ]

# === LEGACY TRANSFORMATION MATRICES (for reference) ===
# Original values that put some particles outside the fastest nose velocity:
# leftRotTrans = [ [ 0.948, 0.000, -0.319, 0.007 ],
#                  [ 0.000, 1.000,  0.000, -0.00875 ],
#                  [ 0.319, 0.000,  0.948, 1.7122 ] ]
# rightRotTrans = [ [ 0.948, 0.000, -0.319, 0.007 ],
#                   [ 0.000, 1.000,  0.000, -0.00875 ],
#                   [ 0.319, 0.000,  0.948, 1.7122 ] ]

# === MAIN SIMULATION FUNCTIONS ===

def NoseParticleGeneration():
    """
    Main function to generate particle data for nose and mouth breathing simulation.
    
    Generates particles during exhale phase of breathing cycles:
    - 5 mouth particles per 5ms time step
    - 2 particles per nostril (4 total) per 5ms time step
    - Only during exhale phase (first 2.5s of each 5s cycle)
    
    Writes data to ParticleInitial.dat file.
    """
    # Enable debugging if needed
    if DEBUG:
        import pdb;
        pdb.set_trace()

    # === DEVELOPMENT/TESTING CODE (commented out) ===
    # Code for generating nostril outline visualization
    # '''
    # # Generate an outline circle
    # pId = 300
    # numSides = 36
    # for i in range(numSides):
    #     cood = RotTrans(leftRotTrans, [radius * math.cos(2*i*math.pi/36),
    #                                    radius * math.sin(2*i*math.pi/36), 0.0 ])
    #     pId = OutputStar(0, pId, cood, file_handle)
    # 
    # cood = RotTrans(leftRotTrans, [ 0.0, 0.0, 0.0 ])
    # pId = OutputStar(0, pId, cood, file_handle)
    # return
    # '''
    
    # Open output file for writing
    with open('ParticleInitial.dat', 'w') as file_handle:
        # Initialize particle counter
        pId = 0
        
        # Write header for output file
        if whichOutput == Output:
            # Header lines are commented out for now
            file_handle.write('# location velocity "start time" diameter  density\n')
            file_handle.write('# x y z       u v w\n')
            pass

        # === MAIN SIMULATION LOOP ===
        # Note: Currently iterating up to 100,005 timesteps (reduced from planned 200,005)
        # Original plan was 40,000 timesteps, comments mention 20,000 timesteps
        # I'm only iterating up to 20000 timesteps instead of 40000.
        # for ti in range(0, 200005, 5):
        for ti in range(0, 200005, 5):
            # Calculate position within breathing cycle (5000ms = 5s cycle)
            tm = ti % 5000
            
            # Generate particles only during exhale phase (first 2500ms of cycle)
            if tm >= 0 and tm < 2500:
                
                # --- Generate Mouth Particles ---
                # Generate 5 randomly distributed particles in mouth area
                for i in range(0,5):
                    rydel = random.uniform(0.0, ydel)
                    y = ymin + rydel
                    rzdel = random.uniform(0.0, zdel)
                    z = zmin + rzdel
                    pId = whichOutput(ti, pId, [ xPln, y, z ], file_handle)

                # --- Generate Nostril Particles ---
                # Generate 2 particles per nostril (4 total)
                pId = GenNostril(ti, radius, pId, leftRotTrans, file_handle)
                pId = GenNostril(ti, radius, pId, rightRotTrans, file_handle)
    
    print(f"Particle data written to ParticleInitial.dat with {pId} particles.")

def GenNostril(ti, radius, pId, rotTrans, file_handle):
    """
    Generate particles for a single nostril.
    
    Args:
        ti: Current time step
        radius: Nostril radius for particle generation
        pId: Current particle ID counter
        rotTrans: 4x3 transformation matrix for nostril positioning
        file_handle: File handle to write data to
        
    Returns:
        Updated particle ID counter
        
    Generates 2 particles randomly distributed within circular nostril area.
    Uses rejection sampling to ensure particles fall within circular boundary.
    """
    x = 0.0
    y = 0.0

    # Generate 2 particles per nostril per time step
    for i in range(0,2):
        # Use rejection sampling to generate particles within circular nostril
        while True:
            # Generate random coordinates within square [-radius, radius]
            # These calculations provide the best particle distribution throughout
            # the model volume according to testing
            x = radius * random.uniform(-1.0, 1.0)
            y = radius * random.uniform(-1.0, 1.0)
            
            # Accept only if point falls within circle
            if x*x + y*y < radius*radius:
                break

        # Transform local nostril coordinates to global 3D space
        coord = RotTrans(rotTrans, [ x, y, 0.0 ])
        pId = whichOutput(ti, pId, coord, file_handle)

    return pId

def RotTrans(rotTrans, coord):
    """
    Apply 3D rotation and translation transformation to coordinates.
    
    Args:
        rotTrans: 4x3 transformation matrix [rotation + translation]
        coord: 3D coordinate vector [x, y, z]
        
    Returns:
        Transformed 3D coordinate vector
        
    Transformation matrix format:
    [[r11, r12, r13, tx],
     [r21, r22, r23, ty], 
     [r31, r32, r33, tz]]
    
    Where r_ij are rotation matrix elements and tx,ty,tz are translation offsets.
    """
    return [ rotTrans[0][0] * coord[0] + rotTrans[0][1] * coord[1]
             + rotTrans[0][2] * coord[2] + rotTrans[0][3],
             rotTrans[1][0] * coord[0] + rotTrans[1][1] * coord[1]
             + rotTrans[1][2] * coord[2] + rotTrans[1][3],
             rotTrans[2][0] * coord[0] + rotTrans[2][1] * coord[1]
             + rotTrans[2][2] * coord[2] + rotTrans[2][3] ]

# === PROGRAM ENTRY POINT ===
if __name__ == '__main__':
    NoseParticleGeneration()


