# Bike Geometry Visualiser

Parse and plot bicycle frame geometry from a simple text file. Produces detailed 2-D side-view diagrams with all key measurements annotated, and supports overlaying multiple bikes for comparison.

## Features

- Renders a full frame side-view: tubes, wheels, saddle, stem, handlebars
- Annotates ~17 dimensions: reach, stack, wheelbase, seat tube, head tube, fork rake, stem length, spacers, and more
- Angle arcs for head angle and seat angle
- 3-D saddle-to-handlebar distance (accounts for bar width)
- Multi-bike comparison overlay with per-bike colour coding

## Requirements

```
python >= 3.9
numpy
matplotlib
```

## Input file format

A plain-text, tab-separated (or whitespace-separated) file with one measurement per line:

```
Head Angle      73.0
Seat Angle      73.5
Stack           590
Reach           385
Head Tube       140
Seat Tube C-C   530
Top Tube (effective)    560
Chainstay       415
BB Drop         70
Front Centre    595
Wheelbase       1010
Fork Rake / Offset  50
Seat height     720
Spacers         20
Stem length     100
Stem Angle      6.0
Bar width       420
```

All linear values are in **mm**; angles in **degrees**.

## Usage

### Single bike plot

```python
from Geometry import Geometry
import matplotlib.pyplot as plt

G = Geometry('my_bike.txt')

fig, ax = plt.subplots(figsize=(18, 10))
G.plot_bike(fig, ax)
plt.show()
```

![alt text](https://github.com/honzascholtz/Bike_geometry/blob/main/Figures/Ribble_Endurance_L.png "Example of the UI")

### Multi-bike comparison

See `Geometry_comp.ipynb` for a worked example overlaying four bikes:

```python
from Geometry import Geometry
import matplotlib.pyplot as plt

G = Geometry('bike_a.txt')

fig, ax = plt.subplots(figsize=(12, 6))
G.plot_comp(fig, ax, 'bike_a.txt', color='blue')
G.plot_comp(fig, ax, 'bike_b.txt', color='orange')
G.plot_comp(fig, ax, 'bike_c.txt', color='green')

ax.legend()
plt.show()
```
![alt text](https://github.com/honzascholtz/Bike_geometry/blob/main/Figures/Comp_bikes.png "Example of the UI")


## Coordinate system

Origin is the **Bottom Bracket centre**.

| Axis | Direction |
|------|-----------|
| +x   | toward front wheel |
| +y   | upward |

## Key computed points

| Point | Derivation |
|-------|-----------|
| `rear_axle` | `(-sqrt(chainstay² - bb_drop²), bb_drop)` |
| `front_axle` | `(front_centre, bb_drop)` |
| `ht_top` | `(reach, stack)` |
| `ht_bottom` | `ht_top + head_tube × (cos ha, −sin ha)` |
| `seat_frame_top` | `bb + seat_tube_cc × (−cos sa, sin sa)` |
| `seat_pos` | `bb + seat_height × (−cos sa, sin sa)` |
| `stem_end` | `spacer_top + stem_length × (cos α, −sin α)` |

## File structure

```
Bike_geometry/
├── Geometry.py          # Geometry class: loader, point computation, plotting
├── Geometry_comp.ipynb  # Example notebook: 4-bike comparison
└── README.md
```
