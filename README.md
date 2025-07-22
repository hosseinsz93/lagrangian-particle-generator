# Lagrangian Particle Generator

A flexible Python toolkit for generating initial particle conditions for Lagrangian particle tracking simulations in Computational Fluid Dynamics (CFD) software.

## Features
- **Multi-Source Injection**: Generate particles from multiple geometric sources (planes, circles, complex shapes)
- **Temporal Control**: Configurable time-based particle release patterns and cycles
- **3D Transformations**: Rotation and translation matrices for complex geometry positioning
- **Flexible Output Formats**: Standard CFD format and custom output options
- **Rejection Sampling**: Accurate particle distribution within complex geometries
- **Configurable Properties**: Particle size, density, initial velocity, and timing control

## Applications
- **Environmental Flows**: Pollutant dispersion, sediment transport, atmospheric particles
- **Industrial Processes**: Spray drying, combustion modeling, chemical reactors
- **Biomedical**: Drug delivery, blood flow particles, respiratory droplets

## Output Format
Generates `ParticleInitial.dat` with:
- 3D position coordinates (x, y, z)
- Initial velocity components (u, v, w)
- Injection time
- Particle diameter
- Particle density
- Unique particle IDs

