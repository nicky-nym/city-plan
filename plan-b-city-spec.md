# Plan-B City — Design Specification (Gen 4)
 
## 1. Premise and scope
 
This project explores the optimal building geometry for a "platonic city": a flat plain divided into a square grid, with one identical building on every grid square, each building flush against all four neighbors. Because every facade abuts a neighbor, the city is effectively one continuous building of unbounded extent, and all daylight must arrive from above — through roofs, skylights, or voids (courtyards and light wells) carved into the mass. The design problem is therefore: choose the height, void pattern, and roofscape that maximize the value of floorspace created, net of construction cost.
 
The current application target is a greenfield site of roughly 7 × 7 miles (about 49 sq mi, 1.37 billion sf of land), intended to house on the order of 10 million people across housing, office, retail, and warehouse uses (roughly 620 sf of floorspace per person at the achieved density). Circulation uses no cars, buses, or rail: only pedestrian ways and a grid of 15-mph lanes for bike-sized vehicles (bikes, e-bikes, cargo bikes, pedicabs, scooters, kei-class microcars), with grade-separated intersections. Buildings contain no stairs, steps, elevators, or lifts; all vertical movement is by gently sloped ramped corridors.
 
## 2. Fixed model assumptions
 
These parameters define the scoring model. They are deliberately simple and are the first candidates for replacement with real-world data.
 
| Parameter | Value | Notes |
|---|---|---|
| Story height | 12 ft | Floor-to-floor |
| Useful daylight depth | 25 ft | From a window wall; implies 50-ft floorplates lit from both sides |
| Daylight adequacy rule | 45° sky angle | A window is "fully lit" if unobstructed at 45°; a courtyard must be as wide as the walls around it are tall |
| Construction cost | $1,000/sf at 1 story, +$100/sf per additional story | Applies to all floorspace in the building; equivalently, the marginal cost of floor k is $800 + $200k (floor 1 = $1,000, floor 7 = $2,200, floor 8 = $2,400) |
| Value: windowed floorspace | $3,000/sf | Window with 45° sky |
| Value: skylit floorspace | $2,500/sf | Roof light, no view window |
| Value: dark floorspace | $800/sf | Below even ground-floor cost, so dark space is never built |
 
Scoring metric: net value per square foot of land ("land utility") — gross floorspace value minus construction cost, per sf of land. Because every grid square must be built, land is the fixed resource and maximizing per-sf net value maximizes the city. ROI (value ÷ cost) was considered and rejected as a primary metric because it rewards margin over magnitude and degenerates toward one-story carpets.
 
## 3. Gen 4 design specification
 
The repeating module is 134 × 134 ft, organized into 402-ft supermodules of 3 × 3 modules.
 
Primary massing: a continuous waffle lattice of 50-ft-deep floorplate bands, seven stories (84 ft) tall, enclosing one square courtyard per module, 84 × 84 ft, open to the sky for the full building height. Every square foot of the seven main floors is within 25 ft of a court-facing window with a 45° sky angle (windowed grade). Service cores (plumbing, utilities; no elevators needed) occupy the naturally dark 50 × 50 ft band intersections.
 
Court pavilions: each courtyard contains a one-story, fully skylit pavilion of 60 × 60 ft, centered, leaving a 12-ft open moat on all sides. The pavilion top sits exactly at the 45° sight line from the surrounding ground-floor sills, so it blocks no daylight. Its roof is a planted garden. Pavilions must remain one story: any upper tier shades the skylights of the floor below, converting +$1,500/sf space into −$200/sf space (a net −$400 per transferred sf).
 
Setback penthouses: an eighth-floor penthouse lattice, 26 ft wide, runs along the centerline of every band, set back 12 ft from each court edge (staying under the 45° planes as they continue above the parapets), flanked by 12-ft roof terraces. A second tier is geometrically impossible (24-ft setbacks leave 2 ft of floorplate). Governing principle: roofs divide into those that are a floor's sole light source (pavilion roofs — unbuildable) and those above side-lit space (band roofs — buildable to the 45° envelope).
 
Vehicle circulation: every third band in each direction (402-ft spacing) is a street band carrying a 32-ft arcade — two 10-ft lanes plus sidewalks — through the building at 15 mph, with floors above on columns. North–south lanes run at ground level; east–west lanes run at level 2 inside their bands, so every intersection is grade-separated by construction (12-ft clearance). Turning and access movements use ~4% ramp lanes, which climb one story in ~300 ft, within the 402-ft intersection spacing. No land is unroofed for streets, and there are no parking lots (small-vehicle racks line the arcades).
 
Pedestrian circulation and the no-stairs rule: each courtyard's perimeter gallery (cloister) is tilted into a continuous helix at 1:30 (3.3%); one ~360-ft lap of the court equals one story of rise. Galleries are 8 ft wide and admit cargo trikes at walking speed, so every floor has direct wheeled freight access. Short bridges cross the moat from each pavilion roof to the level-2 gallery. Floor 7 is about an 8-minute walk or a 2–3 minute ride from ground.
 
Circulation performance: average Manhattan-distance trip in the 7-mi square ≈ 4.7 mi ≈ 19 min at a nonstop 15 mph; average door-to-door commute ≈ 25 min including vertical access. The 92 × 92 lane grid has throughput far above demand for 10M residents.
 
## 4. Design lineage and scorecard
 
| Metric (per sf of land) | Gen 1: waffle | Gen 2: + pavilions | Gen 3: + penthouses | Gen 3 + traditional streets | Gen 4: ramp city |
|---|---|---|---|---|---|
| Saleable FAR | 4.25 | 4.45 | 4.80 | 3.36 | 4.57 |
| Ground coverage | 61% | 81% | 81% | ~57% | 81% |
| Gross value | $12,748 | $13,249 | $14,300 | $10,010 | $13,606 |
| Construction cost | $6,799 | $6,999 | $7,840 | $5,488 | $7,840 |
| Net value (land utility) | $5,949 | $6,250 | $6,460 | $4,522 | $5,766 |
| Avg commute | n/a | n/a | n/a | 30–45 min | ~25 min |
 
Gen 4 charges circulation at ~4.8% of gross floorspace (3.3% arcades + 1.5% ramp allowance), built at full cost with zero sale value. The traditional-streets column assumes 30% of land surrendered to roads and parking. Note that the gen 1 optimum (7 stories, FAR ~4.25) independently reproduces the classic European perimeter block (Paris, Barcelona Eixample), which is a useful sanity check on the daylight economics.
 
## 5. Known weaknesses and open modeling questions
 
The three-tier value model ($3,000 / $2,500 / $800) is coarse; real daylight value is continuous in sky angle and floor depth. Upper-floor value is not discounted for ramp access time (floor 7 ≈ 8-min walk), nor credited for door-to-door freight access; both effects are unmodeled. The cost schedule is linear in height and ignores structure for arcades, ramps, and bridges. Corridor/circulation area inside ordinary floorplates was never charged in any generation, so cross-generation comparisons are fair but absolute FARs are slightly optimistic. Fire egress, drainage of open moats and courts, wind, and solar orientation (the 45° rule is orientation-blind) are all unaddressed. The 30-minute commute claim uses uniform random origin–destination pairs; real trip distributions would likely do better.
 
## 6. Roadmap
 
Candidate next steps: replace the cost model with real construction cost data (e.g., RSMeans-class $/sf by height class); replace the value model with real rent/price gradients by daylight, floor, and use; traffic microsimulation of the two-level lane grid (capacity, intersections, worst-case trips); carbon footprint of construction and operation vs conventional cities; water, sewage, and stormwater sizing for 10M people under 81% coverage; parks and greenspace accounting (courts, moats, pavilion roofs, terraces) vs benchmarks; 3D visualization of the supermodule; and quantitative comparisons against New York, San Francisco, Paris, and Hong Kong on FAR, coverage, commute, and floorspace per capita.
