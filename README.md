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
- **Multiphase Flows**: Bubble tracking, droplet dynamics, solid particle transport
- **Material Processing**: Powder flows, granular materials, coating processes

## Output Format
Generates `ParticleInitial.dat` with:
- 3D position coordinates (x, y, z)
- Initial velocity components (u, v, w)
- Injection time
- Particle diameter
- Particle density
- Unique particle IDs

## Use Cases
- OpenFOAM Lagrangian particle tracking
- ANSYS Fluent DPM (Discrete Phase Model)
- COMSOL particle tracing
- Custom CFD solver particle initialization
- Experimental validation data generation

## Customization
- Modify injection geometries (currently configured for respiratory sources)
- Adjust temporal injection patterns
- Configure particle properties for specific applications
- Add new output formats for different CFD solvers
