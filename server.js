const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const app = express();

app.use(cors());
app.use(express.json());

app.listen(5000, () => {
  console.log("Server has started on port 5000");
});

app.post("/habitable-exoplanet-calculator", async (req, res) => {
  try {
    const {
      R_star,
      L_star,
      T_eff,
      R_planet,
      M_planet,
      semi_major_axis,
      eccentricity,
      inclination,
      albedo,
      distance,
      D_telescope,
      wavelength,
      IWA,
      OWA,
      contrast_limit,
    } = req.body;

    console.log("Received data:", req.body);
    const args = [
      R_star.toString(),
      L_star.toString(),
      T_eff.toString(),
      R_planet.toString(),
      M_planet.toString(),
      semi_major_axis.toString(),
      eccentricity.toString(),
      inclination.toString(),
      albedo.toString(),
      distance.toString(),
      D_telescope.toString(),
      wavelength.toString(),
      IWA.toString(),
      OWA.toString(),
      contrast_limit.toString(),
    ];

    const pythonProcess = spawn("python3", ["main.py", ...args]);
    let pythonOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      pythonOutput += data.toString();
    });
    pythonProcess.stderr.on("data", (data) => {
      console.error(`Error from Python: ${data}`);
    });
    pythonProcess.on("close", (code) => {
      console.log(`Python process exited with code ${code}`);
      try {
        const result = JSON.parse(pythonOutput);
        res.status(200).json({ data: result });
      } catch (e) {
        console.error("Error parsing JSON from Python output:", e);
        res.status(500).json({ message: "Error processing Python output" });
      }
    });
  } catch (err) {
    console.log(err);
    res.status(500).json({ message: "Internal server error" });
  }
});
