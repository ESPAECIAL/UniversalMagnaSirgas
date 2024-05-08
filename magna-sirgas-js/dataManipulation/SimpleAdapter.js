// Import necessary modules
const ndarray = require('@stdlib/ndarray-array');
const MagnaSirgasCRS = require('../MagnaSirgasCRS');
const logger = require('../logger');

// Define the SimpleAdapter class
class SimpleAdapter {
    // Define class constants
    static COL_ARRAY = 1;
    static COORDS_2D = 2;
    static DTYPE_64 = Float64Array;
    static DTYPE_32 = Float32Array;
    static NAME = "SimpleAdapter";
    static PROJECTION = "forward-projection";
    static INVERSE_PROJECTION = "inverse-projection";
    static ELIP_TRANSFORMATION = "elipsoidal-transformation";

    constructor() {
        // Initialize properties
        this.errorMessage = [];
        this.warningMessage = [];
    }

    getResults() {
        return this.results;
    }

    logOriginTargetAreNotProjectable(crs1, crs2) {
        return logger.error(`The crs' ${crs1} and ${crs2} do not create a pipeline to project because they're not Magna Sirgas CRS`);
    }

    differentiatesInputPatterns(coords, functional = "forward-projection") {
        this.matchesSingle2dCoords(coords, { functional });
        if (!this.coordsAreSinglePaired) {
            this.matchesNotSingle2dCoords(coords, { functional });
        }
        this.printsFinalMessage();
    }

    matchesSingle2dCoords(coords, functional = "transformation") {
        this._coordsAreSinglePaired = true;
        coords.forEach(coord => {
            switch (true) {
                case (
                    typeof coord[0] === "number" &&
                    typeof coord[1] === "number" &&
                    this.validatesBoundariedSinglePairedCoords(coord[0], coord[1])
                ):
                    this.segmentatesFunctionals(coord[0], coord[1], { functional });
                    break;

                case (
                    typeof coord[0] === "number" &&
                    typeof coord[1] === "number" &&
                    !this.validatesBoundariedSinglePairedCoords(coord[0], coord[1])
                ):
                    this.warningMessage.push("Coordinates are not all within the crs boundaries.");
                    this.segmentatesFunctionals(coord[0], coord[1], { functional });
                    break;

                case (
                    typeof coord[0] === "string" &&
                    typeof coord[1] === "string" &&
                    this.validatesAreTransformableToFloat(coord[0], coord[1])
                ):
                    const [float_e, float_n] = this.transformsSingleCoordsToFloat(coord);
                    this.warningMessage.push("Coordinates were transformed to floats.");
                    if (!this.validatesBoundariedSinglePairedCoords(float_e, float_n)) {
                        this.warningMessage.push("Coordinates are not all within the crs boundaries.");
                    }
                    this.segmentatesFunctionals(float_e, float_n, { functional });
                    break;

                case (
                    typeof coord[0] === "string" &&
                    typeof coord[1] === "string" &&
                    !this.validatesAreTransformableToFloat(coord[0], coord[1])
                ):
                    this.errorMessage.push("Coordinates cannot be transformed to floats.");
                    this.results = null;
                    break;

                default:
                    this.coordsAreSinglePaired = false;
            }
        });
    }

    matchesNotSingle2dCoords(coords, functional = "transformation") {
        switch (true) {
            case this.validates2dFloatSequenceBoundariedCoordinates(coords):
                const narrays_coords = this.2dIterableToNarray(coords);
                this.segmentatesFunctionals(...narrays_coords, { functional });
                break;

            case this.validates2dFloatTransformable(coords):
                const transformedCoords = this.transforms2dTupleToFloat(coords);
                this.warningMessage.push(
                    "Coordinates were not all floats, but transformed to floats.",
                    "Coordinates are not all within the crs boundaries."
                );
                const narraysCoords = this.2dIterableToNarray(transformedCoords);
                this.segmentatesFunctionals(...narraysCoords, { functional });
                break;

            case !this.validatesIsIterable(coords):
                this.errorMessage.push("The object for the coordinates is not iterable.");
                break;

            case !this.validatesIsAlways2d(coords):
                this.results = null;
                this.errorMessage.push("Coordinates are not always bidimensional.");
                break;

            case !this.validatesAreTransformableToFloat(coords):
                this.results = null;
                this.errorMessage.push("Coordinates are not all transformable to float.");
                break;

            default:
                this.results = null;
                this.errorMessage.push("Invalid coords. Unknown error.");
                break;
        }
    }

    printsFinalMessage() {
        if (this.hasWarningMessage()) {
            console.log(this.warningMessage.join(" ").trim());
        }
        if (this._has_errorMessage()) {
            console.error(this.errorMessage.join(" ").trim());
        } else {
            console.log("Successful");
        }
    }

    validatesBoundariedSinglePairedCoords(e, n) {
        const e_is_well_boundaried = e >= this.crs1._min_west && e < this.crs1._max_east;
        const n_is_well_boundaried = n >= this.crs1._min_south && n < this.crs1._max_north;
        return e_is_well_boundaried && n_is_well_boundaried;
    }
    
    // Define abstract method (if needed)
    validatesCoordTypes(crs1, crs2) {
        return this.areCrsMagnasirgasCRSSubclasses(crs1, crs2);
    }

    areCrsMagnasirgasCRSSubclasses(self, ...many_crs) {
        for (const crs of many_crs) {
            if (!this.isMagnaSirgasCRSSubclass(crs)) {
                return false;
            }
        }
        return true;
    }

    isMagnaSirgasCRSSubclass(self, crs) {
        return crs instanceof MagnaSirgasCRS;
    }

    // Define other methods
    get_results() {
        return this.results;
    }

    // More methods...
}

module.exports = SimpleAdapter;