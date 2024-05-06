const MagnaSirgasCRS = require('../MagnaSirgasCRS');

class Ellipsoidal extends MagnaSirgasCRS {
    constructor() {
        super();
        this._max_north = 90.0;
        this._min_south = -90.0;
        this._max_east = 180.0;
        this._min_west = -180.0;
        this._crs_type = "Ellipsoidal";
    }
    name_from_proj() {
        // Implementation
    }
}

module.exports = Ellipsoidal;
